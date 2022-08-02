from python_ledbox import Frames, TerminalMatrix
from python_ledbox import Color

import random
import time


if __name__ == "__main__":

    m = TerminalMatrix.TerminalMatrix(10, 10)

    frame1 = Frames.Frame(10, 10)

    def generateNoise():

        for i in range(0, 10):
            for j in range(0, 10):
                r = random.randint(0, 256)
                b = random.randint(0, 256)
                g = random.randint(0, 256)
                frame1[i, j] = Color.from_rgb(r, g, b)

        m.applyMap(frame1.getMap())

    generateNoise()
    time.sleep(1)
    generateNoise()
    time.sleep(1)
    generateNoise()
    time.sleep(1)
    generateNoise()
