from typing import Tuple
from datetime import datetime
import time

from threading import Thread

from python_ledbox import Color
from python_ledbox.App import App
from python_ledbox.Images import ImageLoader, Image
from python_ledbox.Frames import Frame
from python_ledbox.Matrix import Matrix
from python_ledbox.events import Event, EventManager


class ClockApp(App):
    def __init__(self, matrix: Matrix, frame: Frame):
        super().__init__()

        self.matrix = matrix
        self.__frame = frame
        self.__imageLoader = ImageLoader()
        self.__imageLoader.load("python_ledbox/images/numerals/")

        self.hour_first_digit_pos: Tuple[int, int] = (0, 0)
        self.hour_second_digit_pos: Tuple[int, int] = (0, 7)
        self.minute_first_digit_pos: Tuple[int, int] = (5, 0)
        self.minute_second_digit_pos: Tuple[int, int] = (5, 7)

        self.hour_first_digit_color: int = Color.red
        self.hour_second_digit_color: int = Color.red
        self.minute_first_digit_color: int = Color.red
        self.minute_second_digit_color: int = Color.red

        EventManager.addListener(Event.MOUSE_CLICK_LEFT, self.__displayTime)
        self._isInitialised = True  # no initialization necessary

    def __updateTime(self, time: datetime) -> None:

        hour_first_digit = self.__imageLoader.get(str(time.hour // 10))
        hour_second_digit = self.__imageLoader.get(str(time.hour % 10))
        minute_first_digit = self.__imageLoader.get(str(time.minute // 10))
        minute_second_digit = self.__imageLoader.get(str(time.minute % 10))

        hour_first_digit.applyToFrame(
            self.__frame,
            self.hour_first_digit_pos[0],
            self.hour_first_digit_pos[1],
            {0: self.hour_first_digit_color},
        )

        hour_second_digit.applyToFrame(
            self.__frame,
            self.hour_second_digit_pos[0],
            self.hour_second_digit_pos[1],
            {0: self.hour_second_digit_color},
        )

        minute_first_digit.applyToFrame(
            self.__frame,
            self.minute_first_digit_pos[0],
            self.minute_first_digit_pos[1],
            {0: self.minute_first_digit_color},
        )

        minute_second_digit.applyToFrame(
            self.__frame,
            self.minute_second_digit_pos[0],
            self.minute_second_digit_pos[1],
            {0: self.minute_second_digit_color},
        )

        # self.matrix.applyChanges(self.__frame.getChanges())

    def __displayTime(self) -> None:
        self.matrix.applyChanges(self.__frame.getChanges())
        time.sleep(5)
        self.matrix.clear()

    def __timeLoop(self) -> None:

        minute: int = None

        while self.isActive():
            now = datetime.now()
            if now.minute != minute:
                self.__updateTime(now)
                minute = now.minute
            time.sleep(1)

    def start(self):
        super().start()
        Thread(target=self.__timeLoop, daemon=True).start()
