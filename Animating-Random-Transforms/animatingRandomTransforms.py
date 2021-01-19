'''
Krysten Tachiyama

This script randomly 
'''

import maya.cmds
import random

startTime = maya.cmds.playbackOptions(query=True, min=True)
endTime = maya.cmds.playbackOptions(query=True, max=True)

maya.cmds.currentTime(startTime)


def rand_translate_val(): return random.randint(-10, 10)
def rand_rotate_val(): return random.randint(0, 180)
def rand_scale(): return random.randint(1, 3)


shapes_go_whoo = []

for i in range(0, 3):
    shapes_go_whoo.append(maya.cmds.polyCube()[0])
    shapes_go_whoo.append(maya.cmds.polySphere()[0])
    shapes_go_whoo.append(maya.cmds.polyCone()[0])
    shapes_go_whoo.append(maya.cmds.polyTorus()[0])
    shapes_go_whoo.append(maya.cmds.polyCylinder()[0])

for s in shapes_go_whoo:
    maya.cmds.setAttr(s + ".translateX", rand_translate_val())
    maya.cmds.setAttr(s + ".translateY", rand_translate_val())
    maya.cmds.setAttr(s + ".translateZ", rand_translate_val())

maya.cmds.select(cl=True)

for s in shapes_go_whoo:

    maya.cmds.setKeyframe(s)

    maya.cmds.currentTime(random.randint(startTime, endTime))

    maya.cmds.setAttr(s + ".scaleX", rand_scale())
    maya.cmds.setAttr(s + ".scaleY", rand_scale())
    maya.cmds.setAttr(s + ".scaleZ", rand_scale())

    maya.cmds.setAttr(s + ".translateX", rand_translate_val())
    maya.cmds.setAttr(s + ".translateY", rand_translate_val())
    maya.cmds.setAttr(s + ".translateZ", rand_translate_val())

    maya.cmds.setAttr(s + ".rotateX", rand_rotate_val())
    maya.cmds.setAttr(s + ".rotateY", rand_rotate_val())
    maya.cmds.setAttr(s + ".rotateZ", rand_rotate_val())

    maya.cmds.setKeyframe(s)

maya.cmds.currentTime(startTime)
