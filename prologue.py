# Don't forget to unimport as much as possbile afterwards.
import io
import sys

# Disable Traceback to make fake name errors
# seem like the real ones
sys.tracebacklimit = 0

# Capture stdout
__original_stdout__ = sys.stdout
sys.stdout = io.StringIO()

# Unimport!

del sys
del io

# numpy configuration has to happen after
# stdout redirection.
# you have been warned.
import numpy

# Raise exceptions instead of issuing warnings
numpy.seterr(all='raise')

del numpy
# End of numpy configuration

# Class definitions
class Color(object):
    def __init__(self, BGR):
        self._b = BGR[0]
        self._g = BGR[1]
        self._r = BGR[2]

    @property
    def b(self):
        return int(self._b)

    @property
    def g(self):
        return int(self._g)

    @property
    def r(self):
        return int(self._r)

    def __repr__(self):
        return f"Color(r={self.r}, g={self.g}, b={self.b})"

class Image(object):
    def at(self, y, x):
        return self.image[y][x]

    def __init__(self, image):
        self.size_x = image.shape[1]
        self.size_y = image.shape[0]
        self.image = [[Color(image[y, x]) for x in range(self.size_x)] for y in range(self.size_y)]

    def __repr__(self):
        return f"Image(size_x={self.size_x}, size_y={self.size_y})"

# JSON response dictionary
__app_response__ = {
    "balls": [],
    "stdout": ""
}

# This is intended to be used by the, uh, user
def get_ball_image():
    import cv2
    im = cv2.imread("public/test.png")
    del cv2

    return Image(im)

def plot_ball(y, x):
    max_balls = 100
    try:
        if len(__app_response__["balls"]) == max_balls:
            return
        x = int(x)
        y = int(y)

        __app_response__["balls"].append({"y": y, "x": x})

        print(f"Ball has been plotted to y={y}, x={x}")
        if len(__app_response__["balls"]) == max_balls:
            print("Max number of balls (max_balls) reached!")
            return
    except ValueError:
        print("plot_ball(x, y) expects integers >:/")
