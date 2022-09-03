from queue import Queue
from python_ledbox.events import Signal, MouseEvent, EventManager


if __name__ == "__main__":
    from queue import Queue

    myQueue: Queue[Signal] = Queue()

    EventManager.addListener(MouseEvent.MOUSE_CLICK_LEFT, myQueue)

    # mouseThread: Thread = Thread(target=startListening, daemon=True)
    # mouseThread.start()

    while True:
        myval = myQueue.get()
        print(myval)
