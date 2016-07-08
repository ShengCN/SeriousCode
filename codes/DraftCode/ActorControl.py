# -*- coding:utf-8 -*-

from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from direct.interval.ActorInterval import ActorInterval
from pandac.PandaModules import WindowProperties
from panda3d.core import Mat4


# v1
# Without Collision, Light, Terrain
# With Camera Fixed

# v2
# Witout Collision, Light, Terrain
# But Now the Actor Move With the Camera

class ActorControl(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.actorModelPath = "/e/models/ralph"
        self.actorAnimaPath = {
            "run": "/e/models/ralph-run",
            "walk": "/e/models/ralph-walk",
            "jump": "/e/models/ralph-jump"
        }

        self.actor = Actor(self.actorModelPath,
                           self.actorAnimaPath)
        self.actor.reparentTo(self.render)
        self.actor.setPos(0, 0, 0)
        self.actor.setScale(0.75)

        print self.actor.getAnimNames()

        self.actorAnimaKeymap = {
            "run_forward": False,
            "run_backward": False,
            "run_left": False,
            "run_right": False,
            "jump": False
        }

        self.jumpItval = ActorInterval(
            actor=self.actor,
            animName="jump",
            #constrainedLoop=0,
            #startFrame=0,
            #endFrame=self.actor.getNumFrames("jump")
        )
        print self.jumpItval.getName()
        self.isMoving = False
        self.isJumping = False

        self.actorCurrH = 0

        self.disableMouse()
        self.camera.setPos(0, 15, self.actor.getZ() + 15)
        self.camera.lookAt(0, 0, self.actor.getZ())
        camVec = self.camera.getPos() - self.actor.getPos()
        print "camVec Length : ", camVec.length()
        print "Z : ", self.actor.getZ()

        self.actor.accept("w", self.set_keymap, ["run_forward", True])
        self.actor.accept("w-up", self.set_keymap, ["run_forward", False])
        self.actor.accept("s", self.set_keymap, ["run_backward", True])
        self.actor.accept("s-up", self.set_keymap, ["run_backward", False])
        self.actor.accept("a", self.set_keymap, ["run_left", True])
        self.actor.accept("a-up", self.set_keymap, ["run_left", False])
        self.actor.accept("d", self.set_keymap, ["run_right", True])
        self.actor.accept("d-up", self.set_keymap, ["run_right", False])
        self.actor.accept("space", self.jump_up)
        # self.actor.accept("space-up", self.jump_up, [False])
        # self.actor.accept("space-up", self.jump_up, ["jump", False])

        self.accept("wheel_up", self.camera_move, ["wheel_up"])
        self.accept("wheel_down", self.camera_move, ["wheel_down"])
        self.accept("arrow_left", self.camera_move, ["arrow_left"])
        self.accept("arrow_right", self.camera_move, ["arrow_right"])

        self.taskMgr.add(self.actor_animate, "actor_animate")
        # self.taskMgr.add(self.debug_check_actor_pos, "debug_check_actor_pos")

        self.isFullscreen = False
        self.accept("f", self.set_fullscreen)

    def set_fullscreen(self):
        winProps = WindowProperties()
        self.isFullscreen = not self.isFullscreen
        winProps.setFullscreen(self.isFullscreen)
        self.win.requestProperties(winProps)

    def set_keymap(self, key, value):
        self.actorAnimaKeymap[key] = value
        # print key, " : ", value

    def jump_up(self):
        self.jumpItval.loop()

    def actor_animate(self, task):

        dt = globalClock.getDt()

        actorRunSpeed = 5

        actorCurrH = self.actor.getH()
        if self.actorAnimaKeymap["run_forward"]:
            self.actorCurrH = 0
            if self.actorAnimaKeymap["run_left"]:
                self.actorCurrH = 45
            if self.actorAnimaKeymap["run_right"]:
                self.actorCurrH = 315
            self.actor.setH(self.actorCurrH)
            self.actor.setY(self.actor.getY() - actorRunSpeed * dt)
        if self.actorAnimaKeymap["run_backward"]:
            self.actorCurrH = 180
            if self.actorAnimaKeymap["run_left"]:
                self.actorCurrH = 135
            if self.actorAnimaKeymap["run_right"]:
                self.actorCurrH = 225
            self.actor.setH(self.actorCurrH)
            self.actor.setY(self.actor.getY() + actorRunSpeed * dt)
        if self.actorAnimaKeymap["run_left"]:
            self.actorCurrH = 90
            if self.actorAnimaKeymap["run_forward"]:
                self.actorCurrH = 45
            if self.actorAnimaKeymap["run_backward"]:
                self.actorCurrH = 135
            self.actor.setH(self.actorCurrH)
            self.actor.setX(self.actor.getX() + actorRunSpeed * dt)
        if self.actorAnimaKeymap["run_right"]:
            self.actorCurrH = 270
            if self.actorAnimaKeymap["run_forward"]:
                self.actorCurrH = 315
            if self.actorAnimaKeymap["run_backward"]:
                self.actorCurrH = 225
            self.actor.setH(self.actorCurrH)
            self.actor.setX(self.actor.getX() - actorRunSpeed * dt)

        if self.actorAnimaKeymap["run_forward"] or \
                self.actorAnimaKeymap["run_backward"] or \
                self.actorAnimaKeymap["run_left"] or \
                self.actorAnimaKeymap["run_right"]:
            if self.isMoving is False:
                self.actor.loop("run")
                self.isMoving = True

        else:
            if self.isMoving:
                self.actor.stop()
                self.actor.play("walk")
                self.actor.pose("walk", 4)
                self.isMoving = False

        # camVec = self.actor.getPos() - self.camera.getPos()
        # camVec.setZ(0)
        # camDist = camVec.length()
        # camVec.normalize()
        # if camDist > 10.0:
        #     self.camera.setPos(self.camera.getPos() + camVec * (camDist - 10))
        #     camDist = 10.0
        # if camDist < 5.0:
        #     self.camera.setPos(self.camera.getPos() - camVec * (5 - camDist))
        #     camDist = 5.0

        return task.cont

    def camera_move(self, mouseEvent):

        mouseCurrY = self.camera.getY()
        mouseMoveOffset = 2

        if mouseEvent == "wheel_up":
            self.camera.setY(mouseCurrY + mouseMoveOffset)

        if mouseEvent == "wheel_down":
            self.camera.setY(mouseCurrY - mouseMoveOffset)

        print "Camera Pos : ", self.camera.getPos()

    def debug_check_actor_pos(self, task):
        # sleep(1)
        print "actor pos : ", self.actor.getPos()
        return task.cont


actorCtrl = ActorControl()
actorCtrl.run()
