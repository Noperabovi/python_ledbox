import unittest
from unittest.mock import Mock, MagicMock
from typing import Any, DefaultDict, Set, Callable
from queue import Queue
from collections import defaultdict

from python_ledbox.events import Event, Signal, MouseEvent as ME, EventManager


class TestEvents(unittest.TestCase):
    def setUp(self):
        """Create Mock objects for function calls."""
        self.queue1 = Mock()
        self.queue2 = Mock()

    def tearDown(self) -> None:
        EventManager.subscribers: DefaultDict[Event, Set[Callable]] = defaultdict(
            lambda: set()
        )

    def test_addListener(self):
        """Test that adding a listener adds queue to set of listeners."""

        EventManager.addListener(ME.MOUSE_CLICK_LEFT, self.queue1)
        EventManager.addListener(ME.MOUSE_CLICK_LEFT, self.queue2)

        self.assertIn(self.queue1, EventManager.subscribers[ME.MOUSE_CLICK_LEFT])
        self.assertIn(self.queue2, EventManager.subscribers[ME.MOUSE_CLICK_LEFT])
        self.assertEqual(0, len(EventManager.subscribers[ME.MOUSE_CLICK_RIGHT]))

    def test_removeListener(self):
        """Test that removing a listener removes queue from set of listeners."""

        EventManager.addListener(ME.MOUSE_CLICK_LEFT, self.queue1)
        EventManager.addListener(ME.MOUSE_CLICK_LEFT, self.queue2)

        EventManager.removeListener(ME.MOUSE_CLICK_LEFT, self.queue1)

        self.assertNotIn(self.queue1, EventManager.subscribers[ME.MOUSE_CLICK_LEFT])
        self.assertEqual(1, len(EventManager.subscribers[ME.MOUSE_CLICK_LEFT]))

    def test_dispatch_called(self):
        """Test that all listening queues are updated once when an envent is fired."""

        EventManager.addListener(ME.MOUSE_CLICK_LEFT, self.queue1)
        EventManager.addListener(ME.MOUSE_CLICK_RIGHT, self.queue2)

        EventManager.dispatch(ME.MOUSE_CLICK_LEFT)
        self.assertEqual(1, self.queue1.put.call_count)
        self.assertEqual(0, self.queue2.put.call_count)

        EventManager.dispatch(ME.MOUSE_CLICK_RIGHT)

        self.assertEqual(1, self.queue1.put.call_count)
        self.assertEqual(1, self.queue2.put.call_count)

    def test_dispatch_called_with_arguments(self):
        """Test that all listening queues are updated once when an envent is fired."""

        def getCallArg():
            return self.queue1.put.call_args.args[0]

        EventManager.addListener(ME.MOUSE_CLICK_LEFT, self.queue1)

        EventManager.dispatch(ME.MOUSE_CLICK_LEFT)
        event = getCallArg().event
        message = getCallArg().message
        self.assertIsInstance(getCallArg(), Signal)
        self.assertEqual(event, ME.MOUSE_CLICK_LEFT)
        self.assertEqual(message, None)

        EventManager.dispatch(ME.MOUSE_CLICK_LEFT, "MOIN")
        event = getCallArg().event
        message = getCallArg().message
        self.assertIsInstance(getCallArg(), Signal)
        self.assertEqual(event, ME.MOUSE_CLICK_LEFT)
        self.assertEqual(message, "MOIN")
