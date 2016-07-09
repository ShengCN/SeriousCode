
from direct.showbase.ShowBase import ShowBase

class Demo(ShowBase):

    def __init__(self):

        ShowBase.__init__(self)

        self.taskMgr.add(self.print_task_time, "print_task_time")

        self.prevTime = 0

    def print_task_time(self, task):

        print "deltaTaskTime : ", task.time - self.prevTime, "   dt : ", globalClock.getDt()

        self.prevTime = task.time

        return task.cont

demo = Demo()
demo.run()