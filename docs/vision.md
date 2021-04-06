# Vision Task

Naturally, a core element of robot soccer is ball detection. On this page we provide you with a sandbox to build a simple ball detection algorithm on your own! There is an exemplary image out of our simulated environment picturing the opponents goal, some field lines, as well as an orange ball. Please write a program in Python that detects the ball in x- and y-coordinates.

Basic knowledge of [Python](https://wiki.python.org/moin/BeginnersGuide/Programmers) is required.

We provide the following classes and functions to assist you in accomplishing this task:

### Image

The `Image` object contains RGB color information for each pixel which can be accessed by calling the `at()` method with x- and y-coordinates.

For example, the red value of pixel with coordinates `x=0` and `y=10` can be accessed using: `image.at(0, 10).r`

The size of the image is returned by `image.width` and `image.height`.

### get_ball_image()

`get_ball_image` returns a reference to the `Image` object you're going to work with.

### plot_ball_detection()

`plot_ball_detection` takes x- and y-coordinates, a radius and a color and places a circle on the image. You are free to call it multiple times with differing values to create multiple circles.

(Hint: look at the example code, click on “Run program”, then look at the image.)

Note: this is idealized. In reality, we program in C++ and soccer-balls are not red.

<x-prologue hidden image="recruiting-website-red-ball" command="bash -c 'cp /usr/src/app/{*.py,*.png} /data/ && cp /data/{red-ball,output}.png && echo Initialized files.'" />

<x-text-editor file="/data/process_image.py" mode="python" />

<x-button image="recruiting-website-red-ball" command="python process_image.py" label="Run program" working-directory="/data" />

<x-image-viewer file="/data/output.png" mime="image/png" />
