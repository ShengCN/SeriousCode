# coding=utf-8
from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from panda3d.core import *

from ControlModule.serious_state_manager import SeriousFSM
from FollowCam import FollowCam
from direct.showbase.DirectObject import DirectObject
from keyboard_mouse_handler import GameControlMouseHandler
from keyboard_mouse_handler import GamePlayerMouseHandler
from test_application import testApplication
from main_menu import MainMenu

class SeriousGame(DirectObject):
    def __init__(self):
        DirectObject.__init__(self)
        self.__fsm = SeriousFSM()
        self.accept("serious_menu",self.__menu_window)
        self.accept("serious_new_game",self.__new_game_window)
        self.accept("serious_load_game",self.__load_game_window)
        self.accept("serious_description",self.__description)
        self.__fsm.request('Menu')

    def __menu_window(self):
        if type(self.__menu_window)==MainMenu:
            self.__menu_window.start()
            self.__fsm.set_menu_window(self.__menu_window)
            self.__menu_window.run()
        else:
            self.__menu_window = MainMenu()
            self.__menu_window.start()
            self.__fsm.set_menu_window(self.__menu_window)
            self.__menu_window.run()

    def __new_game_window(self):
        print '控制器选择了新建游戏窗口'

    def __load_game_window(self):
        print '控制器选择载入游戏窗口'

    def __description(self):
        print '进入描述界面'



game = SeriousGame()
