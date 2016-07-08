# -*- coding:utf-8 -*-

from direct.showbase.ShowBase import ShowBase

class Demo(ShowBase):

    def __init__(self):

        ShowBase.__init__(self)

        modelPath = "/e/Material/v1.egg"

        model = self.loader.loadModel(modelPath)

        model.setPos(0, 0, 0)
        model.reparentTo(self.render)

        self.cam.setPos(10, 10, 10)
        self.cam.lookAt(0, 0, 0)

demo = Demo()
demo.run()