# -*-coding:utf-8 -*-

#!/usr/bin/env python

# Author: Yang chenjing
# Last Updated: 2016-06-26
#
# This tutorial shows play meida interface

from direct.showbase.DirectObject import DirectObject
from direct.showbase.ShowBase import ShowBase
from panda3d.core import *

class MediaPlayer():

    #载入视频文件
    #render:ShowBase属性，render2d
    def __init__(self):

        # Load the texture. We could use loader.loadTexture for this,
        # but we want to make sure we get a MovieTexture, since it
        # implements synchronizeTo.
        self.__mediaFileName=dict()
        self.__mediaFileName["1"]="../../resources/media/PandaSneezes.ogv"
        self.__mediaFileName["2"]="../../resources/media/PandaSneezes.ogv"
        self.__mediaFileName["3"] = "../../resources/media/PandaSneezes.ogv"
        self.__tex = MovieTexture("name")

    # 播放视频文件
    #render:ShowBase属性，render2d
    #id:视频ID
    def playMedia(self,render,id):
        id=str(id)
        # self.__mediaFileName[id] = fileName
        success = self.__tex.read(self.__mediaFileName[id])
        # Set up a fullscreen card to set the video texture on.
        cm = CardMaker("My Fullscreen Card")
        cm.setFrameFullscreenQuad()

        # Tell the CardMaker to create texture coordinates that take into
        # account the padding region of the texture.
        cm.setUvRange(self.__tex)

        # Now place the card in the scene graph and apply the texture to it.
        self.__card = NodePath(cm.generate())
        self.__card.reparentTo(render)
        self.__card.setTexture(self.__tex)

        self.__sound = loader.loadSfx(self.__mediaFileName[id])
        # Synchronize the video to the sound.
        self.__tex.synchronizeTo(self.__sound)

        self.__sound.play()

    #移除视频
    def destroy(self):
        self.__sound.stop()
        self.__card.detachNode()


