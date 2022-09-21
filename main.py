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
    hour_first_digit_color=Color.from_rgb(67, 17, 127),
    hour_second_digit_color=Color.from_rgb(40, 10, 76),
    minute_first_digit_color=Color.from_rgb(6, 41, 95),
    minute_second_digit_color=Color.from_rgb(2, 18, 44),
)

mainapp = MainApp(matrix, main_app_queue, [clockapp])

mainapp.start()


time.sleep(1000)
