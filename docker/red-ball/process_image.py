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

def plot_ball(image, x, y):
    def draw_pixel(image, x, y):
        image.at(x, y)._b = 0
        image.at(x, y)._g = 0
        image.at(x, y)._r = 0
    
    draw_pixel(image, x, y)
    draw_pixel(image, x+1, y)
    draw_pixel(image, x+2, y)
    draw_pixel(image, x+3, y)
    draw_pixel(image, x+4, y)
    draw_pixel(image, x+5, y)
    draw_pixel(image, x+6, y)
    draw_pixel(image, x+7, y)
    draw_pixel(image, x, y+1)
    draw_pixel(image, x, y+2)
    draw_pixel(image, x, y+3)
    draw_pixel(image, x, y+4)
    draw_pixel(image, x, y+5)
    draw_pixel(image, x, y+6)
    draw_pixel(image, x, y+7)
    draw_pixel(image, x+1, y+1)
    draw_pixel(image, x+2, y+2)
    draw_pixel(image, x+3, y+3)
    draw_pixel(image, x+4, y+4)
    draw_pixel(image, x+5, y+5)
    draw_pixel(image, x+6, y+6)
    draw_pixel(image, x+7, y+7)
    draw_pixel(image, x+8, y+8)
    draw_pixel(image, x+9, y+9)
    draw_pixel(image, x+10, y+10)
    draw_pixel(image, x+11, y+11)
    draw_pixel(image, x+12, y+12)
    
    print(f"Ball has been plotted to x={x}, y={y}")

print("Hello, world!")

# Get a reference to the image above
image = get_ball_image()
print(image)

# Pixel [0, 0] has a red value of 166
print(image.at(x=0, y=0).r)

# Draw a cursor onto the image at position [2, 3]
plot_ball(image, x=2, y=3)

write_ball_image(image)
