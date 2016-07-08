# coding=utf-8
from input_handler import *
from panda3d.core import *

"""菜单场景的监听"""
class MenuPlayerInputHandler(MenuInputHandler):
    def __init__(self):
        MenuInputHandler.__init__(self)

        base.disableMouse()
        props = WindowProperties()
        props.setCursorHidden(True)
        base.win.requestProperties(props)

        self.__count = 0
        self.accept("w",self.__countDecress)
        self.accept("arrow_up",self.__countDecress)
        self.accept("s",self.__countIncress)
        self.accept("arrow_down",self.__countIncress)
        self.accept("enter",self.__decide)
        self.accept("escape",exit)

        taskMgr.add(self.updateInput, "update input")

    def __countDecress(self):
        self.__count = self.__count - 1
        self.beginSelect()

    def __countIncress(self):
        self.__count = self.__count + 1
        self.beginSelect()

    def __decide(self):
        tmp = 4
        tmp = self.__count % tmp
        print tmp
        switchInput = {0:self.beginNewGame,
        			   1:self.beginLoadGame,
        			   2:self.beginDescription,
        			   3:self.beginExit}
        switchInput[tmp]()

    def get_count(self):
        tmp = 4
        tmp = self.__count % tmp
        return tmp

    def updateInput(self,task):
        self.dispatchMessages()
        return task.cont

"""游戏场景的监听"""
class GamePlayerMouseHandler(GameInputHandler):
    def __init__(self):
        GameInputHandler.__init__(self)

        base.disableMouse()
        props = WindowProperties()
        props.setCursorHidden(True)
        base.win.requestProperties(props)

        self.accept("escape",self.beginSetting)
        self.accept("w",self.beginForward)
        self.accept("w-up",self.endForward)
        self.accept("s",self.beginBack)
        self.accept("s-up",self.endBack)
        self.accept("a",self.beginLeft)
        self.accept("a-up",self.endLeft)
        self.accept("d",self.beginRight)
        self.accept("d-up",self.endRight)
        self.accept("mouse1",self.beginAttack)
        self.accept("mouse1-up",self.endAttack)

        taskMgr.add(self.updateInput,"update input")

    def updateInput(self,task):
        self.dispatchMessages()
		return task.cont