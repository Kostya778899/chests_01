import dataclasses
import re
import math
from enum import Enum
from dataclasses import dataclass
import numpy as np
from PIL import Image, ImageDraw

DEBUG_MODE = True

# region CustomMath
class CustomMath:
    @staticmethod
    def add(a: tuple, b) -> tuple: return tuple(np.add(a, b))
    @staticmethod
    def subtract(a: tuple, b) -> tuple: return tuple(np.subtract(a, b))
    @staticmethod
    def multiply(a: tuple, b) -> tuple: return tuple(np.multiply(a, b))
    @staticmethod
    def divide(a: tuple, b) -> tuple: return tuple(np.divide(a, b))

cm = CustomMath
# endregion

# region Model
@dataclass
class ModelViewData:
    chests: list


class Model:
    # region Chests
    class ChestBase:
        def __init__(self, player_index, position, direction):
            self.player_index = player_index
            self.position = position
            self.direction = direction

        def get_moves(self, occupied_positions): ...

    class Pawn(ChestBase):
        # def __init__(self, identifier, direction):
        #     super().__init__(identifier, direction)

        def get_moves(self, occupied_positions):
            moves = []
            for position in ((1, 1), (-1, 1)):
                if position not in occupied_positions: moves.append(position)
            return moves

    class Queen(ChestBase): ...
    # endregion

    chests = [Pawn(0, (1, 0), (0, -1)), Pawn(0, (3, 0), (0, -1))]

    def __init__(self, view):
        self.view = view

        self.view.update(ModelViewData(self.chests))

    def manipulate(self, command):
        self.view.update(ModelViewData(self.chests))
# endregion

# region View
class ViewColors:
    bg = (242, 247, 161, 255)
    cell_bg0 = (130, 205, 71, 255)
    cell_bg1 = (84, 180, 53, 255)

class ViewImages:
    chest0 = Image.open('images/pawn_00.png')

class View:
    # field_size = (10, 10)
    chest_size_by_cell = 0.8

    main_image_source = 'images/main.png'
    field_image_source = 'images/field.png'

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

    def draw_field_image(self, size):
        field_image = Image.new(mode="RGBA", size=size)
        draw = ImageDraw.Draw(field_image)

        for x in range(self.field_size[0]):
            for y in range(self.field_size[1]):
                xy_px = cm.multiply(self.cell_size_px, (x, y))
                cell_bg_color = ViewColors.cell_bg0 if (x + y) % 2 == 0 else ViewColors.cell_bg1
                draw.rectangle(
                    (xy_px[0], xy_px[1], xy_px[0]+self.cell_size_px[0], xy_px[1]+self.cell_size_px[1]),
                    cell_bg_color
                )

        return field_image

    # def draw_main_image(self):
    #     main_image = Image.new(mode="RGBA", size=self.field_image.size, color=ViewColors.bg)
    #     return main_image

    def __init__(self, field_size):
        field_size_px = (512, 512)

        self.field_size = field_size
        self.cell_size_px = cm.divide(field_size_px, self.field_size)
        self.field_image = self.draw_field_image(size=field_size_px)

        ViewImages.chest0.thumbnail(cm.multiply(self.cell_size_px, self.chest_size_by_cell))

        if DEBUG_MODE: ViewImages.chest0 = Image.eval(ViewImages.chest0, lambda x: x + 100)

    def update(self, data: ModelViewData):
        out_image = self.field_image

        chest_of_cell_center_px = cm.divide(cm.subtract(self.cell_size_px, ViewImages.chest0.size), 2)
        for chest in data.chests:
            position_px = cm.add(cm.multiply(chest.position, self.cell_size_px), chest_of_cell_center_px)
            out_image.alpha_composite(ViewImages.chest0, tuple(map(int, position_px)))

        out_image.show()

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
    view = View((4, 4))
    model = Model(view)
    controller = ControllerConsole(model)
if __name__ == '__main__': main()
# endregion
