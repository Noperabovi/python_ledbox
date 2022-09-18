import queue
from typing import Set, Any, Optional, DefaultDict
from enum import Enum

# from queue import Queue
# from collections import defaultdict
import logging
from dataclasses import dataclass

# from python_ledbox.events.MouseEvents import MouseEvent

# TODO this might be interesting for defining message types for each event later
# https://stackoverflow.com/questions/12680080/python-enums-with-attributes


logging.basicConfig(
    format="%(levelname)s %(asctime)s     %(message)s",
    filename="eventlog.log",
    level=logging.DEBUG,
    datefmt="%m/%d/%Y %I:%M:%S %p",
)


class Event(Enum):
    pass


class AppEvent(Event):
    START = 1
    STOP = 2
    KILL = 3


@dataclass
class Signal:
    event: Event
    message: Optional[Any] = None


# class EventManager:
# subscribers: DefaultDict[Event, Set[Queue[Signal]]] = defaultdict(lambda: set())

# def addListener(event: Event, queue: Queue[Signal]) -> None:
#     subscribers[event].add(queue)

# def removeListener(event: Event, queue: Queue[Signal]) -> bool:
#     subscribers[event].discard(queue)

# def dispatch(event: Event, message: Optional[Any] = None):
#     logging.debug(f"fired {event} event")
#     for queue in subscribers[event]:
#         queue.put(Signal(event, message))
