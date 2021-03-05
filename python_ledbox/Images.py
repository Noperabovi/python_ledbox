from typing import List, Dict, Tuple
import os, os.path

from PIL import Image as PillowImage
from PIL.Image import Image as PillowImageObject

from python_ledbox.Frames import Frame
from python_ledbox import Color


class ImageLoader:

    __validImages: Tuple = (".jpg", ".gif", ".png", ".tga", ".bmp")

    def __init__(self):
        self.__images: Dict[str, PillowImageObject] = {}

    def load(self, filePath: str, overwrite=False) -> None:
        """Load image file or files from directory, throw exception if image with same name already exists, or could not be found."""

        def loadImageFromFile(filePath: str) -> None:
            """Runs checks, loads and saves image"""

            # evaluate name of image
            imageName = os.path.splitext(os.path.split(filePath)[1])[0]

            # check if name already exists, ignore if overwrite = True
            if imageName in self.__images.keys() and not overwrite:
                raise ValueError(f'Image with filename "{imageName}" already loaded.')

            # check if file has right format
            if os.path.splitext(filePath)[1].lower() not in ImageLoader.__validImages:
                raise ValueError(
                    f'Image file format "{os.path.splitext(filePath)[1].lower().lower()}" not supported.'
                )

            # load image from file and create Image object in RGBA format
            self.__images[imageName] = Image(
                PillowImage.open(filePath).convert("RGBA"),
                imageName,
            )

        if not os.path.isdir(filePath):
            loadImageFromFile(filePath)
        else:
            for f in os.listdir(filePath):
                loadImageFromFile(os.path.join(filePath, f))

    def get(self, imageName: str) -> PillowImage:
        """Get loaded file by imageName, returns None if image with name is not loaded."""

        return self.__images.get(imageName)


class Image:
    def __init__(self, image: PillowImage, name: str):
        self.image = image
        self.name = name

    def getRowCount(self) -> int:
        """Returns number of rows."""
        return self.image.height

    def getColCount(self) -> int:
        """Returns number of cols."""
        return self.image.width

    def getPillowImage(self) -> PillowImage:  # pragma: no cover
        """Returns Pillow Image object of this instance."""
        return self.image

    def applyToFrame(
        self, frame: Frame, row: int, col: int, recolor: Dict[int, int] = None
    ) -> None:
        """Applies this image to frame at given position, colors may be changed."""

        # calculate start and stop coordinates
        col_start = max(0, -col)
        row_start = max(0, -row)
        col_end = min(self.image.width, frame.COLS - col)
        row_end = min(self.image.height, frame.ROWS - row)

        for x in range(row_start, row_end):

            for y in range(col_start, col_end):

                color = self.image.getpixel((y, x))
                int_color = Color.from_rgb(*color[0:3])

                # fully transparent if not completly opaque
                if color[3] < 255:
                    int_color = None

                # recolor if necessary
                if recolor and int_color in recolor.keys():
                    int_color = recolor[int_color]

                frame[x + row, y + col] = int_color
