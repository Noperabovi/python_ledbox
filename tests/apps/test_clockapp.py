import unittest
from unittest.mock import Mock, patch, call
from queue import Queue, Empty as QueueEmptyException
import time
from datetime import datetime
from python_ledbox.Images import ImageLoader

from python_ledbox.apps import ClockApp
from python_ledbox.events import MouseEvent, Signal
from python_ledbox.Matrix import MatrixEvent
from python_ledbox.Frames import Frame
from python_ledbox import Color
from python_ledbox.events import EventManager


class TestClockApp(unittest.TestCase):
    @patch.multiple(ClockApp, __abstractmethods__=set())
    def test_clock_minimal_configuration(self):
        """Test that clock can be initialized with minimal parameters passed."""

        try:
            ClockApp(Frame(10, 10), Queue(), MouseEvent.MOUSE_CLICK_LEFT)
        except Exception:
            self.fail("Initialization raised exception unexpectedly.")

    @patch.multiple(ClockApp, __abstractmethods__=set())
    def test_clock_maximal_configuration(self):
        """Test that clock can be initialized with all parameters passed."""

        clockapp = ClockApp(
            Frame(10, 10),
            Queue(),
            MouseEvent.MOUSE_CLICK_LEFT,
            display_duration=10,
            hour_first_digit_pos=(0, 0),
            hour_second_digit_pos=(0, 3),
            minute_first_digit_pos=(5, 0),
            minute_second_digit_pos=(5, 3),
            hour_first_digit_color=Color.red,
            hour_second_digit_color=Color.rebeccapurple,
            minute_first_digit_color=Color.paleturquoise,
            minute_second_digit_color=Color.blanchedalmond,
        )

        self.assertTrue(clockapp.show_time_event, MouseEvent.MOUSE_CLICK_LEFT)
        self.assertTrue(clockapp.display_duration, 10)
        self.assertTrue(clockapp.minute_second_digit_pos, (5, 3))
        self.assertTrue(clockapp.hour_second_digit_color, Color.rebeccapurple)

    @patch.object(ClockApp, "update_time_on_frame")
    @patch("python_ledbox.apps.clockapp.datetime")
    @patch("python_ledbox.apps.clockapp.EventManager", autospec=True)
    @patch.multiple(ClockApp, __abstractmethods__=set())
    def test_show_time_event_shows_time(
        self, event_manager, mock_datetime, mock_update_time_on_frame
    ):
        """Test that passing the right event will make the app send update to the matrixqueue."""

        matrixQueue: Queue[Signal] = Queue()
        clockapp: ClockApp = ClockApp(
            Frame(10, 10), matrixQueue, MouseEvent.MOUSE_CLICK_LEFT
        )
        clockapp.start()

        mock_datetime.now = Mock(return_value=datetime(2000, 1, 1, 13, 54, 15))

        event_manager.addListener.assert_called_with(
            MouseEvent.MOUSE_CLICK_LEFT, clockapp.signalQueue
        )
        clockapp.signalQueue.put(Signal(MouseEvent.MOUSE_CLICK_LEFT))
        result: Signal = matrixQueue.get()
        self.assertEqual(result.event, MatrixEvent.UPDATE)
        self.assertEqual(type(result.message), dict)

        mock_update_time_on_frame.assert_called_with(datetime(2000, 1, 1, 13, 54, 15))

    @patch("python_ledbox.apps.clockapp.ImageLoader")
    @patch("python_ledbox.apps.clockapp.Image")
    def test_update_time_on_frame_displays_correct_time(
        self, Mock_Image, Mock_ImageLoader
    ):
        """Test that the correct time is applied to the frame."""

        mock_ImageLoader = Mock_ImageLoader()
        mock_Image = Mock_Image()
        mock_ImageLoader.get = Mock(return_value=mock_Image)

        frame = Frame(10, 10)
        matrixQueue: Queue[Signal] = Queue()
        app = ClockApp(
            frame,
            matrixQueue,
            MouseEvent.MOUSE_CLICK_LEFT,
            minute_first_digit_color=Color.lightseagreen,
            hour_first_digit_pos=(0, 0),
            hour_second_digit_pos=(0, 7),
            minute_first_digit_pos=(5, 0),
            minute_second_digit_pos=(5, 7),
        )

        app.update_time_on_frame(datetime(1, 1, 1, hour=13, minute=54))

        # correct digits are loaded
        digits = ["1", "3", "5", "4"]

        for digit in digits:
            c = call(digit)
            self.assertIn(c, mock_ImageLoader.get.call_args_list)

        # printed images
        calls = [None] * 4
        recolor = {0: 16711680}
        calls[0] = call(frame, 0, 0, recolor)
        calls[1] = call(frame, 0, 7, recolor)
        calls[2] = call(frame, 5, 0, {0: Color.lightseagreen})
        calls[3] = call(frame, 5, 7, recolor)

        for c in calls:
            self.assertIn(c, mock_Image.applyToFrame.call_args_list)

    @patch("python_ledbox.apps.clockapp.datetime")
    def test_clear_after_display_duration(self, mock_datetime):
        """Test that matrix is turned off after specified time."""

        mock_datetime.now = Mock(return_value=datetime(2000, 1, 1, 13, 54, 0))

        matrixQueue: Queue[Signal] = Queue()
        clockapp: ClockApp = ClockApp(
            Frame(10, 10), matrixQueue, MouseEvent.MOUSE_CLICK_LEFT, display_duration=10
        )
        clockapp.start()
        clockapp.signalQueue.put(Signal(MouseEvent.MOUSE_CLICK_LEFT))
        matrixQueue.get()  # clear update

        mock_datetime.now = Mock(return_value=datetime(2000, 1, 1, 13, 54, 8))

        # no clear should be here (yet)
        with self.assertRaises(QueueEmptyException):
            matrixQueue.get_nowait()

        mock_datetime.now = Mock(return_value=datetime(2000, 1, 1, 13, 54, 11))
        time.sleep(0.1)

        item = matrixQueue.get_nowait()
        self.assertEqual(item.event, MatrixEvent.CLEAR)

    @patch("python_ledbox.apps.clockapp.datetime")
    def test_update_time_while_displaying(self, mock_datetime):
        """Test that while to clock is shown it is still being updated."""

        mock_datetime.now = Mock(return_value=datetime(2000, 1, 17, 0, 0, 55))

        matrixQueue: Queue[Signal] = Queue()
        clockapp: ClockApp = ClockApp(
            Frame(10, 10), matrixQueue, MouseEvent.MOUSE_CLICK_LEFT, display_duration=10
        )
        clockapp.start()
        clockapp.signalQueue.put(Signal(MouseEvent.MOUSE_CLICK_LEFT))
        matrixQueue.get()  # clear update

        mock_datetime.now = Mock(return_value=datetime(2000, 1, 17, 0, 1, 0))
        time.sleep(0.1)

        self.assertEqual(matrixQueue.get_nowait().event, MatrixEvent.CLEAR)
        self.assertEqual(matrixQueue.get_nowait().event, MatrixEvent.UPDATE)
