# Motion Task

<x-prologue image="recruiting-website-motion" command="bash -c 'cp /usr/src/app/{*.py,*.png,*.ttf} /data/ && echo Initialized files.'" />

## Introduction

In this task you are supposed to help the Nao robot kick the ball as close to the grey target position as possible. To simplify this task, we will work in 2-dimensions only. For defining a kick motion, you should set the angles for the three parts of the Nao leg (thigh, tibia and foot).

Note that every joint has a minimum and maximum angle.

If you want to test your code, you can click the "Run program" button below to see a visualisation of your code. In the left upper corner, you can see the time that has passed (in seconds) and the number below that shows the smallest distance between the ball and the target that you achieved with your current code.

## Keyframes

A motion is defined by a list of keyframes. Each keyframe contains the target angles (in radians) of the thigh, tibia and foot joints as well as the duration in which the keyframe should be executed.
The position of the three joints and the neutral angles can be seen in the picture below.

![](joint_angles.png)

<x-text-editor file="/data/generate_keyframes.py" mode="python" />

<x-button image="recruiting-website-motion" command="python generate_animation.py" label="Run program" working-directory="/data" />

<x-image-viewer file="/data/animation.webp" mime="image/gif" />

## Kinematic Chain

In the following sections, we explore how [end effector](https://en.wikipedia.org/wiki/Robot_end_effector) positions and joint angles can be computed with [kinematic chains](https://en.wikipedia.org/wiki/Kinematic_chain). A kinematic chain is a mathematical model of how joints are connected together. It allows to calculate the position of the end effector from joint angles (forward kinematics) or joint angles from the position of the end effector (inverse kinematics).

### Forward Kinematics

With the so called [forward kinematics](https://en.wikipedia.org/wiki/Forward_kinematics) one can calculate the position of the end effector from the set of involved joint angles. Just from common sense it is obvious, that such a calculation is possible, because the position in space is exactly defined, when given all joint angles. Since we want to control the robot's leg, we need a model of the leg first. Recall to the leg structure that we introduced earlier:

New Image: ![](joint_angles.png)

The kinematic chain is constructed starting at the body of the robot where the leg is mounted. In our case this is the position of the hip joint or `position_0`. For calculating `position_1` at the end of the thigh with the length `length_1` and angle `theta_1`:

```python
theta_1_with_offset = theta_1 - math.radians(45)

position_1 = Vec2d(
    position_0.x + math.cos(theta_1_with_offset) * length_1,
    position_0.y + math.sin(theta_1_with_offset) * length_1,
)
```

The end position of the tibia `position_2` is rotated by `theta_2` around `position_1` and translated by `length_2`. Since the zero angle depends on `theta_1` it is added to `theta_2` (rotating the hip joint also rotates the end effector of our kinematic chain):

```python
theta_2_with_offset = theta_1_with_offset + theta_2 - math.radians(90)

position_2 = Vec2d(
    position_1.x + math.cos(theta_2_with_offset) * length_2,
    position_1.y + math.sin(theta_2_with_offset) * length_2,
)
```

Lastly, the end position of the foot span `position_3` is rotated by `theta_3` around `position_2` and translated by `length_3`. Again, `theta_1` and `theta_2` are added to `theta_3`:

```python
theta_3_with_offset = theta_1_with_offset + theta_2_with_offset + theta_3 + math.radians(111.61)

position_3 = Vec2d(
    position_2.x + math.cos(theta_3_with_offset) * length_3,
    position_2.y + math.sin(theta_3_with_offset) * length_3,
)
```
