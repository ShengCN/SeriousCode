# -*-coding:utf-8 -*-

#!/usr/bin/env python

# Author: Yang chenjing
# Last Updated: 2016-06-26
#
# This tutorial play music and adjust volume

from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenText import OnscreenText
from direct.gui.OnscreenImage import OnscreenImage
from direct.showbase.DirectObject import DirectObject
from direct.gui.DirectSlider import DirectSlider
from direct.gui.DirectButton import DirectButton
from pandac.PandaModules import TransparencyAttrib
from direct.interval.SoundInterval import SoundInterval
from panda3d.core import *


class MySound(DirectObject):
    # 载入所有音乐与音效
    def __init__(self):

        self.__music=dict()
        self.__music["1"]=loader.loadMusic("../../resources/music/test.mp3")#主界面背景音乐
        self.__music["2"] = loader.loadMusic('../../resources/music/test.mp3')#平时音乐
        self.__music["3"] = loader.loadMusic('../../resources/music/test.mp3')#战斗音乐
        # self.__music["4"] = loader.loadSfx('../../resources/music/openclose.ogg')#对话音效
        self.__music["4"] = loader.loadSfx('../../resources/music/openclose.ogg')#枪击音效
        self.__music["5"] = loader.loadSfx('../../resources/music/openclose.ogg')#载入游戏音效
        self.__music["6"] = loader.loadSfx('../../resources/music/openclose.ogg')#退出游戏音效

        #设置音乐与音效的音量
        for index in self.__music:
            self.__music[index].setVolume(0.5)

        # 设置音乐与音效的循环次数
        self.__music["1"].setLoop(0)
        self.__music["2"].setLoop(0)
        self.__music["3"].setLoop(0)
        self.__music["4"].setLoop(1)
        self.__music["5"].setLoop(1)
        self.__music["6"].setLoop(1)

        self.__volume=0.5#滑动条值

        self.__musicTime = 0#背景音乐所处时间

        self.__backgroundId=1#背景音乐ID

        # self.__musicOpen = True#音乐是否开启

        self.__music["1"].play()#主界面背景音乐自动开启


    def set_volume(self,volume):
        self.__volume=volume
        for index in self.__music:
            self.__music[index].setVolume(volume)

    def get_volume(self):
        return self.__volume

    # #开关背景音乐
    # def toggleMusicBox(self,base):
    #
    #     #关闭音乐
    #     if (self.__musicOpen==True):
    #         base.disableAllAudio()
    #         # self.__musicButton["text"]="Open"
    #     #开启音乐
    #     else:
    #         base.enableAllAudio()
    #         self.__music[str(self.__backgroundId)].play()
    #         # self.__musicButton["text"]="Close"
    #
    #     # self.__musicButton.setText()
    #     self.__musicOpen=not self.__musicOpen

    #播放音乐
    #id：音乐与音效id
    def play_music(self,id):
        if(id==1 or id==2 or id==3):
            self.__backgroundId=id
        id=str(id)
        self.__music[id].play()

    #关闭音乐
    def stop_music(self,id):
        id=str(id)
        self.__music[id].stop()
