
from SceneModule.actor_manager import ActorManager
from SceneModule.model_manager import ModelManager
from SceneModule.terrain_manager import TerrainManager

from direct.showbase.ShowBase import ShowBase

actorPath = "/e/models/panda"
actionsPath = {
    "walk" : "/e/models/panda-walk",
    #"run" : "/e/models/ralph-run",
    #"jump" : "/e/models/ralph-jump"
}

modelPath = "/e/models/ralph"

heightfield = "/e/models/grass.jpg"
colormap = "/e/models/grass.jpg"

class Test(ShowBase):

    def __init__(self):

        ShowBase.__init__(self)

        actorMgr = ActorManager()
        modelMgr = ModelManager()
        terraMgr = TerrainManager()

        actor = actorMgr.load_res(actorPath,
                                  actionsPath,
                                  self.render)

        actorMgr.add_toggle_to_actor("w", actor, "walk")
        #actorMgr.add_toggle_to_actor("e", actor, "run")
        #actorMgr.add_toggle_to_actor("space", actor, "jump")

        model = modelMgr.load_res(modelPath)

        terra = terraMgr.load_res(colormap, colormap, self.render)

        terra.getRoot().reparentTo(self.render)
        terra.getRoot().setPos(-50, -50, 0)
        terra.setFocalPoint(self.cam)

        print terra.getRoot().getPos()

        model.setPos(5, 0, 0)
        model.reparentTo(self.render)

        self.cam.setPos(0, 50, 2)
        self.cam.lookAt(0, 0, 0)

        taskMgr.add(terraMgr.update_terrain, "update_terrain")

test = Test()
test.run()
