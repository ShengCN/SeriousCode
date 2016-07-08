
# from direct.showbase.ShowBase import ShowBase
# from direct.particles.ParticleEffect import ParticleEffect

# in essene, any particle effect needs three key parts:
# the renderer, the emitter, and the factory
# the renderer translates the particle object into visible
# object on the screen
# the emitter assigns initial locations and velocity vectors
# for the particles
# the factory generates particles and assigns their attributes

# class Demo(ShowBase):
#
#     def __init__(self):
#
#         ShowBase.__init__(self)
#
#         # tell Panda3D to enable particles
#         self.enableParticles()
#
#         # create a ParticleEffect object and tell it to
#         # use a particle configuration file
#         particle = ParticleEffect()
#         particle.loadConfig("particleConfigFile")
#
#         # to start the ParticleEffect
#         particle.start(parent = self.render,
#                        renderParent = self.render)
#
#         # to reset the ParticleEffect
#         particle.reset()
#
#         # to stop the ParticleEffect
#         particle.disable()
#
#         # to completely remove the ParticleEffect
#         particle.cleanup()
#
#         # to save the particle config file
#         particle.saveConfig("particleConfigFile")
#
#
# demo = Demo()
# demo.run()

# every particle effect needs at least eleven parameters

### poolSize
# maximum number of simultaneous particles --- [0, infinity)
### birthRate
# seconds between particle births --- (0, infinity)
### litterSize
# variation of litter size --- [1, infinity)
### litterSpread
# number of particles created at each birth --- [0, infinity)
### localVelocityFlag
# whether or not velocities are absolute --- Boolean
### systemGrowsOlder
# whether or not the system has a lifespan --- Boolean
### systemLifespan
# age of the system in seconds --- [0, infinity)
### BaseParticleRenderer*render
# pointer to particle renderer --- RendererType
### BaseParticleRenderer*emitter
# pointer to particle emitter --- EmitterType
### BaseParticleRenderer*factory
# pointer to particle factory --- FactoryType

"""
Particle Factories
"""
# there are two types of particle factories : Point and ZSpin
# the differences between these factories lie in the
# orientation and rotational abilities
# There are some common variables to the factories
### lifespanBase
# average lifespan in seconds --- [0, infinity)
### lifespanSpread
# variation in lifespan --- [0, infinity)
### massBase
# average particle mass --- [0, infinity)
### massSpread
# variation in particle mass --- [0, infinity)
### terminalVelocityBas
# average particle terminal velocity --- [0, infinity)
### terminalVelocitySpread
# variation in terminal velocity --- [0, infinity)

# Point particle factories generate simple particles
# they have no additional parameters

# ZSpin particle factories generate that spin around Z axis
# the vertical axis in Panda3D

# there are a large number of particle emitters,
# each categorized by the volume of speac they represent

# all emitters have three modes : explicit, radiate and custom
# explicit mode emits the particles in parallel in the same direction
# radiate mode emits particles away from a specific point
# custom mode emits particles with a velocity determined by
# the particular emitter

### emissionType
# emission mode --- ET_EXPLICIT, ET_RADIATE, ET_CUSTOM
### explicitLaunchVector
# initial velocity in explicit mode --- (x, y, z)
### radiateOrigin
# point particles launch away from in radiate mode --- (x, y, z)
### amplitude
# launch velocity multiplier --- (-infinity, infinity)
### amplitudeSpeed
# spread for launch velocity multiplier --- [0, infinity)

from direct.showbase.ShowBase import ShowBase
from panda3d.core import TextNode
from panda3d.core import AmbientLight, DirectionalLight
from panda3d.core import LPoint3, LVector3
from panda3d.core import Filename
from panda3d.physics import BaseParticleEmitter, BaseParticleRenderer
from panda3d.physics import PointParticleFactory, SpriteParticleRenderer
from panda3d.physics import LinearNoiseForce, DiscEmitter
from direct.particles.Particles import Particles
from direct.particles.ParticleEffect import ParticleEffect
from direct.particles.ForceGroup import ForceGroup
from direct.gui.OnscreenText import OnscreenText
from direct.interval.Interval import *
from direct.interval.IntervalGlobal import *
from direct.interval.FunctionInterval import *
import sys

HELP_TEXT = """
1: Load Steam
2: Load Dust
3: Load Fountain
4: Load Smoke
5: Load Smokering
6: Load Fireish
ESC: Quit
"""

class Demo(ShowBase):

    def __init__(self):

        ShowBase.__init__(self)

        self.title = OnscreenText(
            text = "Panda3D : Tutorial - Particles",
            parent = self.a2dBottomCenter,
            style = 1,
            fg = (1, 1, 1, 1),
            pos = (0.06, -0.06),
            align = TextNode.ALeft,
            scale = 0.05
        )

        self.accept("escape", sys.exit)
        self.accept("1", self.loadParticleConfig, ["steam.ptf"])
        self.accept("2", self.loadParticleConfig, ["dust.ptf"])
        self.accept("3", self.loadParticleConfig, ["fountain.ptf"])
        self.accept("4", self.loadParticleConfig, ["smoke.ptf"])
        self.accept("5", self.loadParticleConfig, ["smokering.ptf"])
        self.accept("6", self.loadParticleConfig, ["fireish.ptf"])

        self.disableMouse()
        self.cam.setPos(0, -20, 2)
        self.camLens.setFov(25)
        self.setBackgroundColor(0, 1, 0)

        self.enableParticles()
        self.teapot = self.loader.loadModel("teapot")
        self.teapot.setPos(0, 10, 0)
        self.teapot.reparentTo(self.render)
        self.setupLights()
        self.particle = ParticleEffect()
        self.loadParticleConfig("steam.ptf")

        self.accept("w", self.toggle_particle)

    def toggle_particle(self):

        particleSeq = Sequence(Func(self.particle_start),
                               Wait(2),
                               Func(self.particle_end))

        particleSeq.start()

    def loadParticleConfig(self, filename):

         self.particle.cleanup()
         self.particle = ParticleEffect()
         self.particle.loadConfig("/e/Panda3D-1.9.2-x64/samples/particles/"+filename)

         #self.particle.start(self.teapot)
         self.particle.setPos(3, 0, 2.225)

    def particle_start(self):

        self.particle.start(self.teapot)

    def particle_end(self):

        self.particle.softStop()

    def setupLights(self):

        ambientLight = AmbientLight("ambiengtLight")
        ambientLight.setColor((0.4, 0.4, 0.35, 1))
        directionalLight = DirectionalLight("directionalLight")
        directionalLight.setDirection(LVector3(0, 8, -2.5))
        directionalLight.setColor((0.9, 0.8, 0.9, 1))
        directionalLight.setColor((0.9, 0.8, 0.9, 1))

        self.teapot.setLight(self.teapot.attachNewNode(directionalLight))
        self.teapot.setLight(self.teapot.attachNewNode(ambientLight))

demo = Demo()
demo.run()










