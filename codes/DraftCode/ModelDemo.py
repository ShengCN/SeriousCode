
from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from panda3d.core import *

class Demo(ShowBase):

    def __init__(self):

        ShowBase.__init__(self)

        modelPath = "/e/Material/finalHunter"

        self.model1 = self.loader.loadModel(modelPath)
        self.model2 = self.loader.loadModel(modelPath)
        self.model3 = self.loader.loadModel(modelPath)
        self.model4 = self.loader.loadModel(modelPath)
        self.model5 = self.loader.loadModel(modelPath)
        self.model6 = self.loader.loadModel(modelPath)
        self.model7 = self.loader.loadModel(modelPath)
        self.model8 = self.loader.loadModel(modelPath)

        self.model1.setPos(0, 0, 0)
        self.model1.setColor(1.0, 0.5, 0.5, 1)
        self.model1.reparentTo(self.render)
        self.model2.setPos(0, 0, 0)
        self.model2.reparentTo(self.render)
        self.model3.setPos(0, 0, 0)
        self.model3.reparentTo(self.render)
        self.model4.setPos(0, 0, 0)
        self.model4.reparentTo(self.render)
        self.model5.setPos(0, 0, 0)
        self.model5.reparentTo(self.render)
        self.model6.setPos(0, 0, 0)
        self.model6.reparentTo(self.render)
        self.model7.setPos(0, 0, 0)
        self.model7.reparentTo(self.render)
        self.model8.setPos(0, 0, 0)
        self.model8.reparentTo(self.render)

        print self.model1.getPos() - self.model2.getPos()

        self.cam.setPos(0, 0, 200)
        self.cam.lookAt(0, 0, 0)

        self.direction1 = LPoint3f(0.967902, 0.251326, 0)
        self.direction2 = LPoint3f(0.862125, -0.506696, 0)
        self.direction3 = LPoint3f(0.251326, -0.967902, 0)
        self.direction4 = LPoint3f(-0.506696, -0.862125, 0)
        self.direction5 = LPoint3f(-0.967902, -0.251326, 0)
        self.direction6 = LPoint3f(-0.862125, 0.506696, 0)
        self.direction7 = LPoint3f(-0.251326, 0.967902, 0)
        self.direction8 = LPoint3f(0.506696, 0.862125, 0)

        self.taskMgr.add(self.actor_move, "actor_move")

        self.accept("w", self.change_direction, [1])
        self.accept("s", self.change_direction, [-1])

    def actor_move(self, task):

       self.model1.setPos(self.model1.getPos() + self.direction1 * globalClock.getDt())
       self.model2.setPos(self.model2.getPos() + self.direction2 * globalClock.getDt())
       self.model3.setPos(self.model3.getPos() + self.direction3 * globalClock.getDt())
       self.model4.setPos(self.model4.getPos() + self.direction4 * globalClock.getDt())
       self.model5.setPos(self.model5.getPos() + self.direction5 * globalClock.getDt())
       self.model6.setPos(self.model6.getPos() + self.direction6 * globalClock.getDt())
       self.model7.setPos(self.model7.getPos() + self.direction7 * globalClock.getDt())
       self.model8.setPos(self.model8.getPos() + self.direction8 * globalClock.getDt())

       return task.cont

    def change_direction(self, d):

        self.direction = LPoint3f(d, 1, 0)

demo = Demo()
demo.run()