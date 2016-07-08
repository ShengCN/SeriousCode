# -*- coding:utf-8 -*-

from direct.showbase.ShowBase import ShowBase
from panda3d.core import GeoMipTerrain

class Application(ShowBase):

    def __init__(self):

        ShowBase.__init__(self)

        self.terrain = GeoMipTerrain("terrain")
        self.terrain.setHeightfield("/e/models/height.bmp")
        self.terrain.setColorMap("/e/models/grass.jpg")
        #self.terrain.getRoot().setSz(100)
        self.terrain.getRoot().reparentTo(self.render)
        self.terrain.getRoot().setPos(0, 0, 0)
        self.terrain.hide()
        #z = self.terrain.getElevation(256, 256) * 40
        #self.cam.setPos(0, 10, 50)
        #self.cam.lookAt(5, 5, 0)

        #self.terrain.setFocalPoint(self.cam)
        self.taskMgr.add(self.updateTerrain, "updateTerrain")

    def updateTerrain(self, task):

        self.terrain.update()
        return task.cont

app = Application()
app.run()
