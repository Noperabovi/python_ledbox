from python_ledbox.TerminalMatrix import TerminalMatrix
from python_ledbox.PiMatrix import PiMatrix
from python_ledbox.Frames import Frame
from python_ledbox import Color
import time

import random


pi = PiMatrix(10, 10, 18)
tm = TerminalMatrix(10, 10)

frame = Frame(10, 10)

while True:
    for row in range(10):
        for col in range(10):
            frame[row, col] = Color.from_rgb(random.randint(0,255), random.randint(0,255), random.randint(0,255))

    tm.applyMap(frame.getMap())
    time.sleep(1)




try:
    while True:
        time.sleep(3600)
except KeyboardInterrupt:
    tm.clear()
    time.sleep(2)
