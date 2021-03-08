from rpi_ws281x import PixelStrip
from typing import Dict

from python_ledbox.Matrix import Matrix


class PiMatrix(Matrix):
    def __init__(
        self,
        rows: int,
        cols: int,
        pin: int,
        freq_hz: int = 800000,
        dma: int = 10,
        invert: bool = False,
        brightness: int = 255,
        channel: int = 0,
        strip_type=None,
        gamma=None,
    ):
        super().__init__(rows, cols)
        self.__pixelStrip = PixelStrip(
            rows * cols,
            pin,
            freq_hz,
            dma,
            invert,
            brightness,
            channel,
            strip_type,
            gamma,
        )
        self.__pixelStrip.begin()

    def applyChanges(self, changes: Dict[int, int]) -> None:
        """Apply given changes to the matrix."""

        self.applyMap(changes)

    def applyMap(self, map: Dict[int, int]) -> None:
        """Apply entire frame-map to the matrix."""

        for led_num, color in map.items():
            if color is None:
                color = 0

            self.__pixelStrip.setPixelColor(led_num, color)

        self.__pixelStrip.show()

    def clear(self) -> None:
        """Turn off all pixels."""

        for i in range(self.COLS * self.ROWS):
            self.__pixelStrip.setPixelColor(i, 0)

        self.__pixelStrip.show()
