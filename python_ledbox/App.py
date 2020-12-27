from abc import ABC
from python_ledbox.Matrix import Matrix


class App(ABC):
    def __init__(self, matrix: Matrix):
        self.__isActive = False
        self.__isInitialised = False
        self.matrix = matrix

    def start(self) -> None:
        """Start app, may be used to start app for first time if resume() is implemented. Subclasses should call super().start() before implementing their own start method"""

        self.__isActive = True
        self.__isInitialised = True

    def stop(self) -> None:
        """Stop app, may not kill all processes if kill() method is implemented. Subclasses should call super().stop() before implementing their own stop method."""

        self.__isActive = False

    def resume(self) -> None:
        """Resume app, should be implemented to start app if it has already been initialiazed. Calls start() by default, should set self.isActive to True if start() is not called."""

        if not self.__isInitialised:
            raise Exception(
                "Cannot resume app, it has not yet been initialzed, call start() instead."
            )
        self.start()

    def kill(self) -> None:
        """Kill app, stopping all processes. Initialisation by calling start() may be necessary (should set self.__isInitialised and self.isActive to False ). Calls stop() by default."""

        self.__isInitialised = False
        self.stop()

    def isActive(self) -> bool:
        """Returns wether app is active or not."""

        return self.__isActive

    def isInitialised(self) -> bool:
        """Returns wether app has been initialized or not."""

        return self.__isInitialised
