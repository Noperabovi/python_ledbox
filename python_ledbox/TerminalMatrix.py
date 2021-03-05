from typing import Dict

from sty import bg, rs

from python_ledbox.Matrix import Matrix
from python_ledbox import Color


class TerminalMatrix(Matrix):
    def __init__(self, rows: int, cols: int):
        super().__init__(rows, cols)

        self.__colorList: int = [None] * rows * cols
        print("\n" * (rows))  # create enough space below prompt

    def applyChanges(self, changes: Dict[int, int]) -> None:
        """Apply given changes to the matrix."""

        self.applyMap(changes)

    def applyMap(self, map: Dict[int, int]) -> None:
        """Apply entire frame-map to the matrix."""

        for key, value in map.items():

            entry = None

            if value is not None:
                entry = bg(*Color.to_rgb(value)) + "  " + rs.bg

            self.__colorList[key] = entry

        self.__printMatrix()

    def __printMatrix(self):

        i = 0
        print("\033[F" * (self.ROWS + 1))

        for row in range(self.ROWS):
            line = ""
            for col in range(self.COLS):

                color = self.__colorList[i]

                # line += color + rs.bg if color != None else " "
                if color is None:
                    line += "  "
                else:
                    line += color  # + rs.bg

                i += 1

            print(line)

        # jump back to start
