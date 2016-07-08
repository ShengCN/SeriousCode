# -*- coding:utf-8 -*-

from role_base import Role

class NPCRole(Role):

    def __init__(self, modelId):

        Role.__init__(self,
                      roleId="NPCRole",
                      modelId=modelId,
                      ableToTalk=True,
                      ableToCtrl=False,
                      ableToAtck=False,
                      )

        self.append_role_attr(key="actions", value=dict())





