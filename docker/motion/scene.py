import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont
import pathlib
import pymunk
import typing


class Scene:

    def __init__(self, width: float, height: float, scale: float, background='#eee'):
        self.width = width
        self.height = height
        self.scale = scale
        self.background = background
        self.image = PIL.Image.new('RGB', (int(self.width * self.scale),
                                           int(self.height * self.scale)), self.background)
        self.draw = PIL.ImageDraw.ImageDraw(self.image, mode='RGBA')
        self.font = PIL.ImageFont.truetype('JetBrainsMono-Regular.ttf', 14)

    def _pymunk_to_pillow(self, point: pymunk.Vec2d):
        return pymunk.Vec2d(
            int(point[0] * self.scale),
            int((self.height * self.scale) - (point[1] * self.scale)),
        )

    def draw_line(self, a: pymunk.Vec2d, b: pymunk.Vec2d, width: float, fill: typing.Union[str, tuple]):
        self.draw.line(
            (self._pymunk_to_pillow(a), self._pymunk_to_pillow(b)),
            fill=fill,
            width=int(width * self.scale),
        )

    def draw_circle(self, center: pymunk.Vec2d, radius: float, fill: typing.Union[str, tuple]):
        radius_vector = pymunk.Vec2d(radius, radius) * self.scale
        self.draw.ellipse([
            self._pymunk_to_pillow(center) - radius_vector,
            self._pymunk_to_pillow(center) + radius_vector,
        ], fill=fill)

    def draw_text(self, text: str, upper_left: pymunk.Vec2d, fill: typing.Union[str, tuple], anchor='ls'):
        self.draw.multiline_text(
            self._pymunk_to_pillow(upper_left),
            text,
            font=self.font,
            fill=fill,
            anchor=anchor,
        )

    def save_png(self, path: pathlib.Path):
        self.image.save(path)
