# coding=utf-8
import sys
from direct.showbase.DirectObject import DirectObject
from direct.showbase.InputStateGlobal import inputState
from direct.showbase.ShowBase import ShowBase, AntialiasAttrib, NodePath
from direct.task.TaskManagerGlobal import taskMgr

from panda3d.core import AmbientLight
from panda3d.core import DirectionalLight
from panda3d.core import Vec3
from panda3d.core import Vec4
from panda3d.core import Point3
from panda3d.core import TransformState
from panda3d.core import BitMask32
from pandac.PandaModules import AntialiasAttrib, LODNode

from panda3d.bullet import BulletWorld, ZUp
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletDebugNode
from panda3d.bullet import BulletConvexHullShape
from panda3d.bullet import BulletBoxShape
from panda3d.bullet import BulletCharacterControllerNode
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletCapsuleShape
from panda3d.bullet import *

from ControlModule import common_para
from ControlModule.common_para import *
from SceneModule.scene_manager import SceneManager
from SceneModule.camera_controller import CameraController
from SceneModule.light_controller import LightController
from RoleModule.role_manager import RoleManager

class BulletEngine(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.init_shader()
        self.init_light_camera()
        self.init_input()
        self.init_bullet_engine()
        self.setup()
        taskMgr.add(self.update,'updateWorld')


    # 灯光镜头初始化
    def init_light_camera(self):
         self.setBackgroundColor(0.1, 0.1, 0.8, 1)
         self.setFrameRateMeter(True)

         self.cam.setPos(0, -20, 4)
         self.cam.lookAt(0, 0, 0)

         # Light
         alight = AmbientLight('ambientLight')
         alight.setColor(Vec4(0.5, 0.5, 0.5, 1))
         alightNP = render.attachNewNode(alight)

         dlight = DirectionalLight('directionalLight')
         dlight.setDirection(Vec3(1, 1, -1))
         dlight.setColor(Vec4(0.7, 0.7, 0.7, 1))
         dlightNP = render.attachNewNode(dlight)

         render.clearLight()
         render.setLight(alightNP)
         render.setLight(dlightNP)

    def init_input(self):
        self.accept('escape', self.doExit)
        self.accept('r', self.doReset)
        self.accept('f1', self.toggleWireframe)
        self.accept('f2', self.toggleTexture)
        self.accept('f3', self.toggleDebug)
        self.accept('f5', self.doScreenshot)

        # 事件管理
        self.accept('space', self.doJump)
        self.accept('mouse1',self.doShoot)
        self.accept('shift', self.doCrouch)

        inputState.watchWithModifiers('back', 's')
        inputState.watchWithModifiers('forward', 'w')
        inputState.watchWithModifiers('turnLeft', 'a')
        inputState.watchWithModifiers('turnRight', 'd')

    # _____HANDLER_____

    def doExit(self):
        # self.cleanup()
        sys.exit(1)

    def doReset(self):
        # self.cleanup()
        # self.setup()
        pass

    def toggleDebug(self):
        if self.debugNP.isHidden():
            self.debugNP.show()
        else:
            self.debugNP.hide()

    def doScreenshot(self):
        self.screenshot('Bullet')

    def doJump(self):
        self.actor_character_NP.setMaxJumpHeight(JUMPHEIGHT)
        self.actor_character_NP.setJumpSpeed(JUMPSPEED)
        self.actor_character_NP.isOnGround()
        self.actor_character_NP.doJump()

    # ____TASK___

    def processInput(self, dt):
        speed = Vec3(0, 0, 0)
        omega = 0.0

        if inputState.isSet('forward'): speed.setY(-SPEED)
        if inputState.isSet('back'): speed.setY(SPEED)
        if inputState.isSet('turnLeft'):  omega = 120.0
        if inputState.isSet('turnRight'): omega = -120.0

        self.actor_character_NP.setAngularMovement(omega)
        self.actor_character_NP.setLinearMovement(speed,True)

    def update(self, task):
        dt = globalClock.getDt()
        self.processInput(dt)
        self.world.doPhysics(dt,4,1./240.)
        return task.cont

    def init_shader(self):
        self.backfaceCullingOn()
        self.setFrameRateMeter(True)
        self.render.flattenStrong()
        self.render.setTwoSided(True)
        self.render.setAntialias(AntialiasAttrib.MAuto)

        lod = LODNode("lod")
        lodnp  = NodePath(lod)
        lodnp.reparentTo(self.render)

    def init_bullet_engine(self):
        self.worldNP = render.attachNewNode('World')
        self.world = BulletWorld()
        self.world.setGravity(Vec3(0, 0, -9.81))
        # World
        self.debugNP = self.worldNP.attachNewNode(BulletDebugNode('Debug'))
        self.debugNP.show()
        self.debugNP.node().showWireframe(True)
        self.debugNP.node().showConstraints(True)
        self.debugNP.node().showBoundingBoxes(False)
        self.debugNP.node().showNormals(True)
        self.world.setDebugNode(self.debugNP.node())
        # 玩家
        self.crouching = False

    def create_box_rigid(self,name,size,pos,isCCD):
        shape = BulletBoxShape(size)
        body = BulletRigidBodyNode(name)
        bodyNP = self.worldNP.attachNewNode(body)
        bodyNP.node().addShape(shape)
        bodyNP.node().setMass(2.0)
        bodyNP.setPos(pos)
        bodyNP.setCollideMask(BitMask32.allOn())

        if isCCD:
            bodyNP.node().setCcdMotionThreshold(1e-7);
            bodyNP.node().setCcdSweptSphereRadius(0.50);
        return bodyNP

    def doRemove(self,bulletNP,task):
        self.world.removeRigidBody(bulletNP.node())
        return task.done


    def doShoot(self):
        pFrom = Point3()
        pTo = Point3()

        print self.actorNP.getPos()

        #get from and to position
        pFrom =  self.actorNP.getPos() + Point3(0,0,5)
        pTo = self.boxNP.getPos()

        # calculate initial velocity
        v = pTo - pFrom
        v.normalize()
        v *= 0.1
        print "v 的速度是: "
        print v
        #create Bullet
        size = Vec3(5,5,5)
        bulletNP = self.create_box_rigid('Bullet',size,pFrom,True)
        bulletNP.node().setMass(10.0)
        bulletNP.node().setLinearVelocity(v)
        self.world.attachRigidBody(bulletNP.node())

        # Remove the bullet again after 1 sec
        taskMgr.doMethodLater(1,self.doRemove,'doRemove',
                            extraArgs=[bulletNP],
                            appendTask=True)

    ####################### some probelm todo  #########################################
    def doCrouch(self):
        self.crouching = not self.crouching
        sz = self.crouching and 0.6 or 1.0
        # self.actor_shape.setLocalScale(Vec3(1,1,sz))
        self.actorNP.setScale(Vec3(1,1,sz) * 0.3048)


    def setup(self):
        sceneMgr = SceneManager()
        sceneMgr.build_on(self)

        # Plane (static)
        shape = BulletPlaneShape(Vec3(0, 0, 1), 0)

        np = self.worldNP.attachNewNode(BulletRigidBodyNode('Ground'))
        np.node().addShape(shape)
        np.setPos(0, 0, -1)
        np.setCollideMask(BitMask32.allOn())

        self.world.attachRigidBody(np.node())

        ## 村庄
        # villageModel = self.loader.loadModel(VILLAGE)
        # villageModel.setPos(0,0,0)
        # villageModel.setScale(5)
        # villageModel.setTwoSided(True)
        # # villageModel.reparentTo(self.render)
        # villageModel.clearLight()

        # # 场地碰撞节点
        # geomNodes = villageModel.findAllMatches('**/+GeomNode')
        # geomNode = geomNodes.getPath(0).node()
        # geom = geomNode.getGeom(0)
        # village_shape = BulletConvexHullShape()
        # village_shape.addGeom(geom)
        # village_coll_NP = self.worldNP.attachNewNode(BulletRigidBodyNode('village'))
        # village_coll_NP.node().addShape(village_shape)
        # village_coll_NP.setPos(0,0,0)
        # village_coll_NP.setScale(5)
        # village_coll_NP.setCollideMask(BitMask32.allOn())
        # self.world.attachRigidBody(village_coll_NP.node())
        # villageModel.reparentTo(village_coll_NP)

        # 测试用房子
        house1 = sceneMgr.add_model_scene(TEST_HOUSE1,self.render)
        house2 = sceneMgr.add_model_scene(TEST_HOUSE2,self.render)
        house3 = sceneMgr.add_model_scene(TEST_HOUSE3,self.render)
        self.add_house_collide(house1,Vec3(5,5,5),Vec3(0,20,0),"house1")
        self.add_house_collide(house1,Vec3(5,5,5),Vec3(0,-20,0),"house2")
        self.add_house_collide(house1,Vec3(5,5,5),Vec3(-20,0,0),"house3")
        house1.setTwoSided(True)
        house2.setTwoSided(True)
        house3.setTwoSided(True)

        # Some boxes
        size = 9.0
        shape = BulletBoxShape(Vec3(size,size,size))
        body = BulletRigidBodyNode('Big box')
        self.boxNP = self.worldNP.attachNewNode(body)
        self.boxNP.node().addShape(shape)
        self.boxNP.node().setMass(5.0)
        self.boxNP.node().setDeactivationEnabled(True)
        self.boxNP.setPos(0,0,10)
        self.boxNP.setCollideMask(BitMask32.allOn())
        self.world.attachRigidBody(self.boxNP.node())


        # 猎人
        actor = sceneMgr.add_actor_scene(HUNTER_PATH,
                                         HUNTER_ACTION_PATH,
                                         self.render)
        actor.setPos(0,1,-10)
        actor.setScale(1.6)
        actor.setTwoSided(True)
        self.add_actor_collide(actor,3.5,15)

        # control
        sceneMgr.get_ActorMgr().set_clock(globalClock)
        actorId = sceneMgr.get_ActorMgr().get_resId(actor)
        sceneMgr.get_ActorMgr().add_toggle_to_actor("w", actorId, "run")
        sceneMgr.get_ActorMgr().add_toggle_to_actor("s", actorId, "run_back")
        sceneMgr.get_ActorMgr().add_toggle_to_actor("z", actorId, "rda")
        sceneMgr.get_ActorMgr().add_toggle_to_actor("x", actorId, "lda")
        sceneMgr.get_ActorMgr().add_toggle_to_actor("c", actorId, "bda")
        print "actorId : ", actorId

        camCtrlr = CameraController()
        camCtrlr.bind_camera(self.cam)
        camCtrlr.bind_ToggleHost(self)
        camCtrlr.set_clock(globalClock)
        camCtrlr.focus_on(actor, 100)
        camCtrlr.set_rotateSpeed(10)
        camCtrlr.add_toggle_to_opt("u", "rotate_around_up")
        camCtrlr.add_toggle_to_opt("j", "rotate_around_down")
        camCtrlr.add_toggle_to_opt("h", "rotate_around_cw")
        camCtrlr.add_toggle_to_opt("k", "rotate_around_ccw")

        sceneMgr.bind_CameraController(camCtrlr)
        sceneMgr.get_ActorMgr().bind_CameraController(camCtrlr)

        print sceneMgr.get_ActorMgr().get_eventActionRecord()
        print sceneMgr.get_ActorMgr().get_eventEffertRecord()

        roleMgr = RoleManager()
        sceneMgr.get_ActorMgr().bind_RoleManager(roleMgr)
        player = roleMgr.create_role(roleType="PlayerRole",
                                     modelId=actorId)
        player.print_all_attr()

        self.taskMgr.add(sceneMgr.update_scene, "update_scene")

    def add_actor_collide(self,actor,radius,height):
        # 猎人胶囊碰撞体
        r = radius
        h = height
        self.actor_shape = BulletCapsuleShape(r, height, ZUp)
        self.actor_character_NP = BulletCharacterControllerNode(self.actor_shape, 1.0, 'Player')
        self.actorNP = self.worldNP.attachNewNode(self.actor_character_NP)
        self.actorNP.setPos(-20, 30, 0)
        self.actorNP.setCollideMask(BitMask32.allOn())
        self.world.attachCharacter(self.actorNP.node())
        # actor.detachNode(self.world)
        actor.reparentTo(self.actorNP)

    def add_house_collide(self, house, size,pos,houseName):
        # geomNodes = loader.loadModel(TEST_HOUSE1).findAllMatches('**/+GeomNode')
        # geomNode = geomNodes.getPath(0).node()
        # geom = geomNode.getGeom(0)
        # house_shape = BulletConvexHullShape()
        # house_shape.addGeom(geom)
        # houseNP = self.worldNP.attachNewNode(BulletRigidBodyNode(houseName))
        # houseNP.node().addShape(house_shape)
        # houseNP.setPos(pos)
        # # houseNP.node().setMass(10.0)
        # houseNP.setCollideMask(BitMask32.allOn())
        # self.world.attachRigidBody(houseNP.node())
        # house.reparentTo(houseNP)
        # house.setPos(0,0,0)
        pass


game = BulletEngine()
game.run()