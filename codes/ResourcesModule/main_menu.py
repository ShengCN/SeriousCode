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

# loadPrcFileData('', 'fullscreen 1')
loadPrcFileData('','win-size 1324 725')#设置窗口大小


class MainMenu(ShowBase):

    def __init__(self):

        ShowBase.__init__(self)

        #load background image
        self.__image = OnscreenImage(image='../../resources/images/main_menu.jpg', pos=(0, 0, 0), scale=1)
        self.__image.setSx(self.getAspectRatio())
        self.__image.setTransparency(TransparencyAttrib.MAlpha)

        #Three main opertaions
        self.__newGameButton = DirectButton(pos=(-0.9, 0, 0.5,), text=("新的游戏"), scale=0.1,
                                            command=self.new_game,frameColor=(0,0,0,0),
                                            image=("../../resources/images/main_menu.jpg","../../resources/images/main_menu.jpg",
                                                   "../../resources/images/main_menu.jpg"))
        self.__selectArchiveButton = DirectButton(pos=(-0.9, 0, 0.3,), text="选择存档", scale=0.1,text_fg=(1,1,1,1),
                                            command=self.select_archives, frameColor=(0, 0, 0, 0),
                                            image=("../../resources/images/main_menu.jpg", "../../resources/images/main_menu.jpg",
                                                   "../../resources/images/main_menu.jpg"))
        self.__exitGameButton = DirectButton(pos=(-0.9, 0, 0.1,), text="退出游戏", scale=0.1,text_fg=(1,1,1,1),
                                            command=self.exit_game, frameColor=(0, 0, 0, 0),
                                            image=("../../resources/images/main_menu.jpg", "../../resources/images/main_menu.jpg",
                                                   "../../resources/images/main_menu.jpg"))

        self.accept("3", self.screenshot1,[self])
        self.accept("4", self.delete)

        #add task to update background-image scale
        self.taskMgr.add(self.example_task, 'exampleTask')

        self.__rm=ResourcesManager()


    # 移除界面上的按钮与图片
    def destroy_all(self):
        self.__newGameButton.destroy()
        self.__selectArchiveButton.destroy()
        self.__exitGameButton.destroy()
        self.__image.destroy()
        self.taskMgr.remove('exampleTask')

    def new_game(self):
        self.destroy_all()

        self.__blood = Blood()
        # self.__rm.show_dialog(1)
        self.accept("a", self.__rm.show_dialog, [1])
        self.accept("b", self.__rm.show_dialog, [2])
        self.accept("c", self.__rm.show_dialog, [3])
        self.accept("d", self.__rm.show_dialog, [4])
        self.accept("e", self.__rm.show_dialog, [5])
        self.accept("f", self.__rm.show_dialog, [6])
        self.accept("g", self.__rm.show_dialog, [7])
        self.accept("h", self.__rm.show_dialog, [8])
        self.accept("i", self.__rm.show_dialog, [9])
        self.accept("x", self.__rm.dialog_next)
        # self.accept("d", self.__rm.play_sound,[2])
        # self.accept("e", self.__rm.stop_sound,[2])
        # self.accept("f", self.__rm.play_sound,[4])
        # self.accept("g", self.__rm.stop_sound,[4])

        self.accept("z",self.__rm.set_path,["123"])

        self.accept("0", self.__blood.init_blood)
        self.accept("1",self.__blood.bloodAdd)
        self.accept("2", self.__blood.bloodMinu)

        self.accept("5",self.__rm.show_prompt_box,["注意"])
        self.accept("6", self.__rm.destroy_prompt)


        #调用对话
        # lp=LoadPlot()
        # lp.init_interface()
        #调用声音
        # ms=MySound()
        # ms.volume_slider()
        #调用视频
        # self.accept("h", self.__rm.play_media, [self,1])
        # self.accept("i", self.__rm.play_media, [self,2])
        # self.accept("i", self.__rm.destroy_media)

    def select_archives(self):
        self.destroy__all()

    def exit_game(self):
        self.destroy__all()

    def example_task(self,task):
        self.__image.setSx(self.getAspectRatio())
        return Task.cont

    def screenshot1(self,base):
        self.__x=self.screenshot()
        print self.__x
        img = Image.open(str(self.__x))
        im2 = img.filter(ImageFilter.BLUR)
        im2.save(str(self.__x))
        self.__background = OnscreenImage(image="../../resources/images/dialogue/npc_chat_frame.png", pos=(0, 0, 0),scale=(1.0))
        self.__background.setImage(str(self.__x))
        self.__background.setSx(base.getAspectRatio())

    def delete(self):
        self.__background.destroy()
        os.remove(str(self.__x))


mm=MainMenu()
mm.run()