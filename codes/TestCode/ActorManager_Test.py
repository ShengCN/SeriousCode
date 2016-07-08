
from SceneModule.actor_manager import ActorManager

from direct.showbase.ShowBase import ShowBase

actorPath = "/e/models/panda"
actionsPath = {
    "walk" : "/e/models/panda-walk",
    "run" : "/e/models/panda-walk"
}

def print_a():

    print "a"

def print_b():

    print "b"

class Test(ShowBase):

    def __init__(self):

        ShowBase.__init__(self)

        actorMgr = ActorManager()

        actor = actorMgr.load_res(actorPath, actionsPath)

        actor.reparentTo(self.render)

        actorId = actorMgr.get_actorId(actor)

        print actorId

        #actor.accept("y", print_a)
        #actor.accept("y-up", print_b)

        actorMgr.add_toggle_to_actor("y", actorId, "walk")
        actorMgr.add_effert_to_actor("y", actorId, "actor_move_forward")

        actorMgr.add_toggle_to_actor("s", actorId, "walk")
        actorMgr.add_effert_to_actor("s", actorId, "actor_move_backward")

        actorMgr.set_actorMoveSpeed(0.01)

        self.cam.setPos(0, 50, 50)
        self.cam.lookAt(0, 0, 0)

        self.taskMgr.add(actorMgr.update_actors, "update_actors")

test = Test()
test.run()
