
from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from panda3d.core import *

modelRootPath = "/e/Serious2"


wifeZombiePath = modelRootPath + "/Material/ModelEGGS/WifeZombie2/WifeZombie_Stand.egg"
wifeZombieActionsPath = {
    # "run" : modelRootPath + "/Material/ModelEGGS/WifeZombie2/WifeZombie_Walk.egg",
    # "attack" : modelRootPath + "/Materal/ModelEGGS/WifeZombie2/WifeZombie_Attack3.egg"
}

hunterPath = modelRootPath + "/Material/ModelEGGS/Hunter/hunter_Alarm1.egg"

class Demo(ShowBase):

    def __init__(self):

        ShowBase.__init__(self)

        hunter = self.loader.loadModel(hunterPath)
        hunter.reparentTo(self.render)
        #hunter.setHpr(45, 0, 0)

        print hunter.getHpr()

        self.cam.setPos(0, -20, 5)
        self.cam.lookAt(0, 0, 0)


demo = Demo()
demo.run()