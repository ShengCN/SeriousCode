# -*-coding:utf-8 -*-
from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from ResourcesModule.load_plot import LoadPlot
from panda3d.core import *

class Demo(ShowBase):

    def __init__(self):

        ShowBase.__init__(self)

        actorPath = "/e/Material/finalHunter"

        modelPath = "/e/Material/finalHunter"

        actionsPath = {"walk":"/e/Material/hunter_WALK123"}

        self.actor = Actor(actorPath, actionsPath)

        self.actor.setPos(0, 0, 0)
        self.actor.reparentTo(self.render)

        self.model = self.loader.loadModel(modelPath)
        self.model.setPos(10, 10, 0)
        self.model.reparentTo(self.render)
        self.actor.accept("w", self.print_w)

        self.cam.setPos(0, 100, 50)
        self.cam.lookAt(0, 0, 0)

        self.accept("w", self.model_move)
        self.accept("s", self.model_move2)
        self.accept("a", self.model_move3)
        self.accept("d", self.model_move4)

        self.demo = LoadPlot()
        self.demo.init_dialogue(1)

        self.flag = False

        self.taskMgr.add(self.show_dialog, "show_dialog")

        print self.actor.getPos()
        print self.actor.getHpr()
        print self.actor.getScale()

    def show_dialog(self, task):

        vector = self.model.getPos() - self.actor.getPos()
        #print vector.length()
        if vector.length() < 10:
            if self.flag == False:
               self.demo.init_dialogue(1)
               self.demo.dialogue_next()
               self.flag = True
        else:
            self.demo.destroy_dialogue()
            self.flag = False

        return task.cont

    def model_move(self):
        dt = globalClock.getDt() * 100
        self.model.setY(self.model.getY() - dt)

    def model_move2(self):
        dt = globalClock.getDt() * 100
        self.model.setY(self.model.getY() + dt)

    def model_move3(self):
        dt = globalClock.getDt() * 100
        self.model.setX(self.model.getX() + dt)

    def model_move4(self):
        dt = globalClock.getDt() * 100
        self.model.setX(self.model.getX() - dt)

    def print_w(self):

        print "w"

demo = Demo()
demo.run()