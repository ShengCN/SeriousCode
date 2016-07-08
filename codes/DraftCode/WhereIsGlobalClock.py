
from direct.showbase.ShowBase import ShowBase

class Demo(ShowBase):

    def __init__(self):

        ShowBase.__init__(self)

        print "What"
        print globalClock.getDt()

demo = Demo()
demo.run()