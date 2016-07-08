# -*- coding:utf-8 -*-

import copy

from res_manager import ResManager
from RoleModule.role_manager import RoleManager
from ArchiveModule.archive_package import ArchivePackage
import SeriousTools.SeriousTools as SeriousTools
from SeriousTools.effert_msg_dispatcher import EffertMsgDispatcher

from direct.actor.Actor import Actor
from direct.interval.ActorInterval import ActorInterval
from direct.showbase.MessengerGlobal import messenger
from direct.interval.FunctionInterval import *
from direct.interval.Interval import *
from direct.interval.IntervalGlobal import *
from pandac.PandaModules import TransparencyAttrib
from panda3d.core import *

import math

# 角色行为常量
ACTOR_MOVE_FORWARD  = "actor_move_forward"
ACTOR_MOVE_BACKWARD = "actor_move_backward"
ACTOR_MOVE_LEFT     = "actor_move_left"
ACTOR_MOVE_RIGHT    = "actor_move_right"
ACTOR_ROTATE_CW     = "actor_rotate_cw"
ACTOR_ROTATE_CCW    = "actor_rotate_ccw"
ACTOR_ATTACK        = "actor_attack"
ACTOR_BE_ATTACKED   = "actor_be_attacked"
ACTOR_TALK          = "actor_talk"

# 角色事件常量
FIND_ENEMY      = "find_enemy"
FIND_NPC        = "find_npc"
FIND_ATTACHMENT = "find_attachment"
FIND_NOTHING    = "find_nothing"

ACTOR_EFFERT = [
    ACTOR_MOVE_FORWARD,
    ACTOR_MOVE_BACKWARD,
    ACTOR_MOVE_LEFT,
    ACTOR_MOVE_RIGHT,
    ACTOR_ROTATE_CW,
    ACTOR_ROTATE_CCW,
    ACTOR_ATTACK,
    ACTOR_BE_ATTACKED,
    ACTOR_TALK,
]

class ActorManager(ResManager):

    def __init__(self, resType = "actor"):

        ResManager.__init__(self, resType)

        self.__itvlMap = dict()

        self.__actorMoveSpeed = 0
        self.__actorRotateSpeed = 0

        self.__roleMgr = None

        self.__clock = None

        self.__playerMovingState = dict()

        self.__attackLock = False

        self.__NPCCanTalkWith = None

        self.isPlayerMoving = False

        self.__effertSwitch = {
            ACTOR_MOVE_FORWARD  : False,
            ACTOR_MOVE_BACKWARD : False,
            ACTOR_MOVE_LEFT     : False,
            ACTOR_MOVE_RIGHT    : False,
            ACTOR_ROTATE_CW     : False,
            ACTOR_ROTATE_CCW    : False,
            ACTOR_ATTACK        : False,
            ACTOR_BE_ATTACKED   : False,
            ACTOR_TALK          : False,
        }

        self.__toggleEffert = {
            ACTOR_MOVE_FORWARD  : self.__actor_move_forward,
            ACTOR_MOVE_BACKWARD : self.__actor_move_backward,
            ACTOR_MOVE_LEFT     : self.__actor_move_left,
            ACTOR_MOVE_RIGHT    : self.__actor_move_right,
            ACTOR_ROTATE_CW     : self.__actor_rotate_cw,
            ACTOR_ROTATE_CCW    : self.__actor_rotate_ccw,
            ACTOR_ATTACK        : self.__actor_attack,
            ACTOR_BE_ATTACKED   : self.__actor_be_attacked,
            ACTOR_TALK          : self.__actor_talk,
        }

        self.__enemyCanAttack = dict()

        self.__eventActionRecord = dict() # actorId : [ toggleEvent, actionName ]
        self.__eventEffertRecord = dict() # actorId : [ toggleEvent, effert ]

        self.__camCurrH = None

        self.__N  = 0
        self.__NE = 45
        self.__E  = 90
        self.__ES = 135
        self.__S  = 180
        self.__SW = 225
        self.__W  = 270
        self.__WN = 315
        self.__directionsVector = None

        self.__playerMovingForward = False
        self.__playerMovingBackward = False

        self.__effertMsgDiptcr = EffertMsgDispatcher()

        self.__arcPkg = ArchivePackage(arcPkgName = "actor",
                                       itemsName = [
                                           "actorId",
                                           "actorPath",
                                           "actionsPath",
                                           "pos",
                                           "hpr",
                                           "scale",
                                           "parentId"
                                       ])
        self.__arcPkg.append_metaData(key = "toggleEvent")
        self.__arcPkg.append_metaData(key = "eventActionRecord")
        self.__arcPkg.append_metaData(key = "eventEffertRecord")

    """""""""""""""
    动态模型管理函数
    """""""""""""""

    # 加载动态模型
    def load_res(self,
                 resPath,
                 extraResPath,
                 _resId = None):

        #print "In load_res : ", resPath, extraResPath

        res = Actor(resPath, extraResPath)
        print "in load_res :", res
        resId = None

        self._resCount += 1

        if _resId == None:

            resId = self._gen_resId()

        else:

            resId = _resId

        self._resMap[resId] = res
        self._resPath[resId] = [resPath, extraResPath]

        self.__itvlMap[resId] = self.__gen_interval_for_actor(res)

        return res

    def delete_actor(self, actorId):

        pass

    #########################################

    """""""""""""""""
    模型动作触发处理函数
    """""""""""""""""

    # 为Actor的某个动作添加触发事件
    def add_toggle_to_actor(self,
                            toggleEvent,
                            actorOrId,
                            actionName,
                            ):

        if isinstance(actorOrId, str):

            actorId = actorOrId

            actor = self.get_res(actorId)

            if actor is not None:

                if actionName in actor.getAnimNames():

                    itvl = self.__get_actor_interval(actorId, actionName)

                    actor.accept(event=toggleEvent,
                                 method=self.__move_interval_loop,
                                 extraArgs=[actor, toggleEvent, itvl])

                    # actor.accept(event=toggleEvent + "-repeat",
                    #              method=self.__move_interval_loop,
                    #              extraArgs=[actor, toggleEvent, itvl])

                    actor.accept(event=toggleEvent + "-up",
                                 method=self.__move_interval_stop,
                                 extraArgs=[actor, toggleEvent, itvl])

                    if self.__eventActionRecord.has_key(actorId) is False:

                        self.__eventActionRecord[actorId] = dict()

                    self.__eventActionRecord[actorId][toggleEvent] = actionName

        elif isinstance(actorOrId, Actor):

            actor = actorOrId

            actorId = self.get_resId(actor)

            if actorId is not None:

                if actionName in actor.getAnimNames():

                    itvl = self.__get_actor_interval(actorId, actionName)

                    actor.accept(event=toggleEvent,
                                 method=self.__move_interval_loop,
                                 extraArgs=[actor, toggleEvent, itvl])

                    # actor.accept(event=toggleEvent + "-repeat",
                    #              method=self.__move_interval_loop,
                    #              extraArgs=[actor, toggleEvent, itvl])

                    actor.accept(event=toggleEvent + "-up",
                                 method=self.__move_interval_stop,
                                 extraArgs=[actor, toggleEvent, itvl])

                    if self.__eventActionRecord.has_key(actorId) is False:

                        self.__eventActionRecord[actorId] = dict()

                    self.__eventActionRecord[actorId][toggleEvent] = actionName

    #########################################

    def __actor_keep_moving(self, isMoving):

        self.isPlayerMoving = isMoving

    def __move_interval_start(self, actor, toggleEvent, itvl):

        if len(actor.getAnimControls()) == 0:

            itvl.start()

    # 循环Interval
    def __move_interval_loop(self, actor, toggleEvent, itvl):

        if itvl.animName == "run_forward":

            self.__playerMovingForward = True

        if itvl.animName == "run_backward":

            self.__playerMovingBackward = True

        if len(actor.getAnimControls()) == 0:

            itvl.loop()

    #########################################

    # 停止Interval
    def __move_interval_stop(self, actor, toggleEvent, itvl):

        if itvl.animName == "run_forward":
            self.__playerMovingForward = False

        if itvl.animName == "run_backward":
            self.__playerMovingBackward = False

        currFrame = itvl.getCurrentFrame()
        endFrame = actor.getNumFrames(itvl.animName)

        itvl.finish()

        standItvl = ActorInterval(actor, "stand")
        standItvl.start()

    #########################################

    def actor_attack_effert(self, event, actorId):

        actor = self.get_actor(actorId)

        actor.accept(event, self.__actor_attack_interval_play, [actorId])

        #actor.accept(event + "-repeat", self.__actor_attack_interval_loop, [actorId])

        actor.accept(event + "-up", self.__actor_attack_interval_stop, [actorId])

    def __actor_attack_interval_stop(self, actorId):

        self.__attackLock = False

        actor = self.get_actor(actorId)

        attackItvl = self.__itvlMap[actorId]["attack"]

        effertDict = self.__eventEffertRecord[actorId]

        for toggleEvent, effertList in effertDict.iteritems():

            for effert in effertList:

                if effert[0] == "actor_move_forward" and self.__playerMovingForward is True:
                    self.__turn_effert_switch(actorId, toggleEvent, "actor_move_forward", True)

                if effert[0] == "actor_move_backward" and self.__playerMovingBackward is True:
                    self.__turn_effert_switch(actorId, toggleEvent, "actor_move_backward", True)

    def __actor_attack_interval_play(self, actorId):

        self.__attackLock = True

        actor = self.get_actor(actorId)

        attackItvl = self.__itvlMap[actorId]["attack"]

        effertDict = self.__eventEffertRecord[actorId]

        for toggleEvent, effertList in effertDict.iteritems():

            for effert in effertList:

                if effert[0] == "actor_move_forward" and self.__playerMovingForward is True:

                    self.__turn_effert_switch(actorId, toggleEvent, "actor_move_forward", False)


                if effert[0] == "actor_move_backward" and self.__playerMovingBackward is True:

                    self.__turn_effert_switch(actorId, toggleEvent, "actor_move_backward", False)

        attackItvl.start()

    #########################################

    def enemy_die_interval_play(self, actorId):

        enemy = self.get_actor(actorId)

        enemy.setTransparency(TransparencyAttrib.MAlpha)

        colorItvl = LerpColorInterval(
            nodePath = enemy,
            duration = 2,
            color = (0)
        )

        colorItvl2 = LerpColorInterval(
            nodePath = enemy,
            duration = 0.1,
            color = (1)
        )

        colorSeq = Sequence(
            colorItvl,
            FunctionInterval(self.__actor_hide, extraArgs = [enemy]),
            Wait(120),
            FunctionInterval(self.__actor_show, extraArgs = [enemy]),
            colorItvl2
        )

        colorSeq.start()

    def __actor_show(self, actor):

        actor.show()

    def __actor_hide(self, actor):

        actor.hide()

    #########################################

    # 为每个Actor的每个动作生成ActorInterval
    def __gen_interval_for_actor(self, actor):

        actionItvlMap = {}

        for actionName in actor.getAnimNames():

            actor.actorInterval(animName=actionName)

            tmpItvl = ActorInterval(actor = actor,
                                    animName = actionName)

            actionItvlMap[actionName] = tmpItvl

        return actionItvlMap

    #########################################

    def __get_actor_interval(self, actorId, actionName):

        actionItvlMap = SeriousTools.find_value_in_dict(actorId, self.__itvlMap)

        if actionItvlMap is not None and \
            actionName in actionItvlMap.keys():

            return actionItvlMap[actionName]

        return None

    #########################################

    def add_effert_to_actor(self,
                            toggleEvent,
                            actorId,
                            effert,
                            extraArgs = None):

        actor = self.get_actor(actorId)
        #print "in add_effert_to_actor : ", actor

        if actor is not None and effert in ACTOR_EFFERT:

            #print "Ok, add_effert execute"

            self.__effertMsgDiptcr.accept_msg(toggleEvent)
            #self.__effertMsgDiptcr.accept_msg(toggleEvent+"up")

            actor.accept(toggleEvent + "_effert",
                         self.__turn_effert_switch,
                         [actorId, toggleEvent, effert, True])
            actor.accept(toggleEvent + "_effert_end",
                         self.__turn_effert_switch,
                         [actorId, toggleEvent, effert, False])

            #print self.__toggleEffert[effert]

            if self.__eventEffertRecord.has_key(actorId) is False:

                self.__eventEffertRecord[actorId] = dict()

            if self.__eventEffertRecord[actorId].has_key(toggleEvent) is False:

                self.__eventEffertRecord[actorId][toggleEvent] = list()

            if self.__eventEffertRecord[actorId][toggleEvent].count([effert, False]) == 0 and \
                self.__eventEffertRecord[actorId][toggleEvent].count([effert, True]) == 0:

                self.__eventEffertRecord[actorId][toggleEvent].append([effert, False])

    #########################################

    def __turn_effert_switch(self, actorId, toggleEvent, effert, onOrOff):

        #print "turn '", effert, "' ", onOrOff

        for i in range(len(self.__eventEffertRecord[actorId][toggleEvent])):

            if effert == self.__eventEffertRecord[actorId][toggleEvent][i][0]:

                self.__eventEffertRecord[actorId][toggleEvent][i][1] = onOrOff

    #########################################

    """""""""""""""""""""""""""""""""""
    预设角色所做动作所产生的在场景或属性中的变化,
    如人物角色"奔跑"的动作，会导致人物角色在场景中
    位置的变化，受到攻击则血量减少，更换武器攻击力
    和攻击速度变化等等
    """""""""""""""""""""""""""""""""""

    def update_actors(self, task):

        #task.setTaskChain("actorTaskChain")

        self.__directionsVector = self.__camCtrlr.get_directionsVector()
        self.__update_actor_direction()

        player = self.__roleMgr.get_role("PlayerRole")

        self.__actorMoveSpeed = player.get_attr_value("runSpeed")
        self.__actorRotateSpeed = player.get_attr_value("rotateSpeed")

        for actorId, records in self.__eventEffertRecord.iteritems():

            actor = self.get_actor(actorId)

            for toggleEvent, effertList in records.iteritems():

                for effert in effertList:

                    if effert[1] == True:
                        #print actorId, ", ", toggleEvent, ", ", effert[0], ", ", effert[1]
                        execTask = self.__toggleEffert[effert[0]]
                        execTask(actor, task)

        self.__check_player_touch_area(task)

        for enemyId, able in self.__enemyCanAttack.iteritems():

            self.__enemy_attack_player(enemyId, task)

        return task.cont

    def __update_actor_direction(self):

        x = self.__directionsVector["N"].getX()
        y = self.__directionsVector["N"].getY()

        # f = open("ActorDirections.txt", "w")
        #
        # f.write(str(self.__directionsVector["N"]) + "\n")

        self.__N  = self.__camCtrlr.get_camToCtrl().getH()
        self.__NE = self.__N + 45
        self.__E  = self.__N + 90
        self.__ES = self.__N + 135
        self.__S  = self.__N + 180
        self.__SW = self.__N + 225
        self.__W  = self.__N + 270
        self.__WN = self.__N + 315

        # f.write(str(self.__N))
        # f.close()

    #########################################

    def bind_RoleManager(self, roleMgr):

        self.__roleMgr = roleMgr

    def get_roleMgr(self):

        return self.__roleMgr

    def bind_CameraController(self, camCtrlr):

        self.__camCtrlr = camCtrlr

    def get_camCtrlr(self):

        return self.__camCtrlr

    #########################################

    def __actor_move_forward(self, actor, task):

        dt = self.__clock.getDt()

        c = math.cos(actor.getH() * math.pi / 180 - math.pi / 2)
        s = math.sin(actor.getH() * math.pi / 180 - math.pi / 2)

        actor.setX(actor.getX() + c * dt * self.__actorMoveSpeed)
        actor.setY(actor.getY() + s * dt * self.__actorMoveSpeed)

        #actor.setH(actorH)

        #actor.setPos(actor.getPos() + dVector * self.__actorMoveSpeed * dt)

        #print actor, "currY : ", actor.getY()

        return task.cont

        #########################################

    def __actor_move_left(self, actor, task):

        return task.cont


    #########################################

    def __actor_move_backward(self, actor, task):

        dt = self.__clock.getDt()

        c = math.cos(actor.getH() * math.pi / 180 - math.pi / 2)
        s = math.sin(actor.getH() * math.pi / 180 - math.pi / 2)

        actor.setX(actor.getX() - c * dt * self.__actorMoveSpeed)
        actor.setY(actor.getY() - s * dt * self.__actorMoveSpeed)

        return task.cont

    #########################################

    def __actor_move_right(self, actor, task):

        return task.cont

    #########################################

    # 角色顺时针旋转
    def __actor_rotate_cw(self, actor, task):

        dt = self.__clock.getDt()

        actorH = actor.getH() + self.__actorRotateSpeed * dt

        if actorH > 360.0:

            actorH -= 360.0

        elif actorH < -360.0:

            actorH += 360.0

        actor.setH(actorH)
        #print "the actor rotate cw : ", actor.getH()
        return task.cont

    # 角色逆时针旋转
    def __actor_rotate_ccw(self, actor, task):

        dt = self.__clock.getDt()

        actorH = actor.getH() - self.__actorRotateSpeed * dt

        if actorH > 360.0:

            actorH -= 360.0

        elif actorH < -360.0:

            actorH += 360.0

        actor.setH(actorH)

        #print "the actor rotate ccw : ", actor.getH()
        return task.cont

    #########################################

    #########################################

    def __actor_attack(self, args, task):

        return task.cont

    #########################################

    def __actor_be_attacked(self, args, task):

        return task.cont

    def __actor_talk(self, args, task):

        return task.cont

    def set_enemyCanAttack(self, enemyId, able):

        self.__enemyCanAttack[enemyId] = able

    def __enemy_attack_player(self, enemyId, task):

        if self.__enemyCanAttack[enemyId] is True:

            enemy = self.get_actor(enemyId)

            self.__enemy_face_to_player(enemy, task)
            self.__enemy_move_to_player(enemy, task)

        return task.cont

    def __enemy_face_to_player(self, enemy, task):

        player = self.get_actor(self.__roleMgr.get_role_model("PlayerRole"))

        playerPos = player.getPos()
        enemyPos = enemy.getPos()

        playerPos.setZ(0)
        enemyPos.setZ(0)

        # v = enemyPos - playerPos
        # v.normalize()
        #
        # enemy.setHpr(-v)

        v1 = enemyPos - LPoint3f(0, 0, 0)
        v2 = enemyPos - playerPos

        v1.normalize()
        v2.normalize()

        a = math.acos(v1.getX())
        b = math.acos(v2.getX())

        if v1.getY() < 0:

            a = 2 * math.pi - a

        if v2.getY() < 0:

            b = 2 * math.pi - b

        a = a * 180 / math.pi
        b = b * 180 / math.pi

        print a, ", ", b

        enemy.setH(b - 90)

        return task.cont

    def __enemy_move_to_player(self, enemy, task):

        player = self.get_actor(self.__roleMgr.get_role_model("PlayerRole"))

        enemyId = self.get_resId(enemy)
        enemyRole = self.__roleMgr.get_role_by_model(enemyId)

        playerPos = player.getPos()
        enemyPos = enemy.getPos()

        playerPos.setZ(0)
        enemyPos.setZ(0)

        v = playerPos - enemyPos

        if v.length() > enemyRole.get_attr_value("attackRange"):

            if enemyRole.get_attr_value("currState") == "attacking":

                messenger.send("enemy_attack-up")

                enemyRole.set_attr_value("currState", "closing")

                messenger.send("enemy_run")

            enemyRunSpeed = enemyRole.get_attr_value("runSpeed") * 1.5

            dt = self.__clock.getDt()

            c = math.cos(enemy.getH() * math.pi / 180 - math.pi / 2)
            s = math.sin(enemy.getH() * math.pi / 180 - math.pi / 2)

            enemy.setX(enemy.getX() + c * dt * enemyRunSpeed)
            enemy.setY(enemy.getY() + s * dt * enemyRunSpeed)

        else:

            if enemyRole.get_attr_value("currState") == "closing":

                enemyRole.set_attr_value("currState", "attacking")

                messenger.send("enemy_run-up")
                messenger.send("enemy_attack")

        return task.cont

    # 监测玩家角色可触碰区域内的其他角色, 监测到的不同事件具有不同优先级
    # 优先级1：发现Enemy
    # 优先级2：发现NPC
    # 优先级3：发现Attachment
    def __check_player_touch_area(self, task):


        playerRole = self.__roleMgr.get_role("PlayerRole")

        touchRadius = playerRole.get_attr_value("touchRadius")

        player = self.get_actor(playerRole.get_attr_value("modelId"))

        playerPos = player.getPos()

        # 首先监测Enemy
        enemies = self.__roleMgr.get_one_kind_of_roles("EnemyRole")

        for enemyRole in enemies:

            enemy = self.get_actor(enemyRole.get_attr_value("modelId"))
            enemyId = self.get_resId(enemy)

            enemyPos = enemy.getPos()

            dVector = playerPos - enemyPos
            dVector.setZ(0)

            if dVector.length() <= touchRadius and enemy.isHidden() is False:

                #print "playerPos:", playerPos, " enemyPos:", enemyPos, " dVector length:", dVector.length()

                self.set_enemyCanAttack(enemyId, True)

                if enemyRole.get_attr_value("currState") == "wandering":

                    messenger.send("enemy_run")

                    enemyRole.set_attr_value("currState", "closing")

                messenger.send(FIND_ENEMY)

            else:

                self.set_enemyCanAttack(enemyId, False)

                messenger.send("enemy_run-up")

                enemyRole.set_attr_value("currState", "wandering")

                return task.cont

        # 然后监测NPC
        NPCs = self.__roleMgr.get_one_kind_of_roles("NPCRole")

        for NPCRole in NPCs:

            NPC = self.get_actor(NPCRole.get_attr_value("modelId"))

            NPCPos = NPC.getPos()

            dVector = playerPos - NPCPos
            dVector.setZ(0)

            if dVector.length() <= touchRadius:

                #print "playerPos:", playerPos, " npcPos:", NPCPos, " dVector length:", dVector.length()

                self.__NPCCanTalkWith = NPC

                messenger.send(FIND_NPC)

                return task.cont

        messenger.send(FIND_NOTHING)

        return task.cont

    #########################################

    def check_effertSwitch(self, key):

        return SeriousTools.find_value_in_dict(key, self.__effertSwitch)

    def set_clock(self, clock):

        self.__clock = clock

    def get_clock(self, clock):

        return self.__clock

    def set_actorMoveSpeed(self, speed):

        self.__actorMoveSpeed = speed

    def get_actorMoveSpeed(self):

        return self.__actorMoveSpeed

    def get_actorId(self, actor):

        return self.get_resId(actor)

    def get_actor(self, actorId):

        return self.get_res(actorId)

    def get_arcPkg(self):

        return self.__arcPkg

    def set_toggleEffert(self, toggleEffert):

        self.__toggleEffert = toggleEffert

    def get_toggleEffert(self):

        return self.__toggleEffert

    def set_eventActionRecord(self, eventActionRecord):

        self.__eventActionRecord = eventActionRecord

    def get_eventActionRecord(self):

        return self.__eventActionRecord

    def print_eventActionRecord(self):

        print "----- eventActionRecord -----"

        for actorId, record in self.__eventActionRecord.iteritems():

            print actorId

            for toggleEvent, actionName in record.iteritems():

                print "    toggleEvent = %s;  actionName = %s" % (toggleEvent, actionName)

        print "------------------------------"

    def set_eventEffertRecord(self, eventEffertRecord):

        self.__eventEffertRecord = eventEffertRecord

    def get_eventEffertRecord(self):

        return self.__eventEffertRecord

    def print_eventEffertRecord(self):

        print "----- eventEffertRecord -----"

        for actorId, record in self.__eventEffertRecord.iteritems():

            print actorId

            for toggleEvent, effertList in record.iteritems():

                print "    ", toggleEvent

                for effert in effertList:

                    print "        ", effert

        print "-------------------------"