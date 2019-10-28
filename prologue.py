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

# Class definitions
class Color(object):
    def __init__(self, BGR):
        self.b = BGR[0]
        self.g = BGR[1]
        self.r = BGR[2]

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
    "ball": {"y": 0, "x": 0},
    "stdout": ""
}

# This is intended to be used by the, uh, user
def get_ball_image():
    import cv2
    im = cv2.imread("public/test.png")
    del cv2

    return Image(im)

def plot_ball(y, x):
    try:
        x = int(x)
        y = int(y)
    except ValueError:
        print("plot_ball(x, y) expects integers >:/")

    __app_response__["ball"] = {"y": y, "x": x}

    print(f"Ball has been plotted to y={y}, x={x}")
