import re
import math
from enum import Enum
import numpy as np
from PIL import Image, ImageDraw

# region CustomMath
class CustomMath:
    @staticmethod
    def multiply(a: tuple, b: tuple) -> tuple: return tuple(np.multiply(a, b))
    @staticmethod
    def divide(a: tuple, b: tuple) -> tuple: return tuple(np.divide(a, b))

cm = CustomMath
# endregion

# region Model
class ModelViewData:
    def __init__(self): ...

class Model:
    def __init__(self, view):
        self.view = view

    def manipulate(self, command):
        view_data = ModelViewData()
        self.view.update(view_data)
# endregion

# region View
class ViewColors:
    bg = (242, 247, 161, 255)
    border = (70, 194, 203, 255)
    cell_border = (70, 194, 203, 255)
    cell_bg0 = (130, 205, 71, 255)
    cell_bg1 = (84, 180, 53, 255)

class View:
    field_size = (10, 10)
    cell_size_px = (50, 50)

    main_image_source = 'images/main.png'
    field_image_source = 'images/field.png'
    field_image_lines_width_px = 10
    field_border_width_px = 10

    @staticmethod
    def draw_broken_line(draw, points, fill=None, width=0):
        for i in range(len(points) - 1):
            draw.line((points[i][0], points[i][1], points[i+1][0], points[i+1][1]), fill=fill, width=width)

    @staticmethod
    def draw_border(draw, image_size, fill=None, width=0):

        View.draw_broken_line(
            draw,
            (
                (0, 0),
                (0, image_size[1]),
                (image_size[0], image_size[1]),
                (image_size[0], 0),
                (0, 0)
            ),
            fill=fill,
            width=width * 2
        )

    def draw_field_image(self):
        field_image = Image.new(mode="RGBA", size=self.field_size_px)
        draw = ImageDraw.Draw(field_image)

        a = cm.divide(field_image.size, self.field_size)
        for x in range(self.field_size[0]):
            for y in range(self.field_size[1]):
                x_px, y_px = x*a[0], y*a[1]
                cell_bg_color = ViewColors.cell_bg0 if (x + y) % 2 == 0 else ViewColors.cell_bg1
                draw.rectangle((x_px, y_px, x_px+a[0], y_px+a[1]), cell_bg_color)

        def line(xy): draw.line(xy, ViewColors.cell_border, self.field_image_lines_width_px)
        distance_between_lines = cm.divide(field_image.size, self.field_size)
        for x in range(self.field_size[0] - 1):
            position_x = x * distance_between_lines[0] + distance_between_lines[0]
            line((position_x, 0, position_x, field_image.size[1]))
        for y in range(self.field_size[1] - 1):
            position_y = y * distance_between_lines[1] + distance_between_lines[1]
            line((0, position_y, field_image.size[0], position_y))

        View.draw_border(draw, field_image.size, ViewColors.border, self.field_border_width_px)
        return field_image

    def draw_main_image(self):
        main_image = Image.new(mode="RGBA", size=self.field_size_px, color=ViewColors.bg)
        return main_image

    def __init__(self):
        self.field_size_px = cm.multiply(self.cell_size_px, self.field_size)
        self.field_image = self.draw_field_image()
        self.main_image = self.draw_main_image()
        self.main_image.save(self.main_image_source)

    def update(self, data):
        print(f'png {data}')
        # self.main_image.show()
        self.field_image.show()

# endregion

# region Controller
class ControllerBase:
    def __init__(self, model):
        self.model = model

class ControllerConsole(ControllerBase):
    def __init__(self, model):
        super().__init__(model)
        while True:
            command = input('Your command: ')
            self.model.manipulate(command)
# endregion

# region Main
def main():
    view = View()
    # model = Model(view)
    # controller = ControllerConsole(model)

    view.update(...)
if __name__ == '__main__': main()
# endregion
