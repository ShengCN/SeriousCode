# -*- coding:utf-8 -*-

import copy

from res_manager import ResManager
from RoleModule.role_manager import RoleManager
from ArchiveModule.archive_package import ArchivePackage
import SeriousTools.SeriousTools as SeriousTools
from SeriousTools.effert_msg_dispatcher import EffertMsgDispatcher
from ResourcesModule.resources_manager import ResourcesManager

from direct.actor.Actor import Actor
from direct.interval.ActorInterval import ActorInterval
from direct.showbase.MessengerGlobal import messenger
from direct.interval.FunctionInterval import *
from direct.interval.Interval import *
from direct.interval.IntervalGlobal import *
from pandac.PandaModules import TransparencyAttrib
from panda3d.core import *

import sys
import math
import time
import random

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
        self.__itvlState = dict()

        self.__actorMoveSpeed = 0
        self.__actorRotateSpeed = 0

        self.__storyLine = 0

        self.__roleMgr = None

        self.__clock = None

        self.__playerMovingState = dict()

        self.__attackLock = False
        self.__playerFoundChest = False

        self.__NPCCanTalkWith = None
        self.__chestCanOpen = None

        self.isPlayerMoving = False
        self.__isTalking = False

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

        self.__shouldDestroyPrompt = False

        self.__effertMsgDiptcr = EffertMsgDispatcher()

        self.__resMgr = ResourcesManager()

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
        #print "in load_res :", res
        resId = None

        self._resCount += 1

        if _resId == None:

            resId = self._gen_resId()

        else:

            resId = _resId

        self._resMap[resId] = res
        self._resPath[resId] = [resPath, extraResPath]
        self.__itvlMap[resId] = self.__gen_interval_for_actor(res)
        #self.print_all_itvl_duration()

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

                    if SeriousTools.is_device_event(toggleEvent) is False:

                        toggleEvent += "_" + actorId

                    actor.accept(event=toggleEvent,
                                 method=self.__move_interval_loop,
                                 extraArgs=[actor, toggleEvent, itvl])

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

                    if SeriousTools.is_device_event(toggleEvent) is False:

                        toggleEvent += actorId

                    actor.accept(event=toggleEvent,
                                 method=self.__move_interval_loop,
                                 extraArgs=[actor, toggleEvent, itvl])

                    actor.accept(event=toggleEvent + "-up",
                                 method=self.__move_interval_stop,
                                 extraArgs=[actor, toggleEvent, itvl])

                    if self.__eventActionRecord.has_key(actorId) is False:

                        self.__eventActionRecord[actorId] = dict()

                    self.__eventActionRecord[actorId][toggleEvent] = actionName

    def add_toggle_to_group_actors(self, toggleEvent, actorList, actionName):

        for actorId in actorList:

            self.add_toggle_to_actor(toggleEvent, actorId, actionName)

    def add_toggle_for_player_to_interact(self, toggleEvent, playerId):

        player = self.get_actor(playerId)

        player.accept(toggleEvent, self.__talk_or_open)

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

    def toggle_actor_attack(self, event, actorId):

        actor = self.get_actor(actorId)

        actor.accept(event, self.__actor_attack_interval_play, [actorId])

        #actor.accept(event + "-repeat", self.__actor_attack_interval_loop, [actorId])

        actor.accept(event + "-up", self.__actor_attack_interval_stop, [actorId])

    def __actor_attack_interval_stop(self, actorId):

        self.__attackLock = False

        actor = self.get_actor(actorId)

        attackItvl = self.__itvlMap[actorId]["attack"]

        # effertDict = self.__eventEffertRecord[actorId]
        #
        # for toggleEvent, effertList in effertDict.iteritems():
        #
        #     for effert in effertList:
        #
        #         if effert[0] == "actor_move_forward" and self.__playerMovingForward is True:
        #             self.__turn_effert_switch(actorId, toggleEvent, "actor_move_forward", True)
        #
        #         if effert[0] == "actor_move_backward" and self.__playerMovingBackward is True:
        #             self.__turn_effert_switch(actorId, toggleEvent, "actor_move_backward", True)

    def __actor_attack_interval_play(self, actorId):

        self.__attackLock = True

        actor = self.get_actor(actorId)

        attackItvl = self.__itvlMap[actorId]["attack"]

        # effertDict = self.__eventEffertRecord[actorId]
        #
        # for toggleEvent, effertList in effertDict.iteritems():
        #
        #     for effert in effertList:
        #
        #         if effert[0] == "actor_move_forward" and self.__playerMovingForward is True:
        #
        #             self.__turn_effert_switch(actorId, toggleEvent, "actor_move_forward", False)
        #
        #
        #         if effert[0] == "actor_move_backward" and self.__playerMovingBackward is True:
        #
        #             self.__turn_effert_switch(actorId, toggleEvent, "actor_move_backward", False)

        attackItvl.start()

    #########################################

    def stop_all_itvls(self):

        for actorId, itvls in self.__itvlMap.iteritems():

            if self.__itvlState.has_key(actorId) is False:

                self.__itvlState[actorId] = dict()

            for actionName, itvl in itvls.iteritems():

                if itvl.isPlaying():

                    self.__itvlState[actorId][actionName] = True

                    itvl.finish()

                else:

                    self.__itvlState[actorId][actionName] = False


    def restart_all_itvls(self):

        for actorId, stateMap in self.__itvlState.iteritems():

            for actionName, state in stateMap.iteritems():

                if state is True:

                    self.__itvlMap[actorId][actionName].loop()

    #########################################

    def __check_enemy_die(self, task):

        enemies = self.__roleMgr.get_one_kind_of_roles("EnemyRole")

        for enemyRole in enemies:

            if enemyRole.get_attr_value("hp") == 0:

                self.enemy_die_interval_play(enemyRole.get_attr_value("modelId"))

        return task.cont

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
            Wait(12000),
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

        self.__check_enemy_die(task)

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

    def bind_ResourcesManager(self, resMgr):

        self.__resMgr = resMgr

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

            #self.__enemy_face_to_player(enemy, task)
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

        #print a, ", ", b

        enemy.setH(b - 90)

        return task.cont

    def __enemy_move_to_player(self, enemy, task):

        playerRole = self.__roleMgr.get_role("PlayerRole")
        player = self.get_actor(playerRole.get_attr_value("modelId"))

        enemyId = self.get_resId(enemy)
        enemyRole = self.__roleMgr.get_role_by_model(enemyId)

        playerPos = player.getPos()
        enemyPos = enemy.getPos()

        playerPos.setZ(0)
        enemyPos.setZ(0)

        v = enemy.getPos(player)
        v.setZ(0)

        #print "v.length : ", v.length(), " attackRange : ", enemyRole.get_attr_value("attackRange")
        #print "currState : ", enemyRole.get_attr_value("currState")
        if v.length() > enemyRole.get_attr_value("attackRange"):

            if enemyRole.get_attr_value("currState") == "attacking":

                enemyRole.set_attr_value("currState", "closing")

                messenger.send("enemy_attack_" + enemyId + "-up")
                #messenger.send("enemy_walk_" + enemyId)

            # elif enemyRole.get_attr_value("currState") == "wandering":
            #
            #     #messenger.send("enemy_attack_" + enemyId + "-up")
            #     messenger.send("enemy_walk_" + enemyId)

            enemyRunSpeed = enemyRole.get_attr_value("runSpeed") * 1.5

            dt = self.__clock.getDt()

            # c = math.cos(enemy.getH() * math.pi / 180 - math.pi / 2)
            # s = math.sin(enemy.getH() * math.pi / 180 - math.pi / 2)
            #
            # enemy.setX(enemy.getX() + c * dt * enemyRunSpeed)
            # enemy.setY(enemy.getY() + s * dt * enemyRunSpeed)

            #messenger.send("player_be_attacked1-up")
            #messenger.send("player_be_attacked2-up")

        else:

            if enemyRole.get_attr_value("currState") == "closing":

                enemyRole.set_attr_value("currState", "attacking")

                messenger.send("enemy_walk_" + enemyId +"-up")
                messenger.send("enemy_attack_" + enemyId)

                # if random.randint(0, 1) == 0:
                #
                #     messenger.send("player_be_attacked1")
                #
                # else:
                #
                #     messenger.send("player_be_attacked2")

            elif enemyRole.get_attr_value("currState") == "attacking":

                cd = enemyRole.get_attr_value("cd")
                remainCd = enemyRole.get_attr_value("remainCd")
                #print "player cd : ", cd, ", remainCd : ", remainCd
                if remainCd == cd:

                    enemyRole.set_attr_value("remainCd", remainCd - self.__clock.getDt())

                    actorState = self.__roleMgr.calc_attack(enemyRole.get_attr_value("roleId"), "PlayerRole")

                    #print "player hp : ", playerRole.get_attr_value("hp")

                    if actorState[1] == "die":

                        messenger.send("player_die")

                else:

                    remainCd = max(remainCd - self.__clock.getDt(), 0)

                    if remainCd == 0:

                        remainCd = cd

                    enemyRole.set_attr_value("remainCd", remainCd)

        return task.cont

    def __talk_or_open(self):

        playerRole = self.__roleMgr.get_role("PlayerRole")

        # 与NPC对话
        if self.__NPCCanTalkWith is not None:

            NPCId = self.get_actorId(self.__NPCCanTalkWith)

            NPCRole = self.__roleMgr.get_role_by_model(NPCId)

            NPCName = NPCRole.get_attr_value("characterName")

            if NPCName == "nun":

                if (self.__storyLine == 1 or self.__storyLine == 4) and self.__isTalking is True:

                    self.__isTalking = self.__resMgr.dialog_next()

                if self.__storyLine == 0 or self.__storyLine == 3:

                    self.__storyLine += 1
                    playerRole.set_attr_value(key = "storyLine", value = self.__storyLine)

                    self.__resMgr.show_dialog(self.__storyLine)

                    self.__isTalking = True

            elif NPCName == "girl":

                if (self.__storyLine == 2 or self.__storyLine == 6) and self.__isTalking is True:

                    self.__isTalking = self.__resMgr.dialog_next()

                if self.__storyLine == 1 or self.__storyLine == 5:

                    self.__storyLine += 1

                    playerRole.set_attr_value(key="storyLine", value=self.__storyLine)

                    self.__resMgr.show_dialog(self.__storyLine)

                    self.__isTalking = True

            elif NPCName == "stealer":

                if self.__isTalking is True:

                    self.__isTalking = self.__resMgr.dialog_next()

                else:

                    self.__storyLine = 8

                    self.__resMgr.show_dialog(8)

                    self.__isTalking = True

            return

        if self.__storyLine == 2 or self.__isTalking is True:

            if self.__storyLine == 3 and self.__isTalking is True:

                self.__isTalking = self.__resMgr.dialog_next()

            if self.__storyLine == 2:

                self.__storyLine += 1

                playerRole.set_attr_value(key="storyLine", value=self.__storyLine)

                self.__resMgr.show_dialog(self.__storyLine)

                self.__isTalking = True

        if self.__storyLine == 4 or self.__isTalking is True:

            if self.__storyLine == 5 and self.__isTalking is True:
                self.__isTalking = self.__resMgr.dialog_next()

            if self.__storyLine == 4:
                self.__storyLine += 1

                playerRole.set_attr_value(key="storyLine", value=self.__storyLine)

                self.__resMgr.show_dialog(self.__storyLine)

                self.__isTalking = True

        if self.__storyLine == 6 or self.__isTalking is True:

            if self.__storyLine == 7 and self.__isTalking is True:

                self.__isTalking = self.__resMgr.dialog_next()

            if self.__storyLine == 6:

                self.__storyLine += 1

                playerRole.set_attr_value(key="storyLine", value=self.__storyLine)

                self.__resMgr.show_dialog(self.__storyLine)

                self.__isTalking = True

        # 打开宝箱
        if self.__chestCanOpen is not None:

            self.__shouldDestroyPrompt = False

            chestId = self.get_actorId(self.__chestCanOpen)

            chestRole = self.__roleMgr.get_role_by_model(chestId)

            if chestRole.get_attr_value("opened") is False:

                self.__chestCanOpen.play("open")

                money = random.randint(40, 60)

                self.__resMgr.destroy_prompt()
                self.__resMgr.show_prompt_box("获得" + str(money) + "金币")

                self.__roleMgr.obtain_money(money)

                self.__shouldDestroyPrompt = False

                #print self.__roleMgr.get_role("PlayerRole").get_attr_value("money")

                chestRole.set_attr_value(key="opened", value=True)

    # 监测玩家角色可触碰区域内的其他角色, 监测到的不同事件具有不同优先级
    # 优先级1：发现Enemy
    # 优先级2：发现NPC
    # 优先级3：发现Attachment
    def __check_player_touch_area(self, task):

        minDist = sys.maxint

        playerRole = self.__roleMgr.get_role("PlayerRole")

        touchRadius = playerRole.get_attr_value("touchRadius")

        player = self.get_actor(playerRole.get_attr_value("modelId"))

        playerPos = player.getPos()

        # 首先监测Enemy
        enemies = self.__roleMgr.get_one_kind_of_roles("EnemyRole")

        enemyFoundPlayer = False

        for enemyRole in enemies:

            enemy = self.get_actor(enemyRole.get_attr_value("modelId"))
            enemyId = self.get_resId(enemy)

            enemyPos = enemy.getPos()

            dVector = enemy.getPos(player)
            dVector.setZ(0)

            if self.__itvlMap[enemyId]["walk"].isPlaying() is False and \
                self.__itvlMap[enemyId]["attack"].isPlaying() is False :

                messenger.send("enemy_walk_" + enemyId)

            if dVector.length() <= touchRadius and enemy.isHidden() is False:

                #print "playerPos:", playerPos, " enemyPos:", enemyPos, " dVector length:", dVector.length()

                self.set_enemyCanAttack(enemyId, True)

                if enemyRole.get_attr_value("currState") == "wandering":

                    #messenger.send("enemy_walk_" + enemyId)

                    enemyRole.set_attr_value("currState", "closing")

                messenger.send(FIND_ENEMY)

                enemyFoundPlayer = True

            else:

                self.set_enemyCanAttack(enemyId, False)

                #messenger.send("enemy_walk_" + enemyId + "-up")

                enemyRole.set_attr_value("currState", "wandering")

        if enemyFoundPlayer is True:

            self.__resMgr.destroy_prompt()

            self.__NPCCanTalkWith = None
            self.__chestCanOpen = None

            return task.cont

        else:

            self.__shouldDestroyPrompt = False

        # 然后监测NPC
        NPCs = self.__roleMgr.get_one_kind_of_roles("NPCRole")

        playerFoundNPC = False

        for NPCRole in NPCs:

            NPC = self.get_actor(NPCRole.get_attr_value("modelId"))

            NPCPos = NPC.getPos()

            dVector = NPC.getPos(player)
            dVector.setZ(0)

            if dVector.length() <= minDist and dVector.length() <= touchRadius:

                minDist = dVector.length()

                self.__resMgr.show_prompt_box("发现NPC")

                self.__NPCCanTalkWith = NPC

                self.__shouldDestroyPrompt = True

                playerFoundNPC = True

                messenger.send(FIND_NPC)

            # else:
            #
            #     if self.__shouldDestroyPrompt is True:
            #
            #         self.__resMgr.destroy_prompt()

        if playerFoundNPC is False:

            self.__NPCCanTalkWith = None

        else:

            self.__shouldDestroyPrompt = False

            return task.cont

        chests = self.__roleMgr.get_one_kind_of_roles("AttachmentRole")



        for chest in chests:

            chestTouchRadius = chest.get_attr_value("touchRadius")

            _chest = self.get_actor(chest.get_attr_value("modelId"))

            chestPos = _chest.getPos()

            dVector = _chest.getPos(player)
            dVector.setZ(0)

            if dVector.length() <= chestTouchRadius:

                if chest.get_attr_value("opened") is False:

                    self.__resMgr.show_prompt_box("发现宝箱")

                    self.__playerFoundChest = True

                    self.__shouldDestroyPrompt = False

                    self.__chestCanOpen = _chest

                    return task.cont

            elif dVector.length() > chestTouchRadius:

                self.__playerFoundChest = False

        if self.__playerFoundChest is False:

            self.__shouldDestroyPrompt = True

            self.__chestCanOpen = None

            self.__resMgr.destroy_prompt()

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

    def get_itvlMap(self):

        return self.__itvlMap

    def set_storyLine(self, storyLine):

        self.__storyLine = storyLine

    def get_storyLine(self):

        return self.__storyLine

    def print_eventEffertRecord(self):

        print "----- eventEffertRecord -----"

        for actorId, record in self.__eventEffertRecord.iteritems():

            print actorId

            for toggleEvent, effertList in record.iteritems():

                print "    ", toggleEvent

                for effert in effertList:

                    print "        ", effert

        print "-------------------------"

    def print_all_itvl_duration(self):

        print "----- all itvl duration -----"

        for actorId, itvlDict in self.__itvlMap.iteritems():

            print actorId, " : "

            for itvl in itvlDict.values():

                print "    ", itvl.animName, " : ", itvl.getDuration()

        print "-------------------------"