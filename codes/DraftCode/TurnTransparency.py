
from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from direct.actor.Actor import Actor

ballPath = "/e/Material/Drop.egg"

class Demo(ShowBase):

    def __init__(self):

        ShowBase.__init__(self)

        self.ball = Actor(ballPath,
                     {
                         "drop" : ballPath
                     })
        self.ball.reparentTo(self.render)
        self.ball.setColor(1.0, 0, 0, 1.0)
        self.ball.setPos(0, 0, 0)
        #self.ball.play("drop")

        self.cam.setPos(0, 100, 10)
        self.cam.lookAt(0, 0, 0)

        self.accept("w", self.drop)

    def drop(self):

        self.ball.play("drop")


demo = Demo()
demo.run()