
from direct.directbase.DirectStart import *
from panda3d.core import RigidBodyCombiner, NodePath, Vec3

import random

rbc = RigidBodyCombiner("rbc")
rbcnp = NodePath(rbc)
rbcnp.reparentTo(render)

for i in range(200):

    pos = Vec3(random.uniform(-100, 100),
               random.uniform(-100, 100),
               random.uniform(-100, 100))

    f = loader.loadModel("box.egg")
    f.setPos(pos)
    f.reparentTo(rbcnp)

rbc.collect()
run()