# coding=utf-8
import sys

import math
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
from RoleModule.role_manager import RoleManager, PLAYER_ROLE


class BulletEngine(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.init_shader()
        self.init_light_camera()
        self.init_bullet_engine()
        self.setup()
        self.init_input()
        taskMgr.add(self.update,'updateWorld')


    # 灯光镜头初始化
    def init_light_camera(self):
         self.setBackgroundColor(0.1, 0.1, 0.8, 1)
         self.setFrameRateMeter(True)

         # self.cam.setPos(0, -20, 4)
         # self.cam.lookAt(0, 0, 0)

         self.cam.setPos(0, 0, 100)
         self.cam.lookAt(0, 0, -90)

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

    # 输入初始化
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
        self.accept('control', self.doCrouch)
        self.accept('1',self.getCurrentPos)

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
        self.actor_character_NP.setJumpSpeed(JUMPSPEED)
        self.actor_character_NP.setMaxJumpHeight(JUMPHEIGHT)
        self.actor_character_NP.isOnGround()
        self.actor_character_NP.doJump()

    def getCurrentPos(self):
        print "角色当前位置 %s" % self.actorNP.getPos()

    # ____TASK___

    def processInput(self, dt):
        speed = Vec3(0, 0, 0)
        omega = 0.0
        force = Vec3(0,0,0)
        torque = Vec3(0,0,0)

        if inputState.isSet('forward'): speed.setY(-SPEED)
        if inputState.isSet('forward'): force.setY(-SPEED)
        if inputState.isSet('back'): speed.setY(SPEED)
        if inputState.isSet('back'): force.setY(SPEED)
        if inputState.isSet('turnLeft'):  omega = 120.0
        if inputState.isSet('turnLeft'):  torque = 120.0
        if inputState.isSet('turnRight'): omega = -120.0
        if inputState.isSet('turnRight'): torque = -120.0

        force *= 30.0
        torque *= 10.0
        # character
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
        self.omega = 0.0

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
        pFrom = Point3(0,0,0)
        pTo = Point3()

        print "omega"
        omega = self.actorNP.getHpr().getX()
        print omega
        omega = (omega - 90)%360
        v = Point3(math.cos(omega * math.pi / 180), math.sin(omega * math.pi / 180),0)
        v.normalize()
        v *= BULLETSPEED
        print '子弹速度 %s' %v
        #create Bullet
        size = Vec3(7,7,7)
        pFrom = self.actorNP.getPos()
        print '玩家位置 %s' %pFrom
        x = self.actorNP.getPos().getX()
        y = self.actorNP.getPos().getY()
        z = self.actorNP.getPos().getZ()
        hpr = self.actorNP.getHpr()
        print '玩家位置x %s' % x
        print '玩家位置y %s' % y
        print '玩家位置z %s' % z
        print '玩家方向hpr %s' % hpr
        print '胶囊包围体r %s' % self.actor_character_NP.getShape().getRadius()
        cosOmg = 10*math.cos(omega*math.pi/180)
        sinOmg = 10*math.sin(omega*math.pi/180)
        bulletNP = self.create_box_rigid('Bullet',size,Point3(x+cosOmg,y+sinOmg,10),True)
        bulletNP.node().setLinearVelocity(v)
        self.world.attachRigidBody(bulletNP.node())
        bulletNP.setCollideMask(BitMask32.allOff())
        print '子弹方向hpr %s' % v
        print '子弹位置 %s' %bulletNP.getPos()

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
        self.sceneMgr = SceneManager()
        self.sceneMgr.build_on(self)

        # Plane (static)
        shape = BulletPlaneShape(Vec3(0, 0, 1), 0)

        np = self.worldNP.attachNewNode(BulletRigidBodyNode('Ground'))
        np.node().addShape(shape)
        np.setPos(0, 0, -1)
        np.setCollideMask(BitMask32.allOn())
        self.world.attachRigidBody(np.node())

        # 测试用房子
        village = self.sceneMgr.add_model_scene(TEST_MAIN_SCENE,self.render)
        village.setTwoSided(True)
        village.setScale(5.0)

        ##测试碰撞平面(西)
        normal = Vec3(0,1,0)
        d = 0
        shape = BulletPlaneShape(normal,d)
        np = self.worldNP.attachNewNode(BulletRigidBodyNode('west_end'))
        np.node().addShape(shape)
        np.setPos(0,-430,0)
        np.setCollideMask(BitMask32.allOn())
        self.world.attachRigidBody(np.node())

        ##测试碰撞平面(东)
        normal = Vec3(0, -1, 0)
        d = 0
        shape = BulletPlaneShape(normal, d)
        np = self.worldNP.attachNewNode(BulletRigidBodyNode('west_end'))
        np.node().addShape(shape)
        np.setPos(0, 400, 0)
        np.setCollideMask(BitMask32.allOn())
        self.world.attachRigidBody(np.node())

        ##测试碰撞平面(北)
        normal = Vec3(1,0,0)
        d = 0
        shape = BulletPlaneShape(normal,d)
        np = self.worldNP.attachNewNode(BulletRigidBodyNode('north_end'))
        np.node().addShape(shape)
        np.setPos(-300,0,0)
        np.setCollideMask(BitMask32.allOn())
        self.world.attachRigidBody(np.node())

        ##测试碰撞平面(南)
        normal = Vec3(-1,0,0)
        d = 0
        shape = BulletPlaneShape(normal,d)
        np = self.worldNP.attachNewNode(BulletRigidBodyNode('north_end'))
        np.node().addShape(shape)
        np.setPos(330,0,0)
        np.setCollideMask(BitMask32.allOn())
        self.world.attachRigidBody(np.node())

        # Some boxes
        # size = 9.0
        # shape = BulletBoxShape(Vec3(size,size,size))
        # body = BulletRigidBodyNode('Big box')
        # self.boxNP = self.worldNP.attachNewNode(body)
        # self.boxNP.node().addShape(shape)
        # # self.boxNP.node().setMass(100.0)
        # self.boxNP.node().setDeactivationEnabled(False)
        # self.boxNP.setPos(0,0,10)
        # self.boxNP.setCollideMask(BitMask32.allOn())
        # self.world.attachRigidBody(self.boxNP.node())

        house1NP = self.create_box_rigid('house1',Vec3(5,5,5),Vec3(0,0,5),False)
        self.world.attachRigidBody(house1NP.node())
        house1NP.node().setDeactivationEnabled(False)

        # 猎人
        actor = self.sceneMgr.add_actor_scene(HUNTER_PATH,
                                         HUNTER_ACTION_PATH,
                                         self.render)
        actor.setPos(0,1,-10)
        actor.setScale(1.6)
        actor.setTwoSided(True)
        self.add_actor_collide(actor,3.5,15)

        # control
        self.sceneMgr.get_ActorMgr().set_clock(globalClock)
        actorId = self.sceneMgr.get_ActorMgr().get_resId(actor)
        self.sceneMgr.get_ActorMgr().add_toggle_to_actor("w", actorId, "run")
        self.sceneMgr.get_ActorMgr().add_toggle_to_actor("s", actorId, "run_back")
        self.sceneMgr.get_ActorMgr().add_toggle_to_actor("z", actorId, "rda")
        self.sceneMgr.get_ActorMgr().add_toggle_to_actor("x", actorId, "lda")
        self.sceneMgr.get_ActorMgr().add_toggle_to_actor("c", actorId, "bda")
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

        self.sceneMgr.bind_CameraController(camCtrlr)
        self.sceneMgr.get_ActorMgr().bind_CameraController(camCtrlr)

        print self.sceneMgr.get_ActorMgr().get_eventActionRecord()
        print self.sceneMgr.get_ActorMgr().get_eventEffertRecord()

        self.roleMgr = RoleManager()
        self.sceneMgr.get_ActorMgr().bind_RoleManager(self.roleMgr)
        self.roleMgr.bind_SceneManager(self.sceneMgr)
        player = self.roleMgr.create_role(roleType="PlayerRole",
                                     modelId=actorId)
        player.print_all_attr()

        self.taskMgr.add(self.sceneMgr.update_scene, "update_scene")

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