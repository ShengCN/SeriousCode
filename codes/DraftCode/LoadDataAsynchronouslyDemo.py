# -*- coding:utf-8 -*-

from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from panda3d.core import Vec3

# Panda3D really makes it very easy to load and use assets like models, actors,
# textures, and sounds. But there is a problem with the default behavior of
# the asset loader -- it blocks the execution of the engine
# This is not a problem if all data is loaded before the player is allowed to
# see the game world, but if models and other assets are to be loaded while
# the game is running, we are facing a serious problem because the frame rate
# will drop dramatically for a moment. This will cause game execution to stop
# for a short moment in a sudden and unpredictable way that breaks gameplay
# To avoid getting into such problems, Panda3D offers the ability to load data
# through background thread. This is a very useful feature if game assets are loaded
# on the fly, such as the popular use case with seamless streaming in game worlds.
# It is also a great way to reduce initial loading times. The main level geometry and
# everything visible from the starting position is loaded before the player enters the
# world and the rest of it is loaded afterwards, often depending on the position in the game world

class Application(ShowBase):

    def __init__(self):

        ShowBase.__init__(self)

        self.cam.setPos(0, -30, 6)

        taskMgr.doMethodLater(3,
                              self.load,
                              "load",
                              extraArgs = [
                                  "/e/models/teapot",
                                  Vec3(-5, 0, 0),
                                  self.modelLoaded
                              ]
                              )
        taskMgr.doMethodLater(5,
                              self.load,
                              "load",
                              extraArgs = [
                                  "/e/models/panda",
                                  Vec3(5, 0, 0),
                                  self.actorLoaded
                              ]
                              )

    def load(self, name, pos, cb):

        loader.loadModel(name, callback = cb, extraArgs = [pos])

    def modelLoaded(self, model, pos):

        model.reparentTo(render)
        model.setPos(pos)

    def actorLoaded(self, model, pos):

        self.panda = Actor(model, {"walk":"/e/models/panda-walk"})
        self.panda.reparentTo(render)
        self.panda.setPos(pos)
        self.panda.loop("walk")

app = Application()
app.run()