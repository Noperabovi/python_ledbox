import unittest
from unittest.mock import Mock, MagicMock
from typing import Dict, Set, Callable

from python_ledbox.events import Event, EventManager


class TestEvents(unittest.TestCase):
    def setUp(self):
        """Create Mock object for function calls."""
        self.mock = MagicMock()

    def tearDown(self) -> None:
        EventManager.subscribers: Dict[Event, Set[Callable]] = {
            event: set() for event in Event
        }

    def test_addListener(self):
        """Test that adding a listener function adds function to list of listeners."""

        EventManager.addListener(Event.MOUSE_CLICK_LEFT, self.mock.func1)
        EventManager.addListener(Event.MOUSE_CLICK_LEFT, self.mock.func2)

        self.assertIn(self.mock.func1, EventManager.subscribers[Event.MOUSE_CLICK_LEFT])
        self.assertIn(self.mock.func2, EventManager.subscribers[Event.MOUSE_CLICK_LEFT])
        self.assertEqual(0, len(EventManager.subscribers[Event.MOUSE_CLICK_RIGHT]))

    def test_removeListener(self):
        """Test that removing a listener function removes function to list of listeners."""

        EventManager.addListener(Event.MOUSE_CLICK_LEFT, self.mock.func1)
        EventManager.addListener(Event.MOUSE_CLICK_LEFT, self.mock.func2)

        EventManager.removeListener(Event.MOUSE_CLICK_LEFT, self.mock.func1)

        self.assertNotIn(
            self.mock.func1, EventManager.subscribers[Event.MOUSE_CLICK_LEFT]
        )
        self.assertEqual(1, len(EventManager.subscribers[Event.MOUSE_CLICK_LEFT]))

    def test_dispatch(self):
        """Test that all functions that subscribed are called once when an envent is fired."""

        EventManager.addListener(Event.MOUSE_CLICK_LEFT, self.mock.func1)
        EventManager.addListener(Event.MOUSE_CLICK_LEFT, self.mock.func2)

        EventManager.dispatch(Event.MOUSE_CLICK_LEFT)
        self.assertEqual(1, self.mock.func1.call_count)
        self.assertEqual(1, self.mock.func2.call_count)

        EventManager.dispatch(Event.MOUSE_CLICK_LEFT)

        self.assertEqual(2, self.mock.func1.call_count)
        self.assertEqual(2, self.mock.func2.call_count)
