
from InterfaceModule.dx_interface import DXInterface

class Test(object):

    def __init__(self):

        dxItfc = DXInterface()

        dxItfc.get_showbase().run()

test = Test()