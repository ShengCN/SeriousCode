# -*- coding:utf-8 -*-

from role_base import Role

ATTACHMENT_TYPE = [
    "medicine",
    "weapon"
]

class AttachmentRole(Role):

    def __init__(self,
                 attachmentType,
                 modelId,
                 num
                 ):

        Role.__init__(self,
                      roleId="AttachmentRole",
                      modelId=modelId,
                      ableToTalk=False,
                      ableToCtrl=False,
                      ableToAtck=False,
                      )

        self.append_role_attr(key = "attachmentType", value = attachmentType)
        self.append_role_attr(key = "num", value = num)
        self.append_role_attr(key = "price", value = 0)
        self.append_role_attr(key = "sold", value = False)
        self.append_role_attr(key = "effert", value = dict())

    def add_holderId(self, holderId):

        if self._roleAttr["holderId"].count(holderId) == 0:

            self._roleAttr["holderId"].append(holderId)

    def delete_holderId(self, holderId):

        if self._roleAttr["holderId"].count(holderId) > 0:

            self._roleAttr["holderId"].remove(holderId)

    def add_effert(self, effertName, effertValue):

        if self._roleAttr["effert"].has_key(effertName) is False:

            effert = self._roleAttr["effert"]

            effert[effertName] = effertValue

    def change_effert(self, effertName, effertValue):

        if self._roleAttr["effert"].has_key(effertName) is True:

            effert = self._roleAttr["effert"]

            effert[effertName] = effertValue

    def get_effert(self, effertName):

        effert = self._roleAttr["effert"]

        if effert.has_key(effertName) is True:

            return effert[effertName]

