from abc import ABC, abstractmethod
from python_ledbox.events import Signal, AppEvent
from queue import Queue
from threading import Thread


class App(ABC):
    def __init__(self):
        self._isActive = False
        self._isInitialised = False
        self.signalQueue: Queue[Signal] = Queue()
        self.__mainloopThread: Thread = Thread(target=self.__mainloop, daemon=True)

    @abstractmethod
    def __mainloop(self) -> None:
        """Method for running the main app logic. Runs in a different thread and should react to signals from signalQueue. Access to other objects should be controlled through locks."""

    def start(self) -> None:
        """Start app, extra initialization step may be necessary. Subclasses should call super().start() before implementing their own start method"""

        self._isActive = True
        self._isInitialised = True
        self.signalQueue.put(Signal(AppEvent.START))
        self.__mainloopThread.start()

    def stop(self) -> None:
        """Stop app, may not kill all processes if kill() method is implemented. Subclasses should call super().stop() before implementing their own stop method."""

        self._isActive = False
        self.signalQueue.put(Signal(AppEvent.STOP))

    # def resume(self) -> None:
    #     """Resume app, should be implemented to start app if it has already been initialiazed. Calls start() by default, should set self.isActive to True if start() is not called."""

    #     if not self.__isInitialised:
    #         raise Exception(
    #             "Cannot resume app, it has not yet been initialzed, call start() instead."
    #         )
    #     self.start()

    def kill(self) -> None:
        """Kill app, stopping all processes (should set self.__isInitialised and self.isActive to False ). The mainloopthread should exit and be called again through start."""

        self._isInitialised = False
        self._isActive = False
        self.signalQueue.put(Signal(AppEvent.KILL))

    def isActive(self) -> bool:
        """Returns wether app is active or not."""

        return self._isActive

    def isInitialised(self) -> bool:
        """Returns wether app has been initialized or not."""

        return self._isInitialised
