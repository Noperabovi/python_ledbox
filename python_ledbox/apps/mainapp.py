from tracemalloc import start
from python_ledbox.App import App
from python_ledbox.Frames import FrameComponent
from python_ledbox.Matrix import Matrix, MatrixEvent
from python_ledbox.events import Signal, AppEvent, Event
from python_ledbox.App import App

import logging

from queue import Queue, Empty as QueueEmptyException
from typing import Dict, List, Optional


class MainApp(App):
    def __init__(
        self,
        matrix: Matrix,
        signalQueue: Queue[Signal],
        apps: List[App],
        prev_app_event: Optional[Event] = None,
        next_app_event: Optional[Event] = None,
    ):
        super().__init__()
        if prev_app_event != None and prev_app_event == next_app_event:
            raise ValueError(
                "Events for switching to next/prev app cannot be the same."
            )

        if len(apps) == 0:
            raise ValueError(
                "Cannot initialize without at least one app being passed into apps argument."
            )

        self.signalQueue = signalQueue
        self.prev_app_event: Optional[Event] = prev_app_event
        self.next_app_event: Optional[Event] = next_app_event
        self.__matrix: Matrix = matrix
        self.__appList: List[App] = apps
        self.__currentIndex: int = 0

    def next_app(self) -> None:
        self.__appList[self.__currentIndex].stop()
        self.__currentIndex = (self.__currentIndex + 1) % len(self.__appList)
        self.__appList[self.__currentIndex].start()

    def prev_app(self) -> None:
        self.__appList[self.__currentIndex].stop()
        self.__currentIndex = (self.__currentIndex - 1) % len(self.__appList)
        self.__appList[self.__currentIndex].start()

    def start(self) -> None:
        super().start()
        self.__appList[self.__currentIndex].start()

    def stop(self) -> None:
        super().stop()
        self.__appList[self.__currentIndex].stop()

    def kill(self) -> None:
        super().kill()
        for app in self.__appList:
            app.kill()

    def _mainloop(self) -> None:

        signal: Signal = None

        while True:
            try:
                signal = self.signalQueue.get(block=True, timeout=0.017)
                # signal = self.signalQueue.get(block=False)
            except QueueEmptyException:
                continue

            match signal:
                case Signal(AppEvent.KILL):
                    break
                case Signal() if not self.isActive():
                    continue
                case Signal(MatrixEvent.UPDATE, x) if isinstance(x, dict):
                    self.__matrix.applyChanges(x)
                case Signal(MatrixEvent.REPAINT, x) if isinstance(x, dict):
                    self.__matrix.applyMap(x)
                case Signal(self.next_app_event, _):
                    self.next_app()
                case Signal(self.prev_app_event, _):
                    self.prev_app()
                case other:
                    logging.error(f"{other} is not a supported message.")
