
from ResourcesModule.load_plot import LoadPlot

from direct.showbase.ShowBase import ShowBase
from panda3d.core import *

class Demo(ShowBase):

    def __init__(self):

        ShowBase.__init__(self)

        demo = LoadPlot()

        demo.init_interface(2)

        demo.dialogue_next()

demo = Demo()
demo.run()