# -*-coding:utf-8 -*-

#!/usr/bin/env python

# Author: Yang chenjing
# Last Updated: 2016-07-09

from direct.gui.OnscreenText import OnscreenText
from direct.gui.OnscreenImage import OnscreenImage
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import TransparencyAttrib
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import *
from pandac.PandaModules import *


class Trade(DirectObject):
    def __init__(self):
        self.__imagePath = "../../resources/images/trade/"

        self.__imageDict=dict()
        self.__imageDict["tf"]=self.__imagePath+"trade_frame.png"
        self.__imageDict["tfbg"] = self.__imagePath + "trade_frame_bg.png"
        self.__imageDict["purchase1"] = self.__imagePath + "btn_perchase_0"
        self.__imageDict["purchase2"] = self.__imagePath + "btn_perchase_1"
        self.__imageDict["btnUp"] = self.__imagePath + "btn_up.png"
        self.__imageDict["btnDown"] = self.__imagePath + "btn_down.png"

    def show(self):
        self.__tradeFrame=OnscreenImage(image=self.__imageDict["tf"], pos=(0.0,0.0,0.0),scale=(1.0, 0, 0.5))
        self.__tradeFrame.setTransparency(TransparencyAttrib.MAlpha)

        self.__tradeFrameBg = DirectEntry(text="", scale=.039, command=self.setText, width=2.0, pos=(-0.72, 0.5, -0.005),
                                          text_fg=(1,1,1,1),frameColor=(0,0,0,0),initialText="122", numLines=1, focus=0,
                                          focusInCommand=self.clearText,text_scale=1.1)

        # self.__tradeFrameBg = DirectEntry(initialText="12",frameSize=(-0.1,0.1,-0.1,0.1),text_scale=(1.0,0.0,1.0))

        # self.__tradeFrameBg = DirectEntry(text="1", pos=(-0.73,0.0,-0.01),scale=(0.010,0,0.04), initialText="12",
        #                                   numLines=1, focus=1)
        # self.__tradeFrameBg.setTransparency(TransparencyAttrib.MAlpha)
        # , image = self.__imageDict["tfbg"],
        # image_scale = (6.0, 0.0, 0.8), image_pos = (5.0, 0.0, 0.4)
        #

        # callback function to set  text
        # 设置文本的回调函数

        # add button
        # 添加按钮

        # self.__charactorTop = OnscreenImage(image=self.__imageDict["ctop"], pos=(-1.6, 0, 0.8), scale=(0.16, 0, 0.16))
        # self.__charactorTop.setTransparency(TransparencyAttrib.MAlpha)
        #
        # self.__charactor = OnscreenImage(image=self.__imageDict["charactor"], pos=(-1.6, 0, 0.8), scale=(0.15, 0, 0.15))
        # self.__charactor.setTransparency(TransparencyAttrib.MAlpha)
        #
        # self.__hpBg = OnscreenImage(image=self.__imageDict["hpbg"], pos=(-1.14, 0, 0.85), scale=(0.30, 0, 0.02))
        # self.__hpBg.setTransparency(TransparencyAttrib.MAlpha)
        #
        # self.__hp = OnscreenImage(image=self.__imageDict["hp"], pos=(-1.14, 0, 0.85), scale=(0.30, 0, 0.02))
        # self.__hp.setTransparency(TransparencyAttrib.MAlpha)
        #
        # self.__medicineFrame = OnscreenImage(image=self.__imageDict["mf"], pos=(-1.33, 0, 0.72), scale=(0.09, 0, 0.09))
        # self.__medicineFrame.setTransparency(TransparencyAttrib.MAlpha)
        #
        # self.__medicine = OnscreenImage(image=self.__imageDict["medicine"], pos=(-1.33, 0, 0.72), scale=(0.09, 0, 0.09))
        # self.__medicine.setTransparency(TransparencyAttrib.MAlpha)
        #
        # self.__gunFrame = OnscreenImage(image=self.__imageDict["gf"], pos=(-0.95, 0, 0.72), scale=(0.27, 0, 0.09))
        # self.__gunFrame.setTransparency(TransparencyAttrib.MAlpha)
        #
        # self.__gun = OnscreenImage(image=self.__imageDict["gun3"], pos=(-0.95, 0, 0.72), scale=(0.27, 0, 0.09))
        # self.__gun.setTransparency(TransparencyAttrib.MAlpha)
        #
        # self.__coin = OnscreenImage(image=self.__imageDict["coin"], pos=(1.35, 0, 0.8), scale=(0.40, 0, 0.065))
        # self.__coin.setTransparency(TransparencyAttrib.MAlpha)
        #
        # self.__medicineNumber = OnscreenText("19", pos=(-1.27, 0.65), scale=0.05, fg=(1, 1, 1, 1), shadow=(0, 0, 0, 1),
        #                            mayChange=True)
        #
        # self.__coinNumber = OnscreenText("500,000,000", pos=(1.40, 0.78), scale=0.07, fg=(1, 1, 1, 1), shadow=(0, 0, 0, 1),
        #                                      mayChange=True)

    def setText(self,textEntered):
        pass


    # clear the text
    # 清除文本
    def clearText(self):
        self.__tradeFrameBg.enterText('')
