
from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from direct.directutil.Mopath import Mopath
from direct.interval.IntervalGlobal import *

class Application(ShowBase):

    def __init__(self):

        ShowBase.__init__(self)

        modelPath = "/e/Material/v11.egg"
        # modelPath4 = "/e/Material/house4.egg"
        # modelPath9 = "/e/Material/house9.egg"

        model = self.loader.loadModel(modelPath)
        model.reparentTo(self.render)
        model.setPos(0, 0, 0)
        model.setTwoSided(True)
        # model4 = self.loader.loadModel(modelPath4)
        # model4.reparentTo(self.render)
        # model4.setPos(30, 30, 0)
        #
        # model9 = self.loader.loadModel(modelPath9)
        # model9.reparentTo(self.render)
        # model9.setPos(-30, -30, 0)

        self.cam.lookAt(0, 0, 0)
        self.cam.setPos(0, -100, 100)

app = Application()
app.run()
