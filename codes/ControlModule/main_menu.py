# -*-coding:utf-8 -*-
# Author: codingblack
# Last Updated: 2016-06-29
# menu菜单
# 游戏的开始界面
import sys
sys.path.append('../')

from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenImage import OnscreenImage
from ResourcesModule.resources_manager import ResourcesManager
from keyboard_mouse_handler import *
from direct.gui.OnscreenImage import OnscreenImage
from direct.showbase.DirectObject import DirectObject
from direct.gui.DirectSlider import DirectSlider
from direct.gui.DirectButton import DirectButton
from panda3d.core import *
from serious_state_manager import SeriousFSM

class MainMenu(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.accept("Exit",self.__exit)
        self.__rm = ResourcesManager()
        self.__destroySetting = False

    # 菜单界面
    def start(self):
        #全屏
        self.setFullScreen(0)

        #load background image
        self.__image = OnscreenImage(image='../../resources/images/menu/home1.png',scale=1)
        self.__image.setSx(self.getAspectRatio())
        self.__image.setTransparency(TransparencyAttrib.MAlpha)

        # 监听输入
        self.__keyInput = MenuPlayerInputHandler()
        self.accept("NewGame",self.__new_game)
        self.accept("LoadGame",self.__load_game)
        self.accept("Description",self.__description)
        self.accept("ChangeMenu",self.__change_menu)

        self.accept("a",self.setting_menu)
        self.accept("b",self.setting_destroy)

    # 设置全屏
    def setFullScreen(self,full):
        if full == 1 :
            self.__setFullscreen(2560,1600,0,0,1)
        else:
            self.__setFullscreen(800,600,150,50,0)

    # 清除界面，清除监听
    def destroy(self):
        self.__image.destroy()
        self.__keyInput.destroy()

    # 私有函数，选择全屏
    def __setFullscreen(self, width, height, posX, posY, full):
        winProps = WindowProperties()
        winProps.setOrigin(posX, posY)
        winProps.setSize(width, height)
        winProps.setFullscreen(full)
        self.win.requestProperties(winProps)

    # 私有函数，进入新建游戏界面
    def __new_game(self):
        print '进入new game'
        messenger.send("serious_new_game")
        print '发送了serious_new_game'

    # 私有函数，进入读取游戏界面
    def __load_game(self):
        print '进入load game'
        messenger.send("serious_load_game")
        print '发送了serious_load_game'

    # 私有函数，进入about界面
    def __description(self):
        print '进入description'
        messenger.send("serious_description")
        print '发送了serious_description'

    # 私有函数，用来自建的选择进入的游戏界面
    def __change_mode(self,image_path):
        self.__image.setImage(image_path)

    def __exit(self):
        print '进入exit'
        # self.__del__()
        exit()

    # 私有函数，更改游戏目录
    def __change_menu(self):
        switch_count = {0:'../../resources/images/menu/home1.png',
                        1:'../../resources/images/menu/home2.png',
                        2:'../../resources/images/menu/home3.png',
                        3:'../../resources/images/menu/home4.png',}
        self.__change_mode(switch_count[self.__keyInput.get_count()])

    #设置界面
    def setting_menu(self):
        if self.__destroySetting==False:
            # 设置界面背景图
            self.__background = OnscreenImage(image='../../resources/images/settings/setting_frame.png', pos=(0, 0, 0),
                                              scale=(1.0, 0, 0.7))
            self.__background.setTransparency(TransparencyAttrib.MAlpha)

            ##滑动条
            self.__slider = DirectSlider(pos=(0.16, 0, 0.26), scale=0.5, value=0.5, command=self.__setMusicSliderVolume,
                                         frameSize=(-1.0, 0.9, -0.06, 0.06),
                                         image='../../resources/images/settings/slide_bar.png',
                                         image_pos=(-0.05, 0, 0.0), image_scale=(1.0, 0, 0.05),
                                         thumb_image='../../resources/images/settings/slide_btn.png',
                                         thumb_image_pos=(-0.0, 0, 0.0), thumb_image_scale=0.1,
                                         thumb_frameSize=(0.0, 0.0, 0.0, 0.0))
            self.__slider.setTransparency(TransparencyAttrib.MAlpha)

            # self.__musicButton = DirectButton(pos=(0.9, 0, 0.75), text="Close", scale=0.1, pad=(0.2, 0.2), rolloverSound=None,
            #                                   clickSound=None, command=self.toggleMusicBox,extraArgs=[base])

            # 继续按钮
            self.__continueButton = DirectButton(pos=(-0.25, 0, 0.0), text="", scale=(0.2, 0, 0.1),
                                                 command=self.__continue_game,
                                                 image=("../../resources/images/settings/btn_continue_0.png",
                                                        "../../resources/images/settings/btn_continue_0.png"
                                                        , "../../resources/images/settings/btn_continue_1.png"),
                                                 frameColor=(0, 0, 0, 0))
            self.__continueButton.setTransparency(TransparencyAttrib.MAlpha)

            # 存档按钮
            self.__saveButton = DirectButton(pos=(0.33, 0, 0.0), text="", scale=(0.2, 0, 0.1), command=self.__save_game,
                                             image=("../../resources/images/settings/btn_save_0.png",
                                                    "../../resources/images/settings/btn_save_0.png"
                                                    , "../../resources/images/settings/btn_save_1.png"),
                                             frameColor=(0, 0, 0, 0))
            self.__saveButton.setTransparency(TransparencyAttrib.MAlpha)

            # 帮助按钮
            self.__helpButton = DirectButton(pos=(-0.25, 0, -0.25), text="", scale=(0.2, 0, 0.1), command=self.__help,
                                             image=("../../resources/images/settings/btn_help_0.png",
                                                    "../../resources/images/settings/btn_help_0.png"
                                                    , "../../resources/images/settings/btn_help_1.png"),
                                             frameColor=(0, 0, 0, 0))
            self.__helpButton.setTransparency(TransparencyAttrib.MAlpha)

            # 回到主界面按钮
            self.__homeButton = DirectButton(pos=(0.33, 0, -0.25), text="", scale=(0.2, 0, 0.1), command=self.__return_home,
                                             image=("../../resources/images/settings/btn_home_0.png",
                                                    "../../resources/images/settings/btn_home_0.png"
                                                    , "../../resources/images/settings/btn_home_1.png"),
                                             frameColor=(0, 0, 0, 0))
            self.__homeButton.setTransparency(TransparencyAttrib.MAlpha)

            # 设置滑动条value
            self.__slider['value'] = self.__rm.get_volume()

            self.__destroySetting = True

    #移除设置界面所有控件
    def setting_destroy(self):
        if self.__destroySetting==True:
            self.__background.destroy()
            self.__rm.set_volume(self.__slider['value'])
            self.__slider.destroy()
            # self.__musicButton.destroy()
            self.__continueButton.destroy()
            self.__saveButton.destroy()
            self.__helpButton.destroy()
            self.__homeButton.destroy()
            self.__destroySetting = False

    # 设置音乐声音大小
    def __setMusicSliderVolume(self):
        newVolume = self.__slider.guiItem.getValue()
        self.__rm.set_volume(newVolume)

    # 设置界面，私有函数,继续游戏
    def __continue_game(self):
        self.setting_destroy()

    # 设置界面，私有函数,存档
    def __save_game(self):
        self.setting_destroy()

    # 设置界面，私有函数,游戏帮助
    def __help(self):
        self.setting_destroy()

    # 设置界面，私有函数,回到主界面
    def __return_home(self):
        self.setting_destroy()
