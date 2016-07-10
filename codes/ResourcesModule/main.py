# -*-coding:utf-8 -*-

#!/usr/bin/env python

# Author: Yang chenjing
# Last Updated: 2016-07-09

from direct.gui.OnscreenText import OnscreenText
from direct.gui.OnscreenImage import OnscreenImage
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import TransparencyAttrib


class Main(DirectObject):
    def __init__(self):
        self.__imagePath = "../../resources/images/main/"

        self.__imageDict=dict()
        self.__imageDict["cbg"]=self.__imagePath+"charactor_bg.png"
        self.__imageDict["ctop"] = self.__imagePath + "charactor_top.png"
        self.__imageDict["charactor"] = self.__imagePath + "charactor3.png"
        self.__imageDict["hpbg"] = self.__imagePath + "hp_bg.png"
        self.__imageDict["hp"] = self.__imagePath + "hp.png"
        self.__imageDict["mf"] = self.__imagePath + "medicine_frame.png"
        self.__imageDict["medicine"] = self.__imagePath + "medicine.png"
        self.__imageDict["gf"] = self.__imagePath + "gun_frame.png"
        self.__imageDict["gun1"] = self.__imagePath + "gun_1.png"
        self.__imageDict["gun2"] = self.__imagePath + "gun_2.png"
        self.__imageDict["gun3"] = self.__imagePath + "gun_3.png"
        self.__imageDict["coin"] = self.__imagePath + "coin.png"

    def show(self):
        self.__charactorBg=OnscreenImage(image=self.__imageDict["cbg"], pos=(-1.6, 0, 0.8),scale=(0.16, 0, 0.16))
        self.__charactorBg.setTransparency(TransparencyAttrib.MAlpha)

        self.__charactorTop = OnscreenImage(image=self.__imageDict["ctop"], pos=(-1.6, 0, 0.8), scale=(0.16, 0, 0.16))
        self.__charactorTop.setTransparency(TransparencyAttrib.MAlpha)

        self.__charactor = OnscreenImage(image=self.__imageDict["charactor"], pos=(-1.6, 0, 0.8), scale=(0.15, 0, 0.15))
        self.__charactor.setTransparency(TransparencyAttrib.MAlpha)

        self.__hpBg = OnscreenImage(image=self.__imageDict["hpbg"], pos=(-1.14, 0, 0.85), scale=(0.30, 0, 0.02))
        self.__hpBg.setTransparency(TransparencyAttrib.MAlpha)

        self.__hp = OnscreenImage(image=self.__imageDict["hp"], pos=(-1.14, 0, 0.85), scale=(0.30, 0, 0.02))
        self.__hp.setTransparency(TransparencyAttrib.MAlpha)

        self.__medicineFrame = OnscreenImage(image=self.__imageDict["mf"], pos=(-1.33, 0, 0.72), scale=(0.09, 0, 0.09))
        self.__medicineFrame.setTransparency(TransparencyAttrib.MAlpha)

        self.__medicine = OnscreenImage(image=self.__imageDict["medicine"], pos=(-1.33, 0, 0.72), scale=(0.09, 0, 0.09))
        self.__medicine.setTransparency(TransparencyAttrib.MAlpha)

        self.__gunFrame = OnscreenImage(image=self.__imageDict["gf"], pos=(-0.95, 0, 0.72), scale=(0.27, 0, 0.09))
        self.__gunFrame.setTransparency(TransparencyAttrib.MAlpha)

        self.__gun = OnscreenImage(image=self.__imageDict["gun3"], pos=(-0.95, 0, 0.72), scale=(0.27, 0, 0.09))
        self.__gun.setTransparency(TransparencyAttrib.MAlpha)

        self.__coin = OnscreenImage(image=self.__imageDict["coin"], pos=(1.35, 0, 0.8), scale=(0.40, 0, 0.065))
        self.__coin.setTransparency(TransparencyAttrib.MAlpha)

        self.__medicineNumber = OnscreenText("19", pos=(-1.27, 0.65), scale=0.05, fg=(1, 1, 1, 1), shadow=(0, 0, 0, 1),
                                   mayChange=True)

        self.__coinNumber = OnscreenText("500,000,000", pos=(1.40, 0.78), scale=0.07, fg=(1, 1, 1, 1), shadow=(0, 0, 0, 1),
                                             mayChange=True)