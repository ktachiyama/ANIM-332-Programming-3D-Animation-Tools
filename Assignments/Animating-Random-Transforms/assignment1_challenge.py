'''
Krysten Tachiyama

This script creates a set of random shapes and transforms them
over random times. To see this happen, simply run the script
in Maya.
'''

import maya.cmds
import random

# initialize start and end keyframe times
start_time = maya.cmds.playbackOptions(query=True, min=True)
end_time = maya.cmds.playbackOptions(query=True, max=True)

maya.cmds.currentTime(start_time)


def rand_translate_val(): return random.randint(-10, 10)
def rand_rotate_val(): return random.randint(0, 180)
def rand_scale_val(): return random.randint(1, 3)


# list where shapes will be stored
shapes_go_whoo = []

# list of possible shapes that can be created
shapes_list = [maya.cmds.polyCube,
               maya.cmds.polySphere,
               maya.cmds.polyCone,
               maya.cmds.polyTorus,
               maya.cmds.polyCylinder]

# list of possible attributes
attributes = [['.scaleX', rand_scale_val],
              ['.scaleY', rand_scale_val],
              ['.scaleZ', rand_scale_val],
              ['.translateX', rand_translate_val],
              ['.translateY', rand_translate_val],
              ['.translateZ', rand_translate_val],
              ['.rotateX', rand_rotate_val],
              ['.rotateY', rand_rotate_val],
              ['.rotateZ', rand_rotate_val]]

# create shapes and append to shapes list
for i in range(0, 15):
    shapes_go_whoo.append(random.choice(shapes_list)()[0])


# randomly initialize position of shapes
for s in shapes_go_whoo:
    maya.cmds.setAttr(s + ".translateX", rand_translate_val())
    maya.cmds.setAttr(s + ".translateY", rand_translate_val())
    maya.cmds.setAttr(s + ".translateZ", rand_translate_val())

maya.cmds.select(cl=True)


for s in shapes_go_whoo:
    # set keyframe of shape
    maya.cmds.setKeyframe(s)

    maya.cmds.currentTime(random.randint(start_time, end_time))

    # randomly assign 3 attributes to a shape
    for i in range(1, 3):
        attr = random.choice(attributes)
        maya.cmds.setAttr(s + attr[0], attr[1]())

    maya.cmds.setKeyframe(s)

maya.cmds.currentTime(start_time)
