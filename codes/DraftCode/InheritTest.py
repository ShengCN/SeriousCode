
class A(object):

    _a = 0

    def __init__(self):

        self._a += 1

    def __print_all(self):

        print "A : ", self._a

class B(A):

    def __init__(self):

        A.__init__(self)

    def print_all(self):
        self.__print_all()
        print "B : ", self._a

b = B()
b.print_all()

