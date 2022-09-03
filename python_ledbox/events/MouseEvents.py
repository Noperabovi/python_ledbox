from Events import Event, EventManager
from threading import Thread
import atexit


class MouseEvent(Event):
    MOUSE_CLICK_LEFT = 1
    MOUSE_CLICK_RIGHT = 2


def startListening():

    mouse = open("/dev/input/mouse0", "rb")

    x = 0
    y = 0

    while True:
        status, dx, dy = tuple(c for c in mouse.read(3))

        left = status & 0x1
        right = status & 0x2
        middle = status & 0x4

        if left:
            EventManager.dispatch(MouseEvent.MOUSE_CLICK_LEFT)
        if right:
            EventManager.dispatch(MouseEvent.MOUSE_CLICK_RIGHT)

    print("listener killed")


mouseThread: Thread = Thread(target=startListening, daemon=True)
mouseThread.start()
atexit.register(lambda: print("exiting mouse event module"))
