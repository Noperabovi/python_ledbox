from abc import ABC, abstractmethod
from typing import List, Tuple, Dict, Final


class FrameComponent(ABC):
    @abstractmethod
    def isStale(self) -> bool:
        """Returns wether the component has changed since last read access or not."""

    @abstractmethod
    def getMap(self) -> List[Tuple[int]]:
        """Returns entire map of color-values from the component."""

    @abstractmethod
    def getChanges(self, flush=True) -> List[Tuple[int]]:
        """Returns the changes made to the component since last read access."""


class Frame(FrameComponent):
    def __init__(self, rows: int, cols: int):
        self.ROWS: Final[int] = rows
        self.COLS: Final[int] = cols
        self.__map: Dict[int, int] = {}
        self.__changes: Dict[int, int] = {}

    def __getIndex(self, row: int, col: int) -> int:  # pragma: no cover
        """Returns map index of given cell."""

        return row * self.COLS + col

    def setColor(self, row: int, col: int, color: int) -> None:
        """Set color of given cell."""

        index = self.__getIndex(row, col)

        self.__map[index] = color
        self.__changes[index] = color

    def getColor(self, row: int, col: int) -> int:
        """Return color of given cell."""

        index = self.__getIndex(row, col)
        return self.__map.get(index)

    def getMap(self) -> Dict[int, int]:
        return self.__map

    def getChanges(self, flush=True) -> Dict[int, int]:
        changes = self.__changes

        if flush:
            self.__changes = {}

        return changes

    def isStale(self) -> bool:
        return len(self.__changes) != 0


class FrameStack(FrameComponent):
    def __init__(self, rows: int, cols: int):
        self.ROWS: Final[int] = rows
        self.COLS: Final[int] = cols
        self.__components: List[FrameComponent] = []

    def add(self, component: FrameComponent, index: int = None) -> None:
        """Add FrameComponent at given index, append to end if no index given."""
        if index is None:
            self.__components.append(component)
        else:
            self.__components.insert(index, component)

    def get(self, index: int) -> FrameComponent:
        """Returns FrameComponent from given index."""
        return self.__components[index]

    def remove(self, index: int) -> FrameComponent:
        """Returns and removes FrameComponent from given index."""
        return self.__components.pop(index)

    def getMap(self) -> Dict[int, int]:
        """Get map from the FrameStack, lower index is on top."""

        map = {}

        # go through each component
        for component in self.__components:
            # get changes of each component
            componentMap = component.getMap()
            # store changes if change for index does not already exist
            for index, color in componentMap.items():
                if index not in map and color != None:
                    map[index] = color

        return map

    def getChanges(self, flush=True) -> Dict[int, int]:
        """Get all changes from the FrameStack, lower index is on top."""

        changes = {}

        # go through each component
        for component in self.__components:
            # get changes of each component
            componentChanges = component.getChanges(flush)
            # store changes if change for index does not already exist
            for index, color in componentChanges.items():
                if index not in changes and color != None:
                    changes[index] = color

        return changes

    def isStale(self) -> bool:
        """Returns true if there are unflushed changes in any component."""

        for component in self.__components:
            if component.isStale():
                return True

        return False
