# HULKs Recruiting 2021

## Hello, future HULK!

As you arrived at this page, we assume you are interested in joining our robot soccer team at TUHH.

This is a small task for you to check if you are interested in our kind of daily problems and if you enjoy solving those issues. In addition, it helps us to determine your skill level (but your input won't affect your application in any way).

Even if you are not completely happy with your solution or can't find any, don't hesitate to send us your result.

## Your Task

Naturally, a core element of robot soccer is ball detection. On this page we provide you with a sandbox to build a naive ball detection algorithm on your own! There is an exemplary image out of our simulated environment picturing the opponents goal, some field lines, as well as an orange ball. Please write a program in Python that detects the ball in x- and y-coordinates.

We provide the following classes and functions to assist you in accomplishing this task:

### Image

The `Image` object contains RGB color information for each pixel which can be accessed by calling the `at()` method with x- and y-coordinates.

For example, the red value of pixel with coordinates `x=0` and `y=10` can be accessed using: `image.at(0, 10).r`

The size of the image is returned by `image.width` and `image.height`.

### get_ball_image()

`get_ball_image` returns a reference to the `Image` object you're going to work with.

### plot_ball()

`plot_ball` takes x- and y-coordinates and places a cursor on the image. You are free to call it multiple times with differing values to create multiple cursors.

(Hint: look at the example code, click on “Run program”, then look at the image.)

Note: this is idealized. In reality, we program in C++ and soccer-balls are not red.

<x-prologue image="recruiting-website-red-ball" command="bash -c 'cp /usr/src/app/{process_image.py,red-ball.png} /data/ && cp /data/{red-ball,output}.png && echo Initialized files.'" />

<x-text-editor file="/data/process_image.py" mode="python" />

<x-button image="recruiting-website-red-ball" command="python process_image.py" label="Run program" working-directory="/data" />

<x-image-viewer file="/data/output.png" mime="image/png" />

Done? Please let us know and send a message (preferably containing your solution) to: hulks@tuhh.de
