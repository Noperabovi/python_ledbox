from enum import Enum
from typing import Any, Optional

# from abc import ABC

# TODO this might be interesting for defining message types for each event later
# https://stackoverflow.com/questions/12680080/python-enums-with-attributes


class Event(Enum):
    pass


class AppEvent(Event):
    START = 1
    STOP = 2
    KILL = 3


class AlarmClockEvent(Event):
    UPDATE_TIME = 1


class Signal:
    def __init__(self, event: Event, message: Optional[Any] = None):
        self.event: Event = event
        self.message: Any = message


def receiveSignal(signal: Signal):
    if signal.event == AppEvent.START:
        print("startapp")
        print(f"Message: {signal.message}")


if __name__ == "__main__":

    receiveSignal(Signal(AppEvent.START))
