
# -*-coding:utf-8 -*-
from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from ResourcesModule.load_plot import LoadPlot
from panda3d.core import *

import math

class Demo(ShowBase):

    def __init__(self):

        ShowBase.__init__(self)

        actorPath = "/e/Material/hunter_WithGun.egg"

        actionsPath = {"attack" : "/e/Material/hunter_Attack2.egg"}

        self.disableMouse()

        self.actor = Actor(actorPath, actionsPath)

        self.actor.setPos(0, 0, 0)
        self.actor.reparentTo(self.render)

        self.accept("a", self.turn_true, [1])
        self.accept("d", self.turn_true, [2])
        self.accept("w", self.turn_true, [3])
        self.accept("a-up", self.turn_false, [1])
        self.accept("d-up", self.turn_false, [2])
        self.accept("w-up", self.turn_false, [3])

        self.cam.setPos(0, -50, 20)
        self.cam.lookAt(0, 0, 0)

        self.prevH = self.actor.getH()
        self.prevP = self.actor.getP()
        self.prevR = self.actor.getR()

        self.taskMgr.add(self.update_hpr, "update_hpr")

        self.a = False
        self.b = False
        self.c = False

        self.accept("mouse1", self.print_mouse_event, ["mouse1"])
        self.accept("mouse1-up", self.print_mouse_event, ["mouse1-up"])
        self.accept("mouse2", self.print_mouse_event, ["mouse2"])
        self.accept("mouse2-up", self.print_mouse_event, ["mouse2-up"])
        self.accept("mouse3", self.print_mouse_event, ["mouse3"])
        self.accept("mouse3-up", self.print_mouse_event, ["mouse3-up"])
        self.accept("wheel_up", self.print_mouse_event, ["wheel_up"])
        self.accept("wheel_down", self.print_mouse_event, ["wheel_down"])

        print LVecBase3f(0, 0, 0)
        print LPoint3f(0, 0, 0)

        print self.cam.getParent()

    def print_mouse_event(self, event):

        print "mouse event : ", event

        if event == "mouse1":

            self.actor.play("attack")



    def update_hpr(self, task):

        self.rotate_cw(task)
        self.rotate_ccw(task)
        self.move_forward(task)

        currH = self.actor.getH()
        currP = self.actor.getP()
        currR = self.actor.getR()

        if currH != self.prevH or \
            currP != self.prevP or \
            currR != self.prevR:

            #print "Actor Hpr change from (", self.prevH, ", ", self.prevP, ", ", self.prevR, ") to ", self.actor.getHpr()

            self.prevH = currH
            self.prevP = currP
            self.prevR = currR

            self.actor.setHpr(currH, currP, currR)

        #self.rotate_cw(task)
        #self.rotate_ccw(task)

        return task.cont

    def turn_false(self, a):

        if a == 1:
            self.a = False
        if a == 2:
            self.b = False
        if a == 3:
            self.c = False

    def turn_true(self, a):

        if a == 1:
            self.a = True
        if a == 2:
            self.b = True
        if a == 3:
            self.c = True

    def rotate_cw(self, task):

        if self.a == True:
            self.actor.setH(self.actor.getH() + globalClock.getDt() * 100)

        return task.cont

    def rotate_ccw(self, task):

        if self.b == True:
            self.actor.setH(self.actor.getH() - globalClock.getDt() * 100)

        return task.cont

    def move_forward(self, task):

        c = math.cos(self.actor.getH() * math.pi / 180 - math.pi / 2)
        s = math.sin(self.actor.getH() * math.pi / 180 - math.pi / 2)

        # print "actor current H : ", self.actor.getH()
        # print "cos(currH) = ", c

        dt = globalClock.getDt()

        if self.c == True:
            self.actor.setX(self.actor.getX() + c * dt * 10)
            self.actor.setY(self.actor.getY() + s * dt * 10)

        return task.cont

demo = Demo()
demo.run()