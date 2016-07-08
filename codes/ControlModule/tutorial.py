from math import pi,sin,cos

from direct.showbase.ShowBase import ShowBase, TransparencyAttrib
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3
import serious_log


class MyApp(ShowBase):
 
    def __init__(self):
        ShowBase.__init__(self)
 
        # Load the environment model.
        self.scene = self.loader.loadModel("/Developer/Panda3D/models/environment")
        # Reparent the model to render.
        self.scene.reparentTo(self.render)
        # Apply scale and position transforms on the model.
        self.scene.setScale(1, 1, 1)
        self.scene.setPos(-8, 42, 0)
 
        # Add the spinCameraTask procedure to the task manager.
        self.taskMgr.add(self.spinCameraTask,"SpinCameraTask")

        #load and transfrom the panda actor
        self.pandaActor = Actor("/Users/codingblack/SeriousPresent/models/GameModel/hunter.egg",
                                {"walk":"/Users/codingblack/SeriousPresent/models/GameModel/hunter_walk.egg"})
        self.pandaActor.setScale(0.005,0.005,0.005)
        self.pandaActor.reparentTo(self.render)
        self.pandaActor.setTransparency(TransparencyAttrib.MAlpha)
        self.pandaActor.setColor(1,1,1,0.5)
        # Loop its animation
        self.pandaActor.loop("walk")

        # create the four lerp intervals needed for the panda to
        # walk back and forth
        pandaPosInterval1 = self.pandaActor.posInterval(13,Point3(0,-10,0),startPos=Point3(0,10,0))
        pandaPosInterval2 = self.pandaActor.posInterval(13,Point3(0,-10,0),startPos=Point3(0,-10,0))
        pandaHprInterval1 = self.pandaActor.hprInterval(3,Point3(180,0,0),startHpr=Point3(0,0,0))
        pandaHprInterval2 = self.pandaActor.hprInterval(3,Point3(0,0,0),startHpr=Point3(180,0,0))

        # Create and play the sequence that coordinates the intervals.
        self.pandaPace = Sequence(pandaPosInterval1,pandaHprInterval1,pandaPosInterval2,pandaHprInterval2)
        self.pandaPace.loop()

    # Define a procedure to move the camera
    def spinCameraTask(self,task):
        angleDegrees = task.time * 6.0
        angleRadians = angleDegrees * (pi / 180.0)
        self.camera.setPos(20 * sin(angleRadians), -20.0 * cos(angleRadians), 3)
        self.camera.setHpr(angleDegrees, 0, 0)
        return Task.cont
 
app = MyApp()
app.run()