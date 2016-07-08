# -*- coding:utf-8 -*-

from player_role import PlayerRole
from enemy_role import EnemyRole
from npc_role import NPCRole
from attachment_role import AttachmentRole
from ArchiveModule.archive_package import ArchivePackage
import SeriousTools.SeriousTools as SeriousTools

# 常量，表示角色类型
PLAYER_ROLE     = "PlayerRole"
ENEMY_ROLE      = "EnemyRole"
NPC_ROLE        = "NPCRole"
ATTACHMENT_ROLE = "AttachmentRole"

DIE            = "die"
ATTACK         = "attack"
BE_ATTACKED    = "be_attacked"
USE_OUT        = "use_out"
FULL_HP        = "full_hp"
SELL_OUT       = "sell_out"
LACK_OF_MONEY  = "lack_of_money"
BUY_MEDICINE   = "buy_medicine"
BUY_WEAPON2    = "buy_weapon2"
BUY_WEAPON3    = "buy_weapon3"
RECOVER_HP     = "recover_hp"
OBTAIN_MONEY   = "obtain_money"
CHANGE_WEAPON1 = "change_weapon1"
CHANGE_WEAPON2 = "change_weapon2"
CHANGE_WEAPON3 = "change_weapon3"

PLAYER_MAX_HP = 100

ROLE_ATTR_LIST = [
    "roleId",
    "modelId",
    "ableToTalk",
    "ableToCtrl",
    "ableToAtck",
    "states",
    "hp",
    "money",
    "attackForce",
    "walkSpeed",
    "runSpeed", # 10
    "rotateSpeed",
    "touchRadius",
    "actions",
    "currWeapon",
    "attachments",
    "attachmentType",
    "num",
    "price",
    "soild",
    "effert" # 20
]

class RoleManager(object):

    def __init__(self):

        self.__roleType = [ PLAYER_ROLE,
                            ENEMY_ROLE,
                            NPC_ROLE,
                            ATTACHMENT_ROLE ]

        self.__roleModelMap = dict()
        self.__roleMap = dict()

        self.__sceneMgr = None

        self.__playerRoleCount = 1
        self.__enemyRoleCount = 0
        self.__npcRoleCount = 0
        self.__attachmentRoleCount = 0

        self.__arcPkg = ArchivePackage(arcPkgName = "role",
                                       itemsName = ROLE_ATTR_LIST)

    def reset(self):

        self.__playerRoleCount = 1
        self.__enemyRoleCount = 0
        self.__npcRoleCount = 0
        self.__attachmentRoleCount = 0

        self.__roleModelMap = dict()
        self.__roleMap = dict()

    """""""""""
    角色创建函数
    """""""""""

    # 创建角色
    def create_role(self,
                    roleType,
                    modelId,
                    _roleId = None,
                    actions = None,
                    attachments = None,
                    attachmentType = None,
                    hp=-1,
                    num = 1):

        role = []
        roleId = None

        if roleType is self.__roleType[0]:

            playerRole = PlayerRole(modelId = modelId)

            self.__playerRoleCount += 1

            role.append(playerRole)

            if _roleId == None:

                roleId = playerRole.get_attr_value("roleId")

            else:

                roleId = _roleId

            playerRole.set_attr_value("roleId", roleId)

            self.__roleMap[roleId] = playerRole
            self.__roleModelMap[roleId] = modelId

        elif roleType is self.__roleType[1]:

            for i in range(num):

                enemyRole = EnemyRole(modelId = modelId)
                enemyRole.set_attr_value("hp", hp)

                self.__enemyRoleCount += 1

                role.append(enemyRole)

                if _roleId == None:

                    roleId = enemyRole.get_attr_value("roleId") + str(self.__enemyRoleCount)

                else:

                    roleId = _roleId

                enemyRole.set_attr_value("roleId", roleId)

                self.__roleMap[roleId] = enemyRole
                self.__roleModelMap[roleId] = modelId

                self.__sceneMgr.get_ActorMgr().set_enemyCanAttack(roleId, False)

        elif roleType is self.__roleType[2]:

            npcRole = NPCRole(modelId=modelId)

            self.__npcRoleCount += 1

            role.append(npcRole)

            if _roleId == None:

                roleId = npcRole.get_attr_value("roleId") + str(self.__npcRoleCount)

            else:

                roleId = _roleId

            npcRole.set_attr_value("roleId", roleId)

            self.__roleMap[roleId] = npcRole
            self.__roleModelMap[roleId] = modelId

        elif roleType is self.__roleType[3]:

            attachmentRole = AttachmentRole(attachmentType, modelId=modelId, num = num)

            self.__attachmentRoleCount += 1

            role.append(attachmentRole)

            if _roleId == None:

                roleId = attachmentRole.get_attr_value("roleId") + str(self.__attachmentRoleCount)

            else:

                roleId = _roleId

            attachmentRole.set_attr_value("roleId", roleId)

            self.__roleMap[roleId] = attachmentRole
            self.__roleModelMap[roleId] = modelId

            if attachmentType == "medicine":

                attachmentRole.add_effert("recoverHP", 35)

            elif attachmentType == "weapon1":

                attachmentRole.add_effert("attackForce", 10)

            elif attachmentType == "weapon2":

                attachmentRole.add_effert("attackForce", 20)

            elif attachmentType == "weapon3":

                attachmentRole.add_effert("attackForce", 30)

        if len(role) == 1:

            return role[0]

        else:

            return role

    def add_toggle_to_action(self, actorOrId, actionName):
        pass

    def bind_SceneManager(self, sceneMgr):

        self.__sceneMgr = sceneMgr

    """""""""""""""""""""
    读档存档的角色数据接口
    """""""""""""""""""""

    # 导入角色属性，用于读档
    def import_arcPkg(self, roleArcPkg):

        roleArcPkg = roleArcPkg[0]

        # 重置某些内部变量
        self.reset()

        for roleItem in roleArcPkg.get_itemsData():

            roleType = SeriousTools.extract_name_from_Id(roleItem[0])

            if roleType == "PlayerRole":

                player = self.create_role(_roleId = roleItem[0],
                                          roleType = "PlayerRole",
                                          modelId = roleItem[1])

                player.set_attr_value("ableToTalk", roleItem[2])
                player.set_attr_value("ableToCtrl", roleItem[3])
                player.set_attr_value("ableToAtck", roleItem[4])
                player.set_attr_value("states", roleItem[5])
                player.set_attr_value("hp", roleItem[6])
                player.set_attr_value("money", roleItem[7])
                player.set_attr_value("attackForce", roleItem[8])
                player.set_attr_value("walkSpeed", roleItem[9])
                player.set_attr_value("runSpeed", roleItem[10])
                player.set_attr_value("rotateSpeed", roleItem[11])
                player.set_attr_value("touchRadius", roleItem[12])
                player.set_attr_value("actions", roleItem[13])
                player.set_attr_value("currWeapon", roleItem[14])
                player.set_attr_value("attachments", roleItem[15])

            elif roleType == "EnemyRole":

                enemy = self.create_role(_roleId=roleItem[0],
                                          roleType="EnemyRole",
                                          modelId=roleItem[1])

                enemy.set_attr_value("ableToTalk", roleItem[2])
                enemy.set_attr_value("ableToCtrl", roleItem[3])
                enemy.set_attr_value("ableToAtck", roleItem[4])
                enemy.set_attr_value("states", roleItem[5])
                enemy.set_attr_value("hp", roleItem[6])
                enemy.set_attr_value("attackForce", roleItem[8])
                enemy.set_attr_value("walkSpeed", roleItem[9])
                enemy.set_attr_value("runSpeed", roleItem[10])
                enemy.set_attr_value("actions", roleItem[13])

            elif roleType == "NPCRole":

                npc = self.create_role(_roleId=roleItem[0],
                                       roleType="NPCRole",
                                       modelId=roleItem[1])

                npc.set_attr_value("ableToTalk", roleItem[2])
                npc.set_attr_value("ableToCtrl", roleItem[3])
                npc.set_attr_value("ableToAtck", roleItem[4])
                npc.set_attr_value("states", roleItem[5])
                npc.set_attr_value("actions", roleItem[13])

            elif roleType == "AttachmentRole":

                attachment = self.create_role(_roleId=roleItem[0],
                                              roleType="AttachmentRole",
                                              modelId=roleItem[1])

                attachment.set_attr_value("ableToTalk", roleItem[2])
                attachment.set_attr_value("ableToCtrl", roleItem[3])
                attachment.set_attr_value("ableToAtck", roleItem[4])
                attachment.set_attr_value("attachmentType", roleItem[16])
                attachment.set_attr_value("num", roleItem[17])
                attachment.set_attr_value("price", roleItem[18])
                attachment.set_attr_value("sold", roleItem[19])
                attachment.set_attr_value("effert", roleItem[20])

    #####################

    # 导出角色属性，用于存档
    def export_arcPkg(self):

        for roleId, role in self.__roleMap.iteritems():

            roleItem = []

            for attrName in ROLE_ATTR_LIST:

                if role.has_attr(attrName):

                    roleItem.append(role.get_attr_value(attrName))

                else:

                    roleItem.append(None)

            self.__arcPkg.add_item(roleItem)

        return self.__arcPkg

    """""""""""""""
    角色属性管理函数
    """""""""""""""

    def append_role_attr(self, roleId, key, value):

        if self.__roleMap.has_key(roleId) is True:

            self.__roleMap[roleId].append_role_value(key, value)

    #####################

    def set_attr_value(self, roleId, key, value):

        if self.__roleMap.has_key(roleId) is True:

            self.__roleMap[roleId].set_attr_value(key, value)

    """""""""""""""""""""""""""""
    角色的行为所导致的属性变化计算函数
    """""""""""""""""""""""""""""

    # 攻击计算
    def calc_attack(self, attackerId, victimId):

        attacker = self.get_role(attackerId)
        victim = self.get_role(victimId)

        attackForce = attacker.get_attr_value("attackForce")
        hp = victim.get_attr_value("hp")

        hp = max(hp - attackForce, 0)

        victim.set_attr_value("hp", hp)

        if hp == 0:

            if attackerId == "PlayerRole":

                return [ATTACK, DIE]

            else:

                return [DIE, ATTACK]
        else:

            if attackerId == "PlayerRole":

                return [ATTACK, BE_ATTACKED]

            else:

                return [BE_ATTACKED, ATTACK]

    # 玩家角色使用药物
    def take_medicine(self):

        player = self.get_role("PlayerRole")

        medicineId = player.get_attachments("medicine")

        medicine = self.get_role(medicineId)

        medicineNum = medicine.get_role_attr("num")
        recoverHP = medicine.get_effert("recoverHP")

        hp = player.get_role_attr("hp")

        if medicineNum == 0:

            return [USE_OUT, hp]

        else:

            if hp < PLAYER_MAX_HP:

                medicineNum -= 1

                player.set_attr_value("num", medicineNum)

            return [RECOVER_HP, min(PLAYER_MAX_HP, hp + recoverHP)]


    # 玩家角色购买物品
    def buy_attachment(self, attachmentId):

        player = self.get_role("PlayerRole")

        attachment = self.get_role(attachmentId)

        attachmentType = attachment.get_role_attr("attachmentType")

        money = player.get_role_attr("money")
        price = attachment.get_role_attr("price")

        if money < price:

            return LACK_OF_MONEY

        else:

            money -= price

            player.set_attr_value("money", money)

        playerAttachment = player.get_role_attr("attachments")

        if attachmentType == "medicine":

            if playerAttachment["medicine"] is None:

                playerAttachment["medicine"] = attachmentId

            else:

                playerMedicine = self.get_role(playerAttachment["medicine"])

                num = playerMedicine.get_role_attr("num") + 1

                playerMedicine.set_attr_value("num", num)

            return BUY_MEDICINE

        elif attachmentType == "weapon2":

            if playerAttachment["weapon2"] is None:

                playerAttachment["weapon2"] = attachmentId

            attachment.set_attr_value("sold", True)

            return BUY_WEAPON2

        elif attachmentType == "weapon3":

            if playerAttachment["weapon3"] is None:

                playerAttachment["weapon3"] = attachmentId

            attachment.set_attr_value("sold", True)

            return BUY_WEAPON3

    # 玩家角色获得金钱
    def obtain_money(self, increase):

        player = self.get_role("PlayerRole")

        money = player.get_role_attr("money")

        money += increase

        player.set_attr_value("money", money)

        return [OBTAIN_MONEY, money]

    # 玩家更换武器
    def change_weapon(self, weaponId):

        player = self.get_role("PlayerRole")

        prevWeapon = self.get_role(player.get_role_attr("currWeapon"))

        currWeapon = self.get_role(weaponId)
        currType = currWeapon.get_role_attr("attachmentType")

        player.set_attr_value("currWeapon", weaponId)
        player.set_attr_value("attackForce", player.get_role_attr("attackForce") - prevWeapon.get_role_attr("attackForce") + currWeapon.get_role_attr("attackForce"))

        if currType == "weapon1":

            return CHANGE_WEAPON1

        elif currType == "weapon2":

            return CHANGE_WEAPON2

        elif currType == "weapon3":

            return CHANGE_WEAPON3

    """""""""""""""""""""
    成员变量的set和get函数
    """""""""""""""""""""

    def get_role_by_model(self, modelId):

        for roleId, _modelId in self.__roleModelMap.iteritems():

            if _modelId == modelId:

                return self.get_role(roleId)

        return None

    def get_role_model(self, roleId):

        return self.get_role(roleId).get_attr_value("modelId")

    def get_role(self, roleId):

        return self.__roleMap[roleId]

    def get_roleId(self, role):

        for roleId, _role in self.__roleMap.iteritems():

            if _role == role:

                return roleId

        return None

    def get_roleModelMap(self):

        return self.__roleModelMap

    def get_roleMap(self):

        return self.__roleMap

    def get_one_kind_of_roles(self, roleName):

        roles = []

        for roleId, role in self.__roleMap.iteritems():

            if SeriousTools.extract_name_from_Id(roleId) == roleName:

                roles.append(role)

        return roles

    def get_role_face_hpr(self, roleId):

        role = self.__sceneMgr.get_res(self.__roleModelMap[roleId])

        roleHpr = role.getHpr()

        h = (roleHpr.getH() - 90) * math.pi / 180

        return LVecBase3f(math.cos(h), 0, 0)

    """""""""""
    角色信息打印
    """""""""""

    def print_roleModelMap(self):

        print "--Role Model Map--"

        for modelId in self.__roleModelMap.keys():

            print modelId, " : ", self.__roleModelMap[modelId]

        print "--------------------"

    def print_roleMap(self):

        print "--Role Name Map--"

        for name in self.__roleMap.keys():

            print name, " : ", self.__roleMap[name]

        print "--------------------"

    def destroy_role(self, role):
        pass




