from enum import Enum
from typing import Callable, Dict, Set, Any
import logging

logging.basicConfig(
    format="%(levelname)s %(asctime)s     %(message)s",
    filename="/home/pi/Documents/python_ledbox/fancontrol.log",
    level=logging.DEBUG,
    datefmt="%m/%d/%Y %I:%M:%S %p",
)


class Event(Enum):
    MOUSE_CLICK_RIGHT = 1
    MOUSE_CLICK_LEFT = 2


class EventManager:
    subscribers: Dict[Event, Set[Callable]] = {event: set() for event in Event}

    def addListener(event: Event, callback: Callable[[], Any]) -> None:
        EventManager.subscribers[event].add(callback)

    def removeListener(event: Event, callback: Callable) -> bool:
        EventManager.subscribers[event].discard(callback)

    def dispatch(event: Event):
        logging.debug(f"fired {event} event")
        for callback in EventManager.subscribers[event]:
            callback()
