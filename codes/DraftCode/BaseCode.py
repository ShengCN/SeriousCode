# -*- coding:utf-8 -*-

from direct.showbase.ShowBase import ShowBase

modelPath = "/e/Serious2/Material/ModelEGGS/Village/v6.egg"

class Demo(ShowBase):

    def __init__(self):

        ShowBase.__init__(self)
        self.render.setTwoSided(True)

        model = self.loader.loadModel(modelPath)
        model.reparentTo(self.render)
        model.setPos(0, 0, 0)

        self.cam.setPos(0, 150, 150)
        self.cam.lookAt(0, 0, 0)

demo = Demo()
demo.run()
