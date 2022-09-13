from abc import ABC, abstractmethod
from typing import Final, Dict
from python_ledbox.Frames import Frame, FrameStack
from python_ledbox.events import Event


class MatrixEvent(Event):
    UPDATE = 1
    REPAINT = 2


class Matrix(ABC):
    def __init__(self, rows: int, cols: int):
        self.ROWS: Final[int] = rows
        self.COLS: Final[int] = cols

    @abstractmethod
    def applyChanges(self, changes: Dict[int, int]) -> None:
        """Apply given changes to the matrix."""

    @abstractmethod
    def applyMap(self, map: Dict[int, int]) -> None:
        """Apply entire frame-map to the matrix."""

    @abstractmethod
    def clear(self) -> None:
        """Clear entire matrix (turn off pixels)."""

    def createFrame(self) -> Frame:
        """Create Frame with same dimensions of matrix."""
        return Frame(self.ROWS, self.COLS)

    def createFrameStack(self) -> FrameStack:
        """Create FrameStack with same dimensions of matrix."""
        return FrameStack(self.ROWS, self.COLS)
