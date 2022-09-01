from concurrent.futures import thread
from .Events import Event, EventManager
from threading import Thread
import atexit
import time


stop = False

# this seems to be useless
# def kill():
#     stop = True
#     print("klling listenener")


def startListening():

    mouse = open("/dev/input/mouse0", "rb")

    x = 0
    y = 0

    while not stop:
        status, dx, dy = tuple(c for c in mouse.read(3))

        left = status & 0x1
        right = status & 0x2
        middle = status & 0x4

        if left:
            EventManager.dispatch(Event.MOUSE_CLICK_LEFT)
        if right:
            EventManager.dispatch(Event.MOUSE_CLICK_RIGHT)

    print("listener killed")


if __name__ == "__main__":

    def rightClickHandler():
        print("right mouse button clicked")

    def leftClickHandler():
        print("left mouse button clicked")

    EventManager.addListener(Event.MOUSE_CLICK_RIGHT, rightClickHandler)
    EventManager.addListener(Event.MOUSE_CLICK_LEFT, leftClickHandler)

    mouseThread: Thread = Thread(target=startListening, daemon=True)
    mouseThread.start()

    # atexit.register(kill)

    time.sleep(5)
    # kill()
    time.sleep(5)
