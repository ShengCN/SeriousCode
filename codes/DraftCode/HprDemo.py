
from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from panda3d.core import *

modelRootPath = "/e/Serious2"


wifeZombiePath = modelRootPath + "/Material/ModelEGGS/WifeZombie2/WifeZombie_Stand.egg"
wifeZombieActionsPath = {
    # "run" : modelRootPath + "/Material/ModelEGGS/WifeZombie2/WifeZombie_Walk.egg",
    # "attack" : modelRootPath + "/Materal/ModelEGGS/WifeZombie2/WifeZombie_Attack3.egg"
}

class Demo(ShowBase):

    def __init__(self):

        ShowBase.__init__(self)

        self.wife = Actor(wifeZombiePath, wifeZombieActionsPath)
        self.wife.reparentTo(self.render)
        self.wife.setPos(0, 0, 0)
        self.wife.setScale(0.2)

        self.cam.setPos(0, -20, 5)
        self.cam.lookAt(0, 0, 0)

    def run(self):

        self.wife.loop("run")

    def attack(self):

        self.wife.loop("attack")

demo = Demo()
demo.run()