# -*-coding:utf-8 -*-

#!/usr/bin/env python

# Author: Yang chenjing
# Last Updated: 2016-06-28
#
# This tutorial shows mainMemu interface,
# include begin new game and select archives operations.

from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.DirectButton import DirectButton
from pandac.PandaModules import TransparencyAttrib
from panda3d.core import loadPrcFileData
from direct.task import Task
from resources_manager import ResourcesManager
from blood import Blood
import os
import Image, ImageFilter
from panda3d.core import *
from main import Main

from trade import Trade

# loadPrcFileData('', 'fullscreen 1')
loadPrcFileData('','win-size 1324 725')#设置窗口大小


class MainMenu(ShowBase):

    def __init__(self):

        ShowBase.__init__(self)

        self.__image = OnscreenImage(image='../../resources/images/menu/home1.png', pos=(0, 0, 0), scale=1)
        self.__image.setSx(self.getAspectRatio())
        self.__image.setTransparency(TransparencyAttrib.MAlpha)

        self.__main=Main()

        self.accept("a",self.__main.show)

        self.__trade=Trade()
        self.accept("b",self.__trade.show)


mm=MainMenu()
mm.run()