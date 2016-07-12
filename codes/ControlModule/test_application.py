# coding=utf-8
from direct.showbase.ShowBase import ShowBase
from BulletEngineModule.serious_game_scene import SeriousGameScene
from ControlModule.common_para import *
from RoleModule.role_manager import RoleManager
from SceneModule.scene_manager import SceneManager


class testApplication(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.roleMgr = RoleManager()
        self.sceneMgr = SceneManager()
        self.sceneMgr.bind_RoleManager(self.roleMgr)
        self.village = SeriousGameScene(self,self.sceneMgr,self.roleMgr)
        self.village.load_game_scene(ROOM,5)
        self.village.add_player_role()
        self.village.task_update()
        self.accept("3",self.village.destroy)

# app = testApplication()
# app.run()
