'''
Krysten Tachiyama

This script creates a set of shapes and randomly transforms them
over random times. To see this happen, simply run the script
in Maya.
'''

import maya.cmds
import random

# initialize start and end keyframe times
startTime = maya.cmds.playbackOptions(query=True, min=True)
endTime = maya.cmds.playbackOptions(query=True, max=True)

maya.cmds.currentTime(startTime)


def rand_translate_val(): return random.randint(-10, 10)
def rand_rotate_val(): return random.randint(0, 180)
def rand_scale_val(): return random.randint(1, 3)


# list of shapes
shapes_go_whoo = []

# create shapes and append to shapes list
for i in range(0, 3):
    shapes_go_whoo.append(maya.cmds.polyCube()[0])
    shapes_go_whoo.append(maya.cmds.polySphere()[0])
    shapes_go_whoo.append(maya.cmds.polyCone()[0])
    shapes_go_whoo.append(maya.cmds.polyTorus()[0])
    shapes_go_whoo.append(maya.cmds.polyCylinder()[0])

# randomly initialize position of shapes
for s in shapes_go_whoo:
    print(s)
    maya.cmds.setAttr(s + ".translateX", rand_translate_val())
    maya.cmds.setAttr(s + ".translateY", rand_translate_val())
    maya.cmds.setAttr(s + ".translateZ", rand_translate_val())

maya.cmds.select(cl=True)

for s in shapes_go_whoo:
    # set keyframe of shape
    maya.cmds.setKeyframe(s)

    maya.cmds.currentTime(random.randint(startTime, endTime))

    # randomly scale, translate, and rotate shape
    maya.cmds.setAttr(s + ".scaleX", rand_scale_val())
    maya.cmds.setAttr(s + ".scaleY", rand_scale_val())
    maya.cmds.setAttr(s + ".scaleZ", rand_scale_val())

    maya.cmds.setAttr(s + ".translateX", rand_translate_val())
    maya.cmds.setAttr(s + ".translateY", rand_translate_val())
    maya.cmds.setAttr(s + ".translateZ", rand_translate_val())

    maya.cmds.setAttr(s + ".rotateX", rand_rotate_val())
    maya.cmds.setAttr(s + ".rotateY", rand_rotate_val())
    maya.cmds.setAttr(s + ".rotateZ", rand_rotate_val())

    maya.cmds.setKeyframe(s)

maya.cmds.currentTime(startTime)
