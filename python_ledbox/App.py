from abc import ABC
from python_ledbox.Matrix import Matrix


class App(ABC):
    def __init__(self):
        self._isActive = False
        self._isInitialised = False

    def start(self) -> None:
        """Start app, extra initialization step may be necessary. Subclasses should call super().start() before implementing their own start method"""

        self._isActive = True
        self._isInitialised = True

    def stop(self) -> None:
        """Stop app, may not kill all processes if kill() method is implemented. Subclasses should call super().stop() before implementing their own stop method."""

        self._isActive = False

    # def resume(self) -> None:
    #     """Resume app, should be implemented to start app if it has already been initialiazed. Calls start() by default, should set self.isActive to True if start() is not called."""

    #     if not self.__isInitialised:
    #         raise Exception(
    #             "Cannot resume app, it has not yet been initialzed, call start() instead."
    #         )
    #     self.start()

    def kill(self) -> None:
        """Kill app, stopping all processes (should set self.__isInitialised and self.isActive to False ). Calls stop() by default."""

        self._isInitialised = False
        self.stop()

    def isActive(self) -> bool:
        """Returns wether app is active or not."""

        return self._isActive

    def isInitialised(self) -> bool:
        """Returns wether app has been initialized or not."""

        return self._isInitialised
