# -*- coding:utf-8 -*-

from panda3d.core import Vec3

import math

a = Vec3(3, 3, 0)
b = Vec3(1, 1, 0)

c = a - b

c.normalize()

A = 0 * math.pi / 2

cX = c.getX() * math.cos(A) + c.getY() * math.sin(A)
cY = c.getY() * math.cos(A) - c.getX() * math.sin(A)

c.setX(cX)
c.setY(cY)

print c
print "a\n"
print math.cos(math.pi/4)
print math.acos(0.5) * 180 / math.pi

x, y = -0.0409929, 0.999159

print math.acos(x / math.sqrt(x**2 + y**2)) * 180 / math.pi