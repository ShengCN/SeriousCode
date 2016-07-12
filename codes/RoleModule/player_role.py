# -*- coding:utf-8 -*-

from role_base import Role

class PlayerRole(Role):

    def __init__(self, modelId):

        Role.__init__(self,
                      roleId = "PlayerRole",
                      modelId = modelId,
                      ableToTalk = True,
                      ableToCtrl = True,
                      ableToAtck = True,
                      )

        self.append_role_attr(key = "hp", value = 100)
        self.append_role_attr(key = "money", value = 0)
        self.append_role_attr(key = "attackForce1", value = 30)
        self.append_role_attr(key = "attackForce2", value = 45)
        self.append_role_attr(key = "attackForce3", value = 60)
        self.append_role_attr(key = "attackForce", value = 30)
        self.append_role_attr(key = "walkSpeed", value = 5)
        self.append_role_attr(key = "runSpeed", value = 20)
        self.append_role_attr(key = "rotateSpeed", value = 100)
        self.append_role_attr(key = "touchRadius", value = 20)
        self.append_role_attr(key = "cd", value = -1)
        self.append_role_attr(key = "remainCd", value = -1)
        self.append_role_attr(key = "currWeapon", value = 1)
        self.append_role_attr(key = "weapon1", value = 1)
        self.append_role_attr(key = "weapon2", value = 0)
        self.append_role_attr(key = "weapon3", value = 0)
        self.append_role_attr(key = "story", value = None)
        self.append_role_attr(key = "recoverHp", value = 35)
        self.append_role_attr(key = "medicineNum", value = 0)

    # 添加附属物
    def add_attachment(self, attachmentType, attachmentId):

        attachments = self._roleAttr["attachments"]

        if attachments[attachmentType].count(attachmentId) == 0:

            attachments[attachmentType].append(attachmentId)

    def delete_attachment(self, attachmentType, attachmentId):

        attachments = self._roleAttr["attachments"]

        if attachments[attachmentType].count(attachmentId) > 0:

            attachments[attachmentType].remove(attachmentId)

    def get_attachments(self, attachmentType):

        attachments = self._roleAttr["attachments"]

        if attachments.has_key(attachmentType) is True:

            return attachments[attachmentType]

        return None