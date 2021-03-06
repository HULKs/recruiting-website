# Motion Task

<x-prologue image="recruiting-website-motion" command="bash -c 'cp /usr/src/app/{*.py,*.png,*.ttf} /data/ && echo Initialized files.'" />

## Introduction
In this task you are supposed to help the Nao robot kick the ball as close to the grey target position as possible. To simplify this task, we will work in 2-dimensions only. For defining a kick motion, you should set the angles for the three parts of the Nao leg (thigh, tibia and foot).
Note that every joint has a minimum and maximum angle.
If you want to test your code, you can click the "Run program" button below to see a visualisation of your code. In the left upper corner, you can see the time that has passed (in seconds) and the number below that shows the smallest distance between the ball and the target that you achieved with your current code.

## Keyframes
A motion is defined by a list of keyframes. Each keyframe contains the target angles (in radians) of the thigh, tibia and foot joints as well as the duration in which the keyframe should be executed.
The position of the three joints and the neutral angles can be seen in the picture below.

<x-text-editor file="/data/generate_keyframes.py" mode="python" />

<x-button image="recruiting-website-motion" command="python generate_animation.py" label="Run program" working-directory="/data" />

<x-image-viewer file="/data/animation.webp" mime="image/gif" />
