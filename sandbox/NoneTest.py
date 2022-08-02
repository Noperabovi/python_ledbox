from python_ledbox import Frames, TerminalMatrix, Images
from python_ledbox import Color

import os

import random
import time


if __name__ == "__main__":

    m = TerminalMatrix.TerminalMatrix(10, 10)

    frame1 = Frames.Frame(10, 10)
    frame1[0, 0] = Color.from_rgb(255, 0, 0)
    m.applyMap(frame1.getMap())

    time.sleep(1)

    frame1[0, 0] = None
    m.applyMap(frame1.getMap())

    # time.sleep(10)
