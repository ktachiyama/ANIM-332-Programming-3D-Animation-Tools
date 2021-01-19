'''
Krysten Tachiyama
'''

import maya.cmds
import random

startTime = maya.cmds.playbackOptions(query=True, min=True)
endTime = maya.cmds.playbackOptions(query=True, max=True)

maya.cmds.currentTime(startTime)


def randTranslateVal(): return random.randint(-10, 10)
def randRotateVal(): return random.randint(0, 180)
def randScale(): return random.randint(1, 3)


shapesGoWhoo = []

for i in range(0, 3):
    shapesGoWhoo.append(maya.cmds.polyCube()[0])
    shapesGoWhoo.append(maya.cmds.polySphere()[0])
    shapesGoWhoo.append(maya.cmds.polyCone()[0])
    shapesGoWhoo.append(maya.cmds.polyTorus()[0])
    shapesGoWhoo.append(maya.cmds.polyCylinder()[0])

for s in shapesGoWhoo:
    maya.cmds.setAttr(s + ".translateX", randTranslateVal())
    maya.cmds.setAttr(s + ".translateY", randTranslateVal())
    maya.cmds.setAttr(s + ".translateZ", randTranslateVal())

maya.cmds.select(cl=True)

for s in shapesGoWhoo:

    maya.cmds.setKeyframe(s)

    maya.cmds.currentTime(random.randint(startTime, endTime))

    maya.cmds.setAttr(s + ".scaleX", randScale())
    maya.cmds.setAttr(s + ".scaleY", randScale())
    maya.cmds.setAttr(s + ".scaleZ", randScale())

    maya.cmds.setAttr(s + ".translateX", randTranslateVal())
    maya.cmds.setAttr(s + ".translateY", randTranslateVal())
    maya.cmds.setAttr(s + ".translateZ", randTranslateVal())

    maya.cmds.setAttr(s + ".rotateX", randRotateVal())
    maya.cmds.setAttr(s + ".rotateY", randRotateVal())
    maya.cmds.setAttr(s + ".rotateZ", randRotateVal())

    maya.cmds.setKeyframe(s)

maya.cmds.currentTime(startTime)
