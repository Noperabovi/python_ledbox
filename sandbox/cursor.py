from python_ledbox.TerminalMatrix import TerminalMatrix
from python_ledbox.Frames import Frame
from python_ledbox import Color

import sys

mouse = open("/dev/input/mouse0", "rb")



tm = TerminalMatrix(10, 10)
frame = Frame(10, 10)

x = 0
y = 0

while True:
    status, dx, dy = tuple(c for c in mouse.read(3))

    def to_signed(n):
        return n - ((0x80 & n) << 1)

    dx = to_signed(dx)
    dy = to_signed(dy)

    left = status & 0x1
    right = status & 0x2
    middle = status & 0x4

    # remember old location to remove cursor
    lx = x
    ly = y

    # update position
    if(x+dx > 999):
        x = 999
    elif(x+dx < 0):
        x = 0
    else:
        x = x+dx

    if(y-dy > 999):
        y = 999
    elif(y-dy < 0):
        y = 0
    else:
        y = y-dy


    frame[ly//100,lx//100] = None
    frame[y//100,x//100] = Color.red

    tm.applyChanges(frame.getChanges())
