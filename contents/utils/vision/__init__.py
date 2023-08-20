from typing import Literal
import cv2
import matplotlib.pyplot  # type: ignore
import numpy

IMAGE_PATH = "utils/vision/red_ball.png"


class Color:
    def __init__(
        self, bgr: numpy.ndarray[tuple[Literal[3]], numpy.dtype[numpy.int8]]
    ) -> None:
        self._b = int(bgr[0])
        self._g = int(bgr[1])
        self._r = int(bgr[2])

    @property
    def b(self) -> int:
        return self._b

    @property
    def g(self) -> int:
        return self._g

    @property
    def r(self) -> int:
        return self._r

    @property
    def bgr(self) -> list[int]:
        return [self._b, self._g, self._r]

    def __repr__(self) -> str:
        return f"Color(r={self.r}, g={self.g}, b={self.b})"


class Image:
    def __init__(
        self, image: numpy.ndarray[tuple[int, int, Literal[3]], numpy.dtype[numpy.int8]]
    ):
        self._width = image.shape[1]
        self._height = image.shape[0]
        self._image = [
            [Color(image[y, x]) for x in range(self._width)]
            for y in range(self._height)
        ]

    def at(self, x: int, y: int) -> Color:
        return self._image[y][x]

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    def as_numpy(
        self,
    ) -> numpy.ndarray[tuple[int, int, Literal[3]], numpy.dtype[numpy.int8]]:
        return numpy.array(
            [
                [self.at(x, y).bgr for x in range(self._width)]
                for y in range(self._height)
            ]
        )

    def __repr__(self) -> str:
        return f"Image(width={self._width}, height={self._height})"

    def show(self) -> None:
        matplotlib.pyplot.imshow(self.as_numpy()[:, :, [2, 1, 0]])


def get_ball_image() -> Image:
    im = cv2.imread(IMAGE_PATH)
    if im is None:
        raise Exception(f"invalid image '{IMAGE_PATH}'")

    return Image(im)


def plot_ball_detection(
    image: Image, x: int, y: int, radius: int, r: int, g: int, b: int
) -> None:
    # Bresenham Circle Drawing
    def draw_pixel(x: int, y: int) -> None:
        if x >= 0 and y >= 0 and x <= image.width and y < image.height:
            image.at(x, y)._r = r
            image.at(x, y)._b = b
            image.at(x, y)._g = g

    def draw_bresenham_pixel_in_all_octants(xc: int, yc: int, x: int, y: int) -> None:
        draw_pixel(xc + x, yc + y)
        draw_pixel(xc - x, yc + y)
        draw_pixel(xc + x, yc - y)
        draw_pixel(xc - x, yc - y)
        draw_pixel(xc + y, yc + x)
        draw_pixel(xc - y, yc + x)
        draw_pixel(xc + y, yc - x)
        draw_pixel(xc - y, yc - x)

    xc = x
    yc = y
    x = 0
    y = radius
    d = 3 - (2 * radius)

    # draw starting pixel for each quadrant
    draw_pixel(xc + y, yc)
    draw_pixel(xc, yc + y)
    draw_pixel(xc - y, yc)
    draw_pixel(xc, yc - y)

    while y >= x:
        x += 1
        if d > 0:
            y -= 1
            d = d + 4 * (x - y) + 10
        else:
            d = d + 4 * x + 6
        draw_bresenham_pixel_in_all_octants(xc, yc, x, y)
    print(f"Ball-detection with radius={radius} has been plotted to x={xc}, y={yc}")
