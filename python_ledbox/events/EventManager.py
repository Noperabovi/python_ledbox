from queue import Queue
from collections import defaultdict
from typing import Set, DefaultDict, Optional, Any
import logging

from .Events import Event, Signal

logging.basicConfig(
    format="%(levelname)s %(asctime)s     %(message)s",
    filename="eventlog.log",
    level=logging.DEBUG,
    datefmt="%m/%d/%Y %I:%M:%S %p",
)


subscribers: DefaultDict[Event, Set[Queue[Signal]]] = defaultdict(lambda: set())


def addListener(event: Event, queue: Queue[Signal]) -> None:
    subscribers[event].add(queue)


def removeListener(event: Event, queue: Queue[Signal]) -> bool:
    subscribers[event].discard(queue)


def dispatch(event: Event, message: Optional[Any] = None):
    logging.debug(f"fired {event} event")
    for queue in subscribers[event]:
        queue.put(Signal(event, message))
