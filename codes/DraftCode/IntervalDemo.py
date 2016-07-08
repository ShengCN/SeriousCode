
from direct.showbase.ShowBase import ShowBase
from direct.interval.LerpInterval import LerpPosInterval
from direct.interval.LerpInterval import LerpHprInterval

class IntervalDemo(ShowBase):

    def __init__(self):

        ShowBase.__init__(self)

        model = self.loader.loadModel("/e/models/ralph/ralph.egg")
        model.reparentTo(self.render)
        model.setPos(0, 0, 0)

        posItvl = LerpPosInterval(model,
                                  1,
                                  pos = (1, 0, 0),
                                  )
        hprItvl = LerpHprInterval(model,
                                  1,
                                  hpr = (50, 50, 50))

        posItvl.loop()
        hprItvl.loop()

        self.trackball.node().setPos(0, 10, -2)


itvlDemo = IntervalDemo()
itvlDemo.run()