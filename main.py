from ast import main
from python_ledbox.apps import MainApp, ClockApp
from python_ledbox.Matrix import Matrix
from python_ledbox.TerminalMatrix import TerminalMatrix
from python_ledbox.PiMatrix import PiMatrix
from python_ledbox.events import Signal, MouseEvent
from python_ledbox import Color
import time

from queue import Queue

# matrix: Matrix = TerminalMatrix(10, 10)
matrix: Matrix = PiMatrix(10, 10, pin=18)

main_app_queue: Queue[Signal] = Queue()


clockapp = ClockApp(
    matrix.createFrame(),
    main_app_queue,
    MouseEvent.MOUSE_CLICK_LEFT,
    hour_first_digit_color=Color.pink,
    hour_second_digit_color=Color.greenyellow,
    minute_first_digit_color=Color.orangered,
)

mainapp = MainApp(matrix, main_app_queue, [clockapp])

mainapp.start()


time.sleep(100)
