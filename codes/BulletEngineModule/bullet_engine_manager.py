# coding=utf-8
"""""""""""""""
BulletEngineMgr 主要用来管理整个游戏场景中的物理碰撞的人物管理、场地碰撞管理、游戏 AI 管理。
编写人： codingblack
编写时间：2016.7.12
"""""""""""""""

import math
from direct.showbase.DirectObject import DirectObject
from direct.showbase.InputStateGlobal import inputState
from direct.showbase.ShowBase import ShowBase, AntialiasAttrib, NodePath, LPoint3f
from direct.task.TaskManagerGlobal import taskMgr
from panda3d.ai import AIWorld, AICharacter

from panda3d.core import AmbientLight
from panda3d.core import DirectionalLight
from panda3d.core import Vec3
from panda3d.core import Vec4
from panda3d.core import Point3
from panda3d.core import TransformState
from panda3d.core import BitMask32
from pandac.PandaModules import AntialiasAttrib, LODNode

from panda3d.bullet import *
from ControlModule.common_para import *
from ControlModule.math_helper import MathHelper
from SceneModule.camera_controller import CameraController


class BulletEngineMgr(DirectObject):
    def __init__(self,base,worldNP,sceneMgr,roleMgr,resMgr):
        DirectObject.__init__(self)
        self.base = base
        self.worldNP = worldNP
        self.sceneMgr = sceneMgr
        self.roleMgr = roleMgr
        self.resMgr = resMgr
        self.initAll()

    def initAll(self):
        self.init_bullet_engine()
        self.init_roles()
        self.init_input()

    # 初始化 bullet 引擎
    def init_bullet_engine(self):
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
        # 地板(static)
        shape = BulletPlaneShape(Vec3(0, 0, 1), 0)
        np = self.worldNP.attachNewNode(BulletRigidBodyNode('Ground'))
        np.node().addShape(shape)
        np.setPos(0, 0, -1)
        np.setCollideMask(BitMask32.allOn())
        self.world.attachRigidBody(np.node())

        # 玩家
        self.crouching = False
        self.omega = 0.0
        # 子弹
        self.bullet_model = loader.loadModel(BULLET_PATH)
        self.bullet_model.setScale(0.5)

    # 建立游戏世界碰撞体
    def add_bullet_world(self,box_world):
        self.add_plane_collide(box_world.west, Vec3(0, 1, 0))  ##测试碰撞平面(西)
        self.add_plane_collide(box_world.east, Vec3(0, -1, 0))  ##测试碰撞平面(东)
        self.add_plane_collide(box_world.north, Vec3(1, 0, 0))  ##测试碰撞平面(北)
        self.add_plane_collide(box_world.south, Vec3(-1, 0, 0))  ##测试碰撞平面(南

    def add_ball_bullet_world(self,radius):
        return self.add_ball_collide(radius)

    """""""""""""""
    人物管理部分
    """""""""""""""
    def init_roles(self):
        self.__enemy_list = dict()
        self.__enemy_NP = dict()
        self.__role_dict = dict()
        self.__NPC_Actor = dict()
        self.__chest_list = dict()
        self.__isDead = dict()
        self.init_AI()

    # 新增游戏主角
    def add_player_role(self,pos,hpr):
        # 猎人
        self.actor_hunter = self.sceneMgr.add_actor_scene(HUNTER_PATH,
                                                          HUNTER_ACTION_PATH,
                                                          self.base.render)
        self.actor_hunter.setPos(0, 1, -10)  # 相对于胶囊体坐标
        self.actor_hunter.setScale(1.6)
        self.actor_hunter.setTwoSided(True)
        self.add_actor_collide(self.actor_hunter,pos,hpr, 3.5, 15)

        # control
        self.sceneMgr.get_ActorMgr().set_clock(globalClock)
        actorId1 = self.sceneMgr.get_ActorMgr().get_resId(self.actor_hunter)
        self.sceneMgr.get_ActorMgr().add_toggle_to_actor("w", actorId1, "run")
        self.sceneMgr.get_ActorMgr().add_toggle_to_actor("s", actorId1, "run_back")
        self.sceneMgr.get_ActorMgr().add_toggle_to_actor("player_be_attacked1", actorId1, "rda")
        self.sceneMgr.get_ActorMgr().add_toggle_to_actor("player_be_attacked2", actorId1, "lda")
        self.sceneMgr.get_ActorMgr().toggle_actor_attack("mouse1", actorId1)

        # create role
        self.actorRole = self.roleMgr.create_role("PlayerRole", self.sceneMgr.get_resId(self.actor_hunter))
        print "新建猎人: ", self.actorRole.get_attr_value("currWeapon")

    # 新增 NPC
    def add_NPC_role(self,character_name,pos,scale,hpr=Vec3(0,0,0)):
        NPC_dic={
            "nun":NUN,
            "girl":GIRL,
            "stealer":STEALER
        }
        self.__NPC_amount = self.__NPC_amount + 1
        id = self.__NPC_amount - 1
        # 修女
        self.__NPC_Actor[id] = self.sceneMgr.add_actor_scene(NPC_dic[character_name],
                                                                            {},
                                                                            self.base.render)
        self.__NPC_Actor[id].setPos(pos)
        self.__NPC_Actor[id].setScale(scale)
        self.__NPC_Actor[id].setHpr(hpr)

        # create role
        actorRole = self.roleMgr.create_role("NPCRole",
                                            self.sceneMgr.get_resId(self.__NPC_Actor[id]),
                                            characterName=character_name)
        # 主角与 NPC 时间监听
        self.sceneMgr.get_ActorMgr().add_toggle_for_player_to_interact("e", self.sceneMgr.get_resId(self.actor_hunter))
        print "NPC 创建: ", self.actorRole.get_attr_value("currWeapon")

    # 新增 宝箱到场景
    def add_chest_role(self,pos,scale,):
        # 宝箱
        self.__chest_amount = self.__chest_amount + 1
        self.__chest_list[self.__chest_amount] = self.sceneMgr.add_actor_scene(CHEST,
                                                            CHEST_OPEN,
                                                            self.base.render)
        self.__chest_list[self.__chest_amount].setScale(scale)
        self.__chest_list[self.__chest_amount].setPos(pos)
        # create role
        self.actorRole = self.roleMgr.create_role("AttachmentRole",
                                                  self.sceneMgr.get_resId(self.__chest_list[self.__chest_amount]))
        self.sceneMgr.get_ActorMgr().add_toggle_to_actor("chest_open",
                                                         self.sceneMgr.get_resId(self.__chest_list[self.__chest_amount]),
                                                         "open")

    # 新增怪物
    def add_enemy_role(self,pos,scale,model_path,model_action_path):
        self.__amount = self.__amount + 1
        id = self.__amount - 1
        self.__isDead[id] = False
        self.add_enemy(id,pos,scale,model_path,model_action_path)
        self.setAI(id,self.__enemy_NP[id])

    # 增加敌人
    def add_enemy(self,id,pos,scale,model_path,action_path):
        self.__enemy_list[id] = self.sceneMgr.add_actor_scene(model_path,
                                                              action_path,
                                                              self.base.render)
        self.__enemy_list[id].setScale(scale)
        self.__enemy_list[id].setZ(-10)
        self.__enemy_NP[id] = self.add_model_collide(self.__enemy_list[id],pos,4,18,id)
        self.__enemy_NP[id].setZ(14)
        # 增加人物 role 到角色管理器
        role_id = self.sceneMgr.get_resId(self.__enemy_list[id])
        self.__role_dict[role_id] = self.roleMgr.create_role("EnemyRole", role_id)
        self.sceneMgr.get_ActorMgr().add_toggle_to_actor("enemy_walk", role_id, "walk")
        self.sceneMgr.get_ActorMgr().add_toggle_to_actor("enemy_attack", role_id, "attack")

        if id == 0:
            # role_id = self.sceneMgr.get_resId(self.__enemy_list[id])wwwwa
            # self.__role_dict[role_id] = self.roleMgr.create_role("EnemyRole", role_id)
            self.__role_dict[role_id].set_attr_value("Boss", 1)
            self.__role_dict[role_id].set_attr_value("hp", BOSS_HP)


    """""""""""""""
    物理世界碰撞体
    """""""""""""""
    # 用场景凸包建立碰撞体
    def add_box_convex(self,scene,height,scale):
        geomNodes = scene.findAllMatches('**/+GeomNode')
        geomNode = geomNodes.getPath(0).node()
        geom = geomNode.getGeom(0)
        world_shape = BulletConvexHullShape()
        world_shape.addGeom(geom)
        self.world_convex_np = self.worldNP.attachNewNode(BulletRigidBodyNode("convex_world"))
        self.world_convex_np.setScale(scale)
        self.world_convex_np.setPos(0,0,height)
        self.world_convex_np.node().addShape(world_shape)
        self.world_convex_np.setCollideMask(BitMask32.allOn())
        self.world.attachRigidBody(self.world_convex_np.node())


    # 房屋碰撞体
    def add_rigid_box(self,pos,size,hpr,id):
        shape = BulletBoxShape(size)
        box_np = self.worldNP.attachNewNode(BulletRigidBodyNode(str(id)))
        box_np.setPos(self.base.render,pos)
        box_np.node().addShape(shape)
        box_np.setHpr(self.base.render,hpr)
        box_np.setCollideMask(BitMask32.allOn())
        box_np.node().setDeactivationEnabled(False)
        self.world.attachRigidBody(box_np.node())


    # 人物碰撞体
    def add_model_collide(self,actor,pos,radius,height,name):
        # 怪物胶囊碰撞体
        r = radius
        h = height
        # 加入 render 世界
        actor_shape = BulletCapsuleShape(r, height, ZUp)
        actor_np = self.worldNP.attachNewNode(BulletRigidBodyNode(str(name)))
        actor_np.setPos(pos)
        actor_np.node().addShape(actor_shape)
        actor_np.setCollideMask(BitMask32.allOn())
        actor_np.node().setMass(ENEMY_MASS)
        actor.reparentTo(actor_np)
        #加入物理引擎
        self.world.attachRigidBody(actor_np.node())
        return actor_np

    def add_actor_collide(self,actor,pos,hpr,radius,height):
        # 猎人胶囊碰撞体
        r = radius
        h = height
        self.actor_shape = BulletCapsuleShape(r, height, ZUp)
        self.actor_character_Node = BulletCharacterControllerNode(self.actor_shape, 1.0, 'Player')
        self.actorNP = self.worldNP.attachNewNode(self.actor_character_Node)
        self.actorNP.setPos(pos)
        self.actorNP.setHpr(hpr)
        self.actorNP.setCollideMask(BitMask32.allOn())
        self.world.attachCharacter(self.actorNP.node())
        # actor.detachNode(self.world)
        actor.reparentTo(self.actorNP)

    def add_plane_collide(self,pos,normal):
        d = 0
        shape = BulletPlaneShape(normal,d)
        np = self.worldNP.attachNewNode(BulletRigidBodyNode('west_end'))
        np.node().addShape(shape)
        np.setPos(pos)
        np.setCollideMask(BitMask32.allOn())
        self.world.attachRigidBody(np.node())

    def add_ball_collide(self,radius):
        shape = BulletSphereShape(radius)
        np = self.worldNP.attachNewNode(BulletRigidBodyNode('ball_world'))
        np.node().addShape(shape)
        np.setCollideMask(BitMask32.allOff())
        self.world.attachRigidBody(np.node())
        return np

    """""""""""""""
    AI 部分
    """""""""""""""
    # 初始化 AI
    def init_AI(self):
        self.AIworld = AIWorld(self.worldNP)
        self.AI_Character = dict()
        self.__amount = 0
        self.__NPC_amount = 0
        self.__chest_amount = 0
        self.math_helper = MathHelper()

    # 为人物加上 AI 效果
    def setAI(self,id,enemy_np):
        self.AI_wander(id,enemy_np)

    # AI 闲逛
    def AI_wander(self,id, enemy_np):
        self.AI_Character[id] = AICharacter(str(id), enemy_np, 100, 0.05, 10)
        self.AIworld.addAiChar(self.AI_Character[id])
        AIbehaviors = self.AI_Character[id].getAiBehaviors()
        AIbehaviors.wander(5, 0, 300, 0.8)

    # AI 追踪
    def AI_seek(self,id, enemy_np):
        self.AI_Character[id] = AICharacter(str(id), enemy_np, 100, 0.05, 5)
        self.AIworld.addAiChar(self.AI_Character[id])
        AIbehaviors = self.AI_Character[id].getAiBehaviors()
        AIbehaviors.pursue(self.actorNP)

    # AI 帧更新
    def AIUpdate(self,task):
        if self.__amount > 0:
            for id in range(self.__amount):
                if self.__isDead[id] != True:
                    if self.isDanger(id):
                        AIbehaviors = self.AI_Character[id].getAiBehaviors()
                        AIbehaviors.removeAi("all")
                        AIbehaviors.pursue(self.actorNP)
                    else:
                        AIbehaviors = self.AI_Character[id].getAiBehaviors()
                        AIbehaviors.removeAi("all")
                        AIbehaviors.wander(5, 0, 10, 1)
                    self.AIworld.update()
        return task.cont

    # 所有攻击的碰撞检测
    def all_collide_result(self):
        for id in range(self.__amount):
            self.result = self.world.contactTest(self.__enemy_NP[id].node())
            for contact in self.result.getContacts():
                if type(contact.getNode1()) != type(self.actor_character_Node):
                    if contact.getNode1().isStatic() == False and contact.getNode1().getMass() == 10.0:
                        print "人物所有的碰撞结果：%s" % self.result.getNumContacts()
                        print "wifi 受到了攻击"
                        print "%s%s 发生了碰撞" % (contact.getNode0(), contact.getNode1())
                        roleId = self.sceneMgr.get_resId(self.__enemy_list[id])
                        print "role id is : "
                        self.roleMgr.calc_attack("PlayerRole", self.__role_dict[roleId].get_attr_value("roleId"))
                        print "怪物血量:%s" %self.__role_dict[roleId].get_attr_value("hp")
            # todo 血量计算

    # AI 的距离判断
    def isDanger(self,id):
        relativePos = self.actorNP.getPos(self.__enemy_NP[id])
        relativePos.setZ(0)
        length = self.math_helper.get_length(relativePos)
        # print "他们的距离是: ",length
        if relativePos.length() < DANGER_LENGTH:
            return True
        else:
            return False
        pass

    """""""""""""""
    输入监听
    """""""""""""""
    # 输入初始化
    def init_input(self):
        # self.accept('escape', self.doExit)
        self.accept('f1', self.base.toggleWireframe)
        self.accept('f2', self.base.toggleTexture)
        self.accept('f3', self.toggleDebug)
        self.accept('f5', self.doScreenshot)

        # 事件管理
        # self.accept('space', self.doJump)
        self.accept('mouse1',self.doShoot)
        # self.accept('control', self.doCrouch)
        self.accept('5',self.getCurrentPos)
        self.accept('6',self.all_collide_result)

        inputState.watchWithModifiers('back', 's')
        inputState.watchWithModifiers('forward', 'w')
        inputState.watchWithModifiers('turnLeft', 'a')
        inputState.watchWithModifiers('turnRight', 'd')

    def cam_control(self,isFixed,pos=Point3(0,0,0),hpr=Vec3(0,0,0),lookAt=Point3(0,0,0)):
        camCtrlr = CameraController()
        camCtrlr.bind_ShowBase(self.base)
        camCtrlr.set_clock(globalClock)
        if isFixed == False:
            camCtrlr.focus_on(self.actor_hunter, 100)
            camCtrlr.set_rotateSpeed(10)
            camCtrlr.add_toggle_to_opt("u", "rotate_around_up")
            camCtrlr.add_toggle_to_opt("j", "rotate_around_down")
            camCtrlr.add_toggle_to_opt("h", "rotate_around_cw")
            camCtrlr.add_toggle_to_opt("k", "rotate_around_ccw")
        else:
            camCtrlr.fix_on(pos,hpr,lookAt)

        allChildren = self.base.render.getChildren()
        print  "相机创建后：", allChildren
        print "相机位置: ",pos

        self.sceneMgr.bind_CameraController(camCtrlr)
        self.sceneMgr.get_ActorMgr().bind_CameraController(camCtrlr)

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
        self.base.screenshot('Bullet')

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
        self.stop_update()
        self.ignore('mouse1')
        self.world = None
        self.worldNP.removeNode()


    def doShoot(self):
        # 子弹枪声
        print "子弹枪声: ",self.actorRole.get_attr_value("currWeapon")
        bullet_sound_id = self.actorRole.get_attr_value("currWeapon") + 3
        self.resMgr.play_sound(bullet_sound_id)

        pFrom = Point3(0, 0, 0)
        pTo = Point3()
        print "omega"
        omega = self.actorNP.getHpr().getX()
        print omega
        omega = (omega - 90)%360
        v = Point3(math.cos(omega * math.pi / 180), math.sin(omega * math.pi / 180),0)
        v.normalize()
        v *= BULLET_SPEED
        #create Bullet
        size = Vec3(7,7,7)
        pFrom = self.actorNP.getPos()
        x = self.actorNP.getPos().getX()
        y = self.actorNP.getPos().getY()
        z = self.actorNP.getPos().getZ()
        hpr = self.actorNP.getHpr()
        cosOmg = 18*math.cos(omega*math.pi/180)
        sinOmg = 18*math.sin(omega*math.pi/180)
        bulletNP = self.create_bullet('Bullet', BULLET_SIZE, Point3(x + cosOmg, y + sinOmg, 15), True)
        bulletNP.setHpr(self.actorNP,Vec3(0,0,0))
        bulletNP.node().setLinearVelocity(v)
        self.world.attachRigidBody(bulletNP.node())
        bulletNP.setCollideMask(BitMask32.allOff())
        print '子弹方向hpr %s' % v
        print '子弹位置 %s' %bulletNP.getPos()



        # Remove the bullet again after 1 sec
        taskMgr.doMethodLater(1,self.doRemove,'doRemove',
                            extraArgs=[bulletNP],
                            appendTask=True)

    def create_bullet(self, name, size, pos, isCCD):
        shape = BulletBoxShape(size)
        body = BulletRigidBodyNode(name)
        bodyNP = self.worldNP.attachNewNode(body)
        bodyNP.node().addShape(shape)
        bodyNP.node().setMass(BULLET_MASS)
        bodyNP.setPos(pos)
        bodyNP.setCollideMask(BitMask32.allOn())
        self.bullet_model.reparentTo(bodyNP)
        self.bullet_model.setHpr(bodyNP,Vec3(-90,0,-90))

        if isCCD:
            bodyNP.node().setCcdMotionThreshold(1e-7);
            bodyNP.node().setCcdSweptSphereRadius(0.50);
        return bodyNP

    def doRemove(self,bulletNP,task):
        self.world.removeRigidBody(bulletNP.node())
        return task.done

    """""""""""""""
    帧更新
    """""""""""""""
    def task_update(self):
        taskMgr.add(self.sceneMgr.update_scene, "update_scene")
        taskMgr.add(self.update, 'updateWorld')
        taskMgr.add(self.AIUpdate, 'AIUpdate')

    # 设置界面暂停帧更新
    def stop_update(self):
        taskMgr.remove('update_scene')
        taskMgr.remove('updateWorld')
        taskMgr.remove('AIUpdate')
        tasks = taskMgr.getAllTasks()
        print tasks

    #设置界面结束，恢复帧更新
    def reset_update(self):
        taskMgr.add(self.sceneMgr.update_scene, "update_scene")
        taskMgr.add(self.update, 'updateWorld')
        taskMgr.add(self.AIUpdate, 'AIUpdate')

    def update(self, task):
        dt = globalClock.getDt()
        self.processInput(dt)
        self.world.doPhysics(dt,4,1./240.)
        self.all_collide_result()
        self.death_detect()
        return task.cont

    def death_detect(self):
        #enemies = self.roleMgr.get_one_kind_of_roles("EnemyRole")
        for id in range(self.__amount):
            roleId = self.sceneMgr.get_resId(self.__enemy_list[id])
            if self.__role_dict[roleId].get_attr_value("hp") == 0:
                # 碰撞体移除
                self.__enemy_NP[id].setCollideMask(BitMask32.allOff())
                # AI 不更新
                self.__isDead[id] = True
                self.AI_Character[id].getAiBehaviors().removeAi("all")

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

