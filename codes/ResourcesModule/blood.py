from direct.gui.OnscreenImage import OnscreenImage
from direct.showbase.DirectObject import DirectObject

class Blood(DirectObject):
    def init(self):
        pass

    def init_blood(self):
        self.__image = OnscreenImage(image='../../resources/images/1.jpg', pos=(-0.9, 0, -0.2), scale=(0.3, 0, 0.05))
        self.__x = self.__image.getSx()

    def bloodAdd(self):
        self.__x = self.__image.getSx()
        self.__x += 0.01
        self.__image.setSx(self.__x)

    def bloodMinu(self):
        self.__x=self.__image.getSx()
        self.__x-=0.01
        self.__image.setSx(self.__x)