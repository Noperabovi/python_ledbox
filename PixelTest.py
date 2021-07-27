from python_ledbox.TerminalMatrix import TerminalMatrix
from python_ledbox.PiMatrix import PiMatrix
from python_ledbox.Frames import Frame
from python_ledbox import Color
import time


pi = PiMatrix(10, 10, 18)
tm = TerminalMatrix(10, 10)

frame = Frame(10, 10)


for row in range(10):
    for col in range(10):
        frame[row, col] = Color.goldenrod


pi.applyMap(frame.getMap())


try:
    while True:
        time.sleep(3600)
except KeyboardInterrupt:
    pi.clear()
    time.sleep(2)
