# coding=utf-8
import  sys
sys.path.append('../')
from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from panda3d.core import *

from ControlModule.serious_state_manager import SeriousFSM
from direct.showbase.DirectObject import DirectObject
from keyboard_mouse_handler import GamePlayerMouseHandler
from test_application import testApplication
from main_menu import MainMenu
from ControlModule.common_para import *

loadPrcFileData("", CONFIG)

class SeriousGame(DirectObject):
    def __init__(self):
        DirectObject.__init__(self)
        self.__fsm = SeriousFSM()
        self.__window = MainMenu()
        self.accept("serious_menu",self.__menu_window)
        self.accept("serious_new_game",self.__new_game_window)
        self.accept("serious_load_game",self.__load_game_window)
        self.accept("serious_description",self.__description)
        self.__menu_window()

    def __menu_window(self):
        self.__window.start()
        self.__window.run()

    def __new_game_window(self):
        print '控制器选择了新建游戏窗口'
        self.__window.destroy()
        self.__window.game_window()

    def __load_game_window(self):
        print '控制器选择载入游戏窗口'
        self.__window.destroy()
        self.__window.archive()

    def __description(self):
        print '进入描述界面'
        self.__window.destroy()
        # False:help
        # True:description
        self.__window.help_menu(True)



game = SeriousGame()
