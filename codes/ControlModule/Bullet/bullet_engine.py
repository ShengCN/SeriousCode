# coding=utf-8
import sys
sys.path.append('../../')
import math
from direct.showbase.DirectObject import DirectObject
from direct.showbase.InputStateGlobal import inputState
from direct.showbase.ShowBase import ShowBase, AntialiasAttrib, NodePath, LPoint3f
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
from ControlModule.math_helper import MathHelper
from panda3d.ai import *
from pandac.PandaModules import Material
from pandac.PandaModules import VBase4



class BulletEngine(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.math_helper = MathHelper()
        self.init_shader()
        self.init_light_camera()
        self.init_mgr()
        self.init_bullet_engine()
        self.init_AI()
        self.scene_1()
        self.init_input()

        taskMgr.add(self.update,'updateWorld')

    def init_mgr(self):
        self.sceneMgr = SceneManager()
        self.roleMgr = RoleManager()
        self.sceneMgr.bind_RoleManager(self.roleMgr)

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
        self.accept('2',self.all_collide_result)

        inputState.watchWithModifiers('back', 's')
        inputState.watchWithModifiers('forward', 'w')
        inputState.watchWithModifiers('turnLeft', 'a')
        inputState.watchWithModifiers('turnRight', 'd')

    # 初始化 AI
    def init_AI(self):
        self.AIworld = AIWorld(self.worldNP)

    # _____HANDLER_____
    def doExit(self):
        # self.cleanup()
        sys.exit(1)

    def doReset(self):
        self.cleanup()
        # self.setup()

    def toggleDebug(self):
        if self.debugNP.isHidden():
            self.debugNP.show()
        else:
            self.debugNP.hide()

    def doScreenshot(self):
        self.screenshot('Bullet')

    def doJump(self):
        self.actor_character_Node.setJumpSpeed(JUMP_SPEED)
        self.actor_character_Node.setMaxJumpHeight(JUMP_HEIGHT)
        self.actor_character_Node.isOnGround()
        self.actor_character_Node.doJump()

    def getCurrentPos(self):
        print "角色当前位置 %s" % self.actorNP.getPos()
        print "角色当前朝向 %s" % self.actorNP.getHpr()

    def cleanup(self):
        ###todo
        ###1.destroy all actor
        ###2.destroy all collison node
        self.world = None
        self.worldNP.removeNode()
        self.taskMgr.remove("updateWorld")

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
        self.actorNP.node().setAngularMovement(omega)
        self.actorNP.node().setLinearMovement(speed,True)

    def update(self, task):
        dt = globalClock.getDt()
        self.processInput(dt)
        self.world.doPhysics(dt,4,1./240.)
        self.all_collide_result()
        return task.cont

    def all_collide_result(self):
        self.result = self.world.contactTest(self.wife_character_NP.node())
        for contact in self.result.getContacts():
            if type(contact.getNode1()) != type(self.actor_character_Node):
                if contact.getNode1().isStatic() == False:
                    print "人物所有的碰撞结果：%s" % self.result.getNumContacts()
                    print "wifi 受到了攻击"
                    print "%s%s 发生了碰撞" % (contact.getNode0(), contact.getNode1())
                    self.roleMgr.calc_attack("PlayerRole", self.actorRole2.get_attr_value("roleId"))
                    print "怪物血量:%s" %self.actorRole2.get_attr_value("hp")

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
        v *= BULLET_SPEED
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
        print '胶囊包围体r %s' % self.actor_character_Node.getShape().getRadius()
        cosOmg = 10*math.cos(omega*math.pi/180)
        sinOmg = 10*math.sin(omega*math.pi/180)
        bulletNP = self.create_box_rigid('Bullet',BULLET_SIZE,Point3(x+cosOmg,y+sinOmg,10),True)
        bulletNP.node().setLinearVelocity(v)
        self.world.attachRigidBody(bulletNP.node())
        bulletNP.setCollideMask(BitMask32.allOff())
        print '子弹方向hpr %s' % v
        print '子弹位置 %s' %bulletNP.getPos()

        # Remove the bullet again after 1 sec
        taskMgr.doMethodLater(1,self.doRemove,'doRemove',
                            extraArgs=[bulletNP],
                            appendTask=True)

    def doCrouch(self):
        self.crouching = not self.crouching
        sz = self.crouching and 0.6 or 1.0
        # self.actor_shape.setLocalScale(Vec3(1,1,sz))
        self.actorNP.setScale(Vec3(1,1,sz) * 0.3048)

    """""""""""""""
    碰撞体部分
    """""""""""""""
    def add_plane_collide(self,pos,normal):
        d = 0
        shape = BulletPlaneShape(normal,d)
        np = self.worldNP.attachNewNode(BulletRigidBodyNode('west_end'))
        np.node().addShape(shape)
        np.setPos(pos)
        np.setCollideMask(BitMask32.allOn())
        self.world.attachRigidBody(np.node())

    def add_actor_collide(self,actor,radius,height):
        # 猎人胶囊碰撞体
        r = radius
        h = height
        self.actor_shape = BulletCapsuleShape(r, height, ZUp)
        self.actor_character_Node = BulletCharacterControllerNode(self.actor_shape, 1.0, 'Player')
        self.actorNP = self.worldNP.attachNewNode(self.actor_character_Node)
        self.actorNP.setPos(-20, 30, 0)
        self.actorNP.setCollideMask(BitMask32.allOn())
        self.world.attachCharacter(self.actorNP.node())
        # actor.detachNode(self.world)
        actor.reparentTo(self.actorNP)

    def add_model_collide(self,actor,radius,height,name):
        # 怪物胶囊碰撞体
        r = radius
        h = height
        # 加入 render 世界
        actor_shape = BulletCapsuleShape(r, height, ZUp)
        actor_np = self.worldNP.attachNewNode(BulletRigidBodyNode(name))
        actor_np.setPos(0,0,10)
        actor_np.node().addShape(actor_shape)
        actor.reparentTo(actor_np)
        #加入物理引擎
        self.world.attachRigidBody(actor_np.node())
        # actorNP.reparentTo(actor)
        return actor_np

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

    """""""""""""""
    玩家的游戏参数
    """""""""""""""
    def setAI(self):
        self.wifi_AI_wander()
        self.taskMgr.add(self.AIUpdate,"AIUpate")

    # AI 闲逛
    def wifi_AI_wander(self):
        self.AIchar = AICharacter("wanderer", self.wife_character_NP, 100, 0.05, 5)
        self.AIworld.addAiChar(self.AIchar)
        self.AIbehaviors = self.AIchar.getAiBehaviors()
        self.AIbehaviors.wander(5, 0, 10, 1)

    # AI 追踪
    def wifi_AI_seek(self):
        self.AIchar = AICharacter("pursuer", self.wife_character_NP, 100, 0.05, 5)
        self.AIworld.addAiChar(self.AIchar)
        self.AIbehaviors = self.AIchar.getAiBehaviors()
        self.AIbehaviors.pursue(self.actorNP)

    def AIUpdate(self,task):
        if self.isDanger():
            # self.AIbehaviors.removeAiChar("wander")
            self.AIbehaviors.pursue(self.actorNP)
        else:
            self.AIbehaviors.wander(5, 0, 10, 1)

        self.AIworld.update()
        return task.cont

    def isDanger(self):
        relativePos = self.actorNP.getPos(self.wife_character_NP)
        length = self.math_helper.get_length(relativePos)
        print "他们的距离是: ",length
        if length < DANGER_LENGTH:
            return True
        else:
            return False
    """""""""""""""
    场景部分
    """""""""""""""
    def scene_1(self):
        # Plane (static)
        shape = BulletPlaneShape(Vec3(0, 0, 1), 0)

        np = self.worldNP.attachNewNode(BulletRigidBodyNode('Ground'))
        np.node().addShape(shape)
        np.setPos(0, 0, -1)
        np.setCollideMask(BitMask32.allOn())
        self.world.attachRigidBody(np.node())

        # 村庄
        village = self.sceneMgr.add_model_scene(OUTER, self.render)
        village.setTwoSided(True)
        village.setScale(5.0)

        # 整个场景的碰撞体
        self.add_plane_collide(Point3(0, -430, 0), Vec3(0, 1, 0))  ##测试碰撞平面(西)
        self.add_plane_collide(Point3(0, 400, 0), Vec3(0, -1, 0))  ##测试碰撞平面(东)
        self.add_plane_collide(Point3(-300, 0, 0), Vec3(1, 0, 0))  ##测试碰撞平面(北)
        self.add_plane_collide(Point3(330, 0, 0), Vec3(-1, 0, 0))  ##测试碰撞平面(南)

        # 房子包围体
        house1NP = self.create_box_rigid('house1', Vec3(5, 5, 5), Vec3(0, 0, 5), False)
        self.world.attachRigidBody(house1NP.node())
        house1NP.node().setDeactivationEnabled(False)

        # 猎人
        self.actor_hunter = self.sceneMgr.add_actor_scene(HUNTER_PATH,
                                                          HUNTER_ACTION_PATH,
                                                          self.render)
        self.actor_hunter.setPos(0, 1, -10)  # 相对于胶囊体坐标
        self.actor_hunter.setScale(1.6)
        self.actor_hunter.setTwoSided(True)
        self.add_actor_collide(self.actor_hunter, 3.5, 15)
        self.actorNP.setPos(-30, 30, 0)

        # 怪物
        self.actor_wife = self.sceneMgr.add_actor_scene(WIFE_ZOMBIE_PATH,
                                                        WIFE_ZOMBIE_ACTION_PATH,
                                                        self.render)
        self.actor_wife.setPos(0, 0, -10)
        self.actor_wife.setScale(1)
        self.actor_wife.setTwoSided(True)
        self.actor_wife.setH(-90)
        self.wife_character_NP = self.add_model_collide(self.actor_wife, 4, 18, 'WIFI')
        print "怪物现在的位置：", self.actor_wife.getPos(render)
        print "怪物现在的朝向：", self.actor_wife.getHpr(render)
        # self.wifi_AI_wander()
        self.setAI()

        # control
        self.sceneMgr.get_ActorMgr().set_clock(globalClock)
        actorId1 = self.sceneMgr.get_ActorMgr().get_resId(self.actor_hunter)
        actorId2 = self.sceneMgr.get_ActorMgr().get_resId(self.actor_wife)
        self.sceneMgr.get_ActorMgr().add_toggle_to_actor("w", actorId1, "run")
        self.sceneMgr.get_ActorMgr().add_toggle_to_actor("s", actorId1, "run_back")
        self.sceneMgr.get_ActorMgr().add_toggle_to_actor("player_be_attacked1", actorId1, "rda")
        self.sceneMgr.get_ActorMgr().add_toggle_to_actor("player_be_attacked2", actorId1, "lda")
        self.sceneMgr.get_ActorMgr().toggle_actor_attack("mouse1", actorId1)
        self.sceneMgr.get_ActorMgr().add_toggle_to_actor("enemy_run", actorId2, "walk")
        self.sceneMgr.get_ActorMgr().add_toggle_to_actor("enemy_attack", actorId2, "attack")

        self.sceneMgr.get_ActorMgr().print_eventEffertRecord()

        camCtrlr = CameraController()
        camCtrlr.bind_camera(self.cam)
        camCtrlr.bind_ToggleHost(self)
        camCtrlr.set_clock(globalClock)
        camCtrlr.focus_on(self.actor_hunter, 100)
        camCtrlr.set_rotateSpeed(10)
        camCtrlr.add_toggle_to_opt("u", "rotate_around_up")
        camCtrlr.add_toggle_to_opt("j", "rotate_around_down")
        camCtrlr.add_toggle_to_opt("h", "rotate_around_cw")
        camCtrlr.add_toggle_to_opt("k", "rotate_around_ccw")

        self.sceneMgr.bind_CameraController(camCtrlr)
        self.sceneMgr.get_ActorMgr().bind_CameraController(camCtrlr)

        # create role
        self.actorRole = self.roleMgr.create_role("PlayerRole", self.sceneMgr.get_resId(self.actor_hunter))
        self.actorRole2 = self.roleMgr.create_role("EnemyRole", self.sceneMgr.get_resId(self.actor_wife))

        print self.sceneMgr.get_ActorMgr().get_eventActionRecord()
        print self.sceneMgr.get_ActorMgr().get_eventEffertRecord()

        self.taskMgr.add(self.sceneMgr.update_scene, "update_scene")

    def scene_2(self):
        # Plane (static)
        shape = BulletPlaneShape(Vec3(0, 0, 1), 0)

        np = self.worldNP.attachNewNode(BulletRigidBodyNode('Ground'))
        np.node().addShape(shape)
        np.setPos(0, 0, -1)
        np.setCollideMask(BitMask32.allOn())
        self.world.attachRigidBody(np.node())

        # 村庄
        village = self.sceneMgr.add_model_scene(OUTER, self.render)
        village.setTwoSided(True)
        village.setScale(5.0)

        # 整个场景的碰撞体
        self.add_plane_collide(Point3(0, -430, 0), Vec3(0, 1, 0))  ##测试碰撞平面(西)
        self.add_plane_collide(Point3(0, 400, 0), Vec3(0, -1, 0))  ##测试碰撞平面(东)
        self.add_plane_collide(Point3(-300, 0, 0), Vec3(1, 0, 0))  ##测试碰撞平面(北)
        self.add_plane_collide(Point3(330, 0, 0), Vec3(-1, 0, 0))  ##测试碰撞平面(南)

        # 房子包围体
        house1NP = self.create_box_rigid('house1', Vec3(5, 5, 5), Vec3(0, 0, 5), False)
        self.world.attachRigidBody(house1NP.node())
        house1NP.node().setDeactivationEnabled(False)

        # 猎人
        self.actor_hunter = self.sceneMgr.add_actor_scene(HUNTER_PATH,
                                                          HUNTER_ACTION_PATH,
                                                          self.render)
        self.actor_hunter.setPos(0, 1, -10)  # 相对于胶囊体坐标
        self.actor_hunter.setScale(1.6)
        self.actor_hunter.setTwoSided(True)
        self.add_actor_collide(self.actor_hunter, 3.5, 15)
        self.actorNP.setPos(-30, 30, 0)

        # 怪物
        self.actor_wife = self.sceneMgr.add_actor_scene(WIFE_ZOMBIE_PATH,
                                                        WIFE_ZOMBIE_ACTION_PATH,
                                                        self.render)
        self.actor_wife.setPos(0, 0, -10)
        self.actor_wife.setScale(1)
        self.actor_wife.setTwoSided(True)
        self.actor_wife.setH(-90)
        self.wife_character_NP = self.add_model_collide(self.actor_wife, 4, 18, 'WIFI')
        print "怪物现在的位置：", self.actor_wife.getPos(render)
        print "怪物现在的朝向：", self.actor_wife.getHpr(render)
        # self.wifi_AI_wander()
        self.setAI()

        # control
        self.sceneMgr.get_ActorMgr().set_clock(globalClock)
        actorId1 = self.sceneMgr.get_ActorMgr().get_resId(self.actor_hunter)
        actorId2 = self.sceneMgr.get_ActorMgr().get_resId(self.actor_wife)
        self.sceneMgr.get_ActorMgr().add_toggle_to_actor("w", actorId1, "run")
        self.sceneMgr.get_ActorMgr().add_toggle_to_actor("s", actorId1, "run_back")
        self.sceneMgr.get_ActorMgr().add_toggle_to_actor("player_be_attacked1", actorId1, "rda")
        self.sceneMgr.get_ActorMgr().add_toggle_to_actor("player_be_attacked2", actorId1, "lda")
        self.sceneMgr.get_ActorMgr().toggle_actor_attack("mouse1", actorId1)
        self.sceneMgr.get_ActorMgr().add_toggle_to_actor("enemy_run", actorId2, "walk")
        self.sceneMgr.get_ActorMgr().add_toggle_to_actor("enemy_attack", actorId2, "attack")

        self.sceneMgr.get_ActorMgr().print_eventEffertRecord()

        camCtrlr = CameraController()
        camCtrlr.bind_camera(self.cam)
        camCtrlr.bind_ToggleHost(self)
        camCtrlr.set_clock(globalClock)
        camCtrlr.focus_on(self.actor_hunter, 100)
        camCtrlr.set_rotateSpeed(10)
        camCtrlr.add_toggle_to_opt("u", "rotate_around_up")
        camCtrlr.add_toggle_to_opt("j", "rotate_around_down")
        camCtrlr.add_toggle_to_opt("h", "rotate_around_cw")
        camCtrlr.add_toggle_to_opt("k", "rotate_around_ccw")

        self.sceneMgr.bind_CameraController(camCtrlr)
        self.sceneMgr.get_ActorMgr().bind_CameraController(camCtrlr)

        # create role
        self.actorRole = self.roleMgr.create_role("PlayerRole", self.sceneMgr.get_resId(self.actor_hunter))
        self.actorRole2 = self.roleMgr.create_role("EnemyRole", self.sceneMgr.get_resId(self.actor_wife))

        print self.sceneMgr.get_ActorMgr().get_eventActionRecord()
        print self.sceneMgr.get_ActorMgr().get_eventEffertRecord()

        self.taskMgr.add(self.sceneMgr.update_scene, "update_scene")


game = BulletEngine()
game.run()