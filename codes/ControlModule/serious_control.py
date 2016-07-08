# coding=utf-8
# serious_control模块是控制模块
# 是程序的入口模块,用来控制整个游戏的流程
# 编写人:盛逸辰
# 最新修改日期:2016.6.24
#
from direct.fsm.FSM import FSM

from SceneModule.SceneManager import SceneManager

# # 游戏的总状态机
# class SeriousState(FSM):
#     def __init__(self):
#         FSM.__init__(self,'SeriousFSM')

#     def enterBeginMenu(self):
#         print "开始菜单"
#         self.request("Load")

#     def exitBeginMenu(self):
#         print "exit begin menu"

#     def enterLoad(self):
#         print "i am loading"
#         self.request("Game")

#     def exitLoad(self):
#         print "exit load!"

#     def enterStraightGame(self):
#         print "straight to the game"

#     def exitStraightGame(self):
#         print "exit straight to the game!"

#     def enterGame(self):
#         print "in game"
#         self.request("ExitMenu")

#     def exitGame(self):
#         print "exit in game"

#     def enterExitMenu(self):
#         print "exit menu"
#         self.request("Save")

#     def exitExitMenu(self):
#         print "exit game"

#     def enterSave(self):
#         print "save game"

#     def exitSave(self):
#         print "exit save game"



class SeriousControl(object):

    def __init__(self):
        self.__begin_menu = False
        self.__load = False
        self.__in_game = False
        self.__save = False
        self.__exit = False

        self.accept("escape",exit)
        




ctrl = SeriousControl()



###新游戏
####游戏逻辑（人物控制）
#####esc
#####wasd（右键）
#####左键
#####攻击
#####交流
#####ai控制

####游戏后台
#####声音控制
#####场景载入


###载入
####游戏逻辑


###退出
