import cv2
import numpy

IMAGE_PATH = "red-ball.png"

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
    
    @property
    def bgr(self):
        return [self._b, self._g, self._r]

    def __repr__(self):
        return f"Color(r={self.r}, g={self.g}, b={self.b})"

class Image(object):
    def at(self, x, y):
        return self.image[y][x]

    def __init__(self, image):
        self.width = image.shape[1]
        self.height = image.shape[0]
        self.image = [[Color(image[y, x]) for x in range(self.width)] for y in range(self.height)]
    
    @property
    def as_numpy(self):
        return numpy.array([[self.at(x, y).bgr for x in range(self.width)] for y in range(self.height)])

    def __repr__(self):
        return f"Image(width={self.width}, height={self.height})"

def get_ball_image():
    im = cv2.imread("red-ball.png")
    if im is None:
        raise Exception(f"invalid image 'red-ball.png'")

    return Image(im)

def write_ball_image(image):
    cv2.imwrite("/data/output.png", image.as_numpy)

def plot_ball_detection(image, x, y, radius, r, g, b):
    # Bresenham Circle Drawing
    def draw_pixel(x, y):
        if x>=0 and y>=0 and x<=image.width and y<image.height:
            image.at(x, y)._r = r
            image.at(x, y)._b = b
            image.at(x, y)._g = g
    def draw_bresenham_pixel_in_all_octants(xc, yc, x, y):
        draw_pixel(xc+x, yc+y)
        draw_pixel(xc-x, yc+y)
        draw_pixel(xc+x, yc-y)
        draw_pixel(xc-x, yc-y)
        draw_pixel(xc+y, yc+x)
        draw_pixel(xc-y, yc+x)
        draw_pixel(xc+y, yc-x)
        draw_pixel(xc-y, yc-x)
    xc = x
    yc = y
    x = 0
    y = radius
    d = 3 - (2 * radius)
    
    # draw starting pixel for each quadrant
    draw_pixel(xc+y, yc)
    draw_pixel(xc, yc+y)
    draw_pixel(xc-y, yc)
    draw_pixel(xc, yc-y)
    
    while y >= x:
        x += 1
        if d > 0:
            y -= 1
            d = d + 4 * (x - y) + 10
        else:
            d = d + 4 * x + 6
        draw_bresenham_pixel_in_all_octants(xc, yc, x, y)
    print(f"Ball-detection with radius={radius} has been plotted to x={xc}, y={yc}")
