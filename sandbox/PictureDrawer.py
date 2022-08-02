from python_ledbox import Frames, TerminalMatrix, Images
from python_ledbox import Color

import os

import random
import time


if __name__ == "__main__":

    pics = Images.ImageLoader()

    try:
        # print(os.listdir("."))
        pics.load(".vscode/images/")
    except Exception as e:
        print(e)

    m = TerminalMatrix.TerminalMatrix(800, 600)

    frame1 = Frames.Frame(800, 600)

    recolor = {}
    recolor[Color.black] = Color.cornflowerblue

    pics.get("felix").applyToFrame(frame1, 0, 0, recolor)

    m.applyMap(frame1.getMap())

    # time.sleep(10)
