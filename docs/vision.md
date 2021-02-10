# Vision Task
[<< back to Bootcamp](index.md)

Naturally, a core element of robot soccer is ball detection. On this page we provide you with a sandbox to build a simple ball detection algorithm on your own! There is an exemplary image out of our simulated environment picturing the opponents goal, some field lines, as well as an orange ball. Please write a program in Python that detects the ball in x- and y-coordinates.

Basic knowledge of [Python](https://wiki.python.org/moin/BeginnersGuide/Programmers) is required.

We provide the following classes and functions to assist you in accomplishing this task:

 <script>
    window.intergramId = "402774621";
    window.intergramCustomizations = {
        titleClosed: 'Chat with HULKs',
        titleOpen: 'HULKs Bootcamp Group',
        introMessage: 'Welcome to the HULKs Bootcamp Telegram Group Chat. Please be extra excellent and patient. If you have a specific question it is best to ask right away, instead of asking if you can ask a question. It might take a bit of time until someone is available to answer.',
        autoResponse: 'If you are not getting a reply and cannot wait any longer, please leave your Telegram username here in chat, so we can reach you later.',
        autoNoResponse: 'Noone has answered yet. Please remember to leave your Telegram username here in chat, before you leave.',
        mainColor: "#2eac66",
        alwaysUseFloatingButton: false // Use the mobile floating button also on large screens
    };
 </script>
 <script id="intergram" type="text/javascript" src="https://www.intergram.xyz/js/widget.js"></script>

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

<x-prologue image="recruiting-website-red-ball" command="bash -c 'cp /usr/src/app/{process_image.py,red-ball.png} /data/ && cp /data/{red-ball,output}.png && echo Initialized files.'" />

<x-text-editor file="/data/process_image.py" mode="python" />

<x-button image="recruiting-website-red-ball" command="python process_image.py" label="Run program" working-directory="/data" />

<x-image-viewer file="/data/output.png" mime="image/png" />
