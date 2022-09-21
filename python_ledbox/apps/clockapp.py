from python_ledbox.App import App
from python_ledbox.Frames import Frame
from python_ledbox.events import Signal, Event, EventManager
from python_ledbox.Matrix import MatrixEvent
from python_ledbox.events import AppEvent
from python_ledbox.Images import ImageLoader, Image
from python_ledbox import Color

from queue import Queue, Empty as QueueEmptyException
from datetime import datetime, timedelta
import logging


class ClockApp(App):
    """App for temporarily displaying time on given event."""

    def __init__(
        self,
        frame: Frame,
        matrixQueue: Queue[Signal],
        show_time_event: Event,
        display_duration: int = 5,
        hour_first_digit_pos=(0, 2),
        hour_second_digit_pos=(0, 5),
        minute_first_digit_pos=(5, 2),
        minute_second_digit_pos=(5, 5),
        hour_first_digit_color=Color.red,
        hour_second_digit_color=Color.red,
        minute_first_digit_color=Color.red,
        minute_second_digit_color=Color.red,
    ):
        super().__init__()

        self.frame: Frame = frame
        self.matrixQueue: Queue[Signal] = matrixQueue
        self.show_time_event: Event = show_time_event
        self.display_duration: int = display_duration
        self.hour_first_digit_pos: tuple[int, int] = hour_first_digit_pos
        self.hour_second_digit_pos: tuple[int, int] = hour_second_digit_pos
        self.minute_first_digit_pos: tuple[int, int] = minute_first_digit_pos
        self.minute_second_digit_pos: tuple[int, int] = minute_second_digit_pos
        self.hour_first_digit_color: Color = hour_first_digit_color
        self.hour_second_digit_color: Color = hour_second_digit_color
        self.minute_first_digit_color: Color = minute_first_digit_color
        self.minute_second_digit_color: Color = minute_second_digit_color

        self.__turn_off_time = None
        self.__imageLoader: ImageLoader = ImageLoader()
        self.__imageLoader.load("python_ledbox/images/numerals/")
        EventManager.addListener(self.show_time_event, self.signalQueue)

    def _mainloop(self) -> None:

        signal: Signal = None
        cur_minute: int = None

        while True:

            now: datetime = datetime.now()

            if self.__turn_off_time != None:
                if now > self.__turn_off_time:
                    self.matrixQueue.put(Signal(MatrixEvent.CLEAR))
                    self.__turn_off_time = None
                elif now.minute != cur_minute:
                    cur_minute = now.minute
                    self.update_time_on_frame(now)
                    self.matrixQueue.put(Signal(MatrixEvent.CLEAR))
                    self.matrixQueue.put(
                        Signal(MatrixEvent.UPDATE, self.frame.getMap())
                    )

            try:
                signal = self.signalQueue.get(block=True, timeout=0.017)
                # signal = self.signalQueue.get(block=False)
            except QueueEmptyException:
                continue

            match signal:
                case Signal(AppEvent.KILL):
                    break
                case _ if not self.isActive():
                    continue
                case Signal(self.show_time_event):
                    cur_minute = now.minute
                    self.update_time_on_frame(now)
                    self.__turn_off_time = now + timedelta(
                        seconds=self.display_duration
                    )
                    self.matrixQueue.put(
                        Signal(MatrixEvent.UPDATE, self.frame.getMap())
                    )
                case other:
                    logging.error(f"{other} is not a supported message.")

    def update_time_on_frame(self, cur_time: datetime):
        hour_first_digit: Image = self.__imageLoader.get(str(cur_time.hour // 10))
        hour_second_digit: Image = self.__imageLoader.get(str(cur_time.hour % 10))
        minute_first_digit: Image = self.__imageLoader.get(str(cur_time.minute // 10))
        minute_second_digit: Image = self.__imageLoader.get(str(cur_time.minute % 10))

        hour_first_digit.applyToFrame(
            self.frame,
            self.hour_first_digit_pos[0],
            self.hour_first_digit_pos[1],
            {0: self.hour_first_digit_color},
        )

        hour_second_digit.applyToFrame(
            self.frame,
            self.hour_second_digit_pos[0],
            self.hour_second_digit_pos[1],
            {0: self.hour_second_digit_color},
        )

        minute_first_digit.applyToFrame(
            self.frame,
            self.minute_first_digit_pos[0],
            self.minute_first_digit_pos[1],
            {0: self.minute_first_digit_color},
        )

        minute_second_digit.applyToFrame(
            self.frame,
            self.minute_second_digit_pos[0],
            self.minute_second_digit_pos[1],
            {0: self.minute_second_digit_color},
        )
