from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.DirectGui import *
from direct.actor.Actor import Actor
from panda3d.core import *
from direct.gui.OnscreenText import OnscreenText
from direct.interval.IntervalGlobal import *

class Application(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        font = loader.loadFont("cmr12.egg")
        props = TextProperties()
        props.setTextColor(1/84,1/2,1/8,0.5)
        tp = TextPropertiesManager.getGlobalPtr()
        tp.setProperties("yellow",props)
    
        OnscreenText(text = "Serious Game!!",
                     frame = Vec4(1,0,0,0),
                     bg = Vec4(84,2,8,0),
                     pos = Vec2(-0.5,0.5),
                     scale = 0.2,
                     font = font)
        myText = DirectLabel(text="fuck",
                             pos=Vec3(0.5,0.5,0),
                             scale = 0.2)
        self.waitBar = DirectWaitBar(text="loading",
                                range = 100,
                                value = 0,
                                pos = Vec3(0,0,-0.3))
        
        inc = Func(self.loadStep)
        load = Sequence(inc,Wait(1),inc,Wait(1),inc,Wait(1),inc)
        load.start()

    def loadStep(self):
        self.waitBar["value"] += 25



app = Application()
app.run()