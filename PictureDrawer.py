from python_ledbox import Frames, TerminalMatrix, Images, PiMatrix
from python_ledbox import Color

from python_ledbox.apps.ClockApp import ClockApp
from python_ledbox.apps.PingSwitchApp import PingSwitchApp

import os

import random
import time


if __name__ == "__main__":

    # pics = Images.ImageLoader()

    try:
        terminalMatrix = TerminalMatrix.TerminalMatrix(10, 10)
        piMatrix = PiMatrix.PiMatrix(10, 10, 18)
        frame = Frames.Frame(10, 10)

        # setup clock app
        clockApp = ClockApp(piMatrix, frame)

        clockApp.hour_first_digit_pos = (0, 2)
        clockApp.hour_second_digit_pos = (0, 5)
        clockApp.minute_first_digit_pos = (5, 2)
        clockApp.minute_second_digit_pos = (5, 5)

        clockApp.hour_first_digit_color = Color.from_rgb(52, 235, 195)
        clockApp.hour_second_digit_color = Color.from_rgb(52, 174, 235)
        clockApp.minute_first_digit_color = Color.from_rgb(95, 52, 235)
        clockApp.minute_second_digit_color = Color.from_rgb(52, 58, 235)

        # night colors
        # clockApp.hour_first_digit_color = Color.from_rgb(10, 0, 0)
        # clockApp.hour_second_digit_color = Color.from_rgb(10, 0, 2)
        # clockApp.minute_first_digit_color = Color.from_rgb(10, 0, 2)
        # clockApp.minute_second_digit_color = Color.from_rgb(10, 0, 0)

        # settup pingswitch

        pingswitch = PingSwitchApp("192.168.1.69")

        pingswitch.apps = [clockApp]
        pingswitch.startDelay = 0
        pingswitch.stopDelay = 120
        pingswitch.pingInterval = 30

        pingswitch.start()

        while True:
            time.sleep(3600)

    except KeyboardInterrupt:
        piMatrix.clear()
        clockApp.stop()
