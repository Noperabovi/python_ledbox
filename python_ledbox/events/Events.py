import queue
from typing import Callable, Dict, Set, Any, Optional, DefaultDict
from enum import Enum
from queue import Queue
from collections import defaultdict
from abc import ABC

import logging

# from python_ledbox.events.MouseEvents import MouseEvent

# TODO this might be interesting for defining message types for each event later
# https://stackoverflow.com/questions/12680080/python-enums-with-attributes


logging.basicConfig(
    format="%(levelname)s %(asctime)s     %(message)s",
    filename="/home/pi/Documents/python_ledbox/eventlog.log",
    level=logging.DEBUG,
    datefmt="%m/%d/%Y %I:%M:%S %p",
)


class Event(Enum):
    pass


class AppEvent(Event):
    START = 1
    STOP = 2
    KILL = 3


class Signal:
    def __init__(self, event: Event, message: Optional[Any] = None):
        self.event: Event = event
        self.message: Any = message


class EventManager:
    subscribers: DefaultDict[Event, Set[Queue[Signal]]] = defaultdict(lambda: set())

    def addListener(event: Event, queue: Queue[Signal]) -> None:
        EventManager.subscribers[event].add(queue)

    def removeListener(event: Event, queue: Queue[Signal]) -> bool:
        EventManager.subscribers[event].discard(queue)

    def dispatch(event: Event, message: Optional[Any] = None):
        logging.debug(f"fired {event} event")
        for queue in EventManager.subscribers[event]:
            queue.put(Signal(event, message))


if __name__ == "__main__":
    myQueue = Queue()
    EventManager.addListener(AppEvent.START, myQueue)
    EventManager.addListener(AppEvent.KILL, myQueue)
    EventManager.dispatch(AppEvent.START)
    EventManager.dispatch(AppEvent.START, "start2")
    EventManager.dispatch(AppEvent.START, {"hour": 8, "minute": 30, "active": True})
    EventManager.dispatch(AppEvent.KILL, 2234)

    while not myQueue.empty():
        signal: Signal = myQueue.get()
        print(f"Event: {signal.event} Message: {signal.message}")
