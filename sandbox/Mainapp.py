from ast import main
from typing import Counter, Dict
from python_ledbox.App import App
from python_ledbox.PiMatrix import PiMatrix
from python_ledbox.TerminalMatrix import TerminalMatrix
from python_ledbox.apps.ClockApp import ClockApp
from threading import Thread
import threading
import logging
import time
import atexit
import signal

from python_ledbox.Matrix import Matrix
from python_ledbox.events import MouseEvents


logging.basicConfig(level=logging.INFO)


class MainApp(App):
    def __init__(self, matrix: Matrix):
        super().__init__()
        self.matrix: Matrix = matrix
        self.counter: int = 0
        self.clockapp = ClockApp(self.matrix, self.matrix.createFrame())

    def start(self) -> None:
        super().start()
        logging.info("Starting main app")
        self.clockapp.start()
        self.apploop()

    def kill(self) -> None:
        super().kill()
        print(f"active threads: {threading.active_count()}")
        self.clockapp.stop()
        print(f"active threads: {threading.active_count()}")
        logging.info("Klling main app")

    def apploop(self) -> None:
        MouseEvents.startListening()
        while self.isActive():
            time.sleep(10)
            # changes: Dict[int, int] = self.clockapp.frame.getChanges()
            # if len(changes) != 0:
            #     self.matrix.applyChanges(changes)

        print("mainapp killed")
        # time.sleep(0.1)


if __name__ == "__main__":
    # matrix: Matrix = TerminalMatrix(10, 10)
    matrix: Matrix = PiMatrix(10, 10, 18)
    mainapp: MainApp = MainApp(matrix)

    mainappthread: Thread = Thread(target=mainapp.start, daemon=True)
    print("hello")

    atexit.register(mainapp.kill)

    mainappthread.start()
    time.sleep(100)
