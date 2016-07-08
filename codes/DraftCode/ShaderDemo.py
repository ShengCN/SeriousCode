from direct.showbase.ShowBase import ShowBase
from panda3d.core import *

class Application(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)
        self.world = self.loader.loadModel("environment")
        self.world.reparentTo(self.render)
        self.world.setScale(0.5)
        self.world.setPos(-8, 80, 0)
        shader = self.loader.loadShader("shader.cg")
        self.render.setShader(shader)
        self.cam.setPos(0, -40, 10)

        self.render.setShaderAuto()

app = Application()
app.run()