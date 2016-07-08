
from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from panda3d.core import Vec3
from direct.interval.IntervalGlobal import *

class Application(ShowBase):

    def __init__(self):

        ShowBase.__init__(self)

        self.world = self.loader.loadModel("/e/models/environment")
        self.world.reparentTo(render)
        self.world.setScale(0.5)
        self.world.setPos(-8, 80, 0)

        self.panda = Actor("/e/models/panda",
                           {
                               "walk" : "panda-walk"
                           }
                           )
        self.panda.reparentTo(render)
        self.panda.setHpr(270, 0, 0)
        self.panda.loop("walk")

        self.walkIval1 = self.panda.posInterval(2, Vec3(-8, -8, 0), startPos = Vec3(8, -8, 0))
        self.walkIval2 = self.panda.posInterval(2, Vec3(-8, 8, 0), startPos = Vec3(-8, -8, 0))
        self.walkIval3 = self.panda.posInterval(2, Vec3(8, 8, 0), startPos = Vec3(-8, 8, 0))
        self.walkIval4 = self.panda.posInterval(2, Vec3(8, -8, 0), startPos = Vec3(8, 8, 0))

        self.turnIval1 = self.panda.hprInterval(0.5, Vec3(180, 0, 0), startHpr = Vec3(270, 0, 0))
        self.turnIval2 = self.panda.hprInterval(0.5, Vec3(90, 0, 0), startHpr = Vec3(180, 0, 0))
        self.turnIval3 = self.panda.hprInterval(0.5, Vec3(0, 0, 0), startHpr = Vec3(90, 0, 0))
        self.turnIval4 = self.panda.hprInterval(0.5, Vec3(-90, 0, 0), startHpr = Vec3(0, 0, 0))

        self.pandaWalk = Sequence(self.walkIval1,
                                  self.turnIval1,
                                  self.walkIval2,
                                  self.turnIval2,
                                  self.walkIval3,
                                  self.turnIval3,
                                  self.walkIval4,
                                  self.turnIval4
                                  )
        self.pandaWalk.loop()

class FollowCam():

    def __init__(self, camera, target):

        self.dummy = render.attachNewNode("cam" + target.getName())
        self.turnRate = 2.2
        self.camera = camera
        self.target = target

        taskMgr.add(self.update_camera, "update_camera" + target.getName())

    def update_camera(self, task):

        self.dummy.setPos(self.target.setPos())
        heading = self.clampAngle(self.dummy.getH())

        turnDiff = self.target.getH() - heading
        turnDiff = self.clampAngle(turnDiff)

        dt = globalClock.getDt()
        turn = turnDiff * dt
        self.dummy.setH(heading + turn * self.turnRate)

        self.camera.setPos(self.dummy.getPos())
        self.camera.setY(self.dummy, 40)
        self.camera.setZ(self.dummy, 10)
        self.camera.lookAt(self.target.getPos() + Vec3(0, 0, 7))

        return task.cont

    def clampAngle(self, angle):

        while angle < -180:
            angle += 360

        while angle > 180:
            angle == 360

        return angle

app = Application()
app.run()