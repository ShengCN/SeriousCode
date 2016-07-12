# -*- coding:utf-8 -*-

from direct.showbase.ShowBase import ShowBase
from panda3d.core import *

modelPath = "/e/Serious2/Material/ModelEGGS/Village/v6.egg"

class Demo(ShowBase):

    def __init__(self):

        ShowBase.__init__(self)
        self.render.setTwoSided(True)

        nodepath = NodePath("nodepath")
        nodepath.reparentTo(self.render)

        model = self.loader.loadModel(modelPath)
        model.reparentTo(nodepath)
        model.setPos(0, 0, 0)

        self.cam.setPos(0, 150, 150)
        self.cam.lookAt(0, 0, 0)

        nodepath.detachNode()

demo = Demo()
demo.run()
