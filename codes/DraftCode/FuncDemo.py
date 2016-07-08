
from direct.interval.FunctionInterval import *
from direct.interval.Interval import *
from direct.interval.IntervalGlobal import *
from direct.showbase.ShowBase import ShowBase
from pandac.PandaModules import TransparencyAttrib

class Demo(ShowBase):

    def __init__(self):

        ShowBase.__init__(self)

        modelPath = "/e/Material/finalHunter.egg"
        self.model = self.loader.loadModel(modelPath)
        self.model.reparentTo(self.render)
        self.model.setPos(0, 0, 0)

        # ballPath = "/e/Material/Drop.egg"
        # self.ball = self.loader.loadModel(ballPath)
        # self.ball.reparentTo(self.render)
        # self.ball.setPos(0, 0, 0)
        # self.ball.hide()
        # x = self.ball.getX()
        # y = self.ball.getY()

        self.model.setTransparency(TransparencyAttrib.MAlpha)
        colorItvl = LerpColorInterval(
            nodePath = self.model,
            duration = 2,
            color = (0),
        )
        colorItvl.start()

        # posItvl = LerpPosInterval(
        #     nodePath = self.ball,
        #     duration = 1,
        #     pos = (x, y, 0)
        # )

        seq = Sequence(colorItvl)#, Func(self.show_ball))
        seq.start()

        self.cam.setPos(0, 50, 20)
        self.cam.lookAt(0, 0, 0)

    # def show_ball(self):
    #
    #     self.ball.show()

    def actor_show(self):

        self.model.show()

    def actor_hide(self):

        self.model.hide()

demo = Demo()
demo.run()