import unittest
from unittest.mock import patch, call, Mock
from datetime import datetime
import time

from python_ledbox.Frames import Frame
from python_ledbox.apps.ClockApp import ClockApp


class TestClockApp(unittest.TestCase):
    @patch("python_ledbox.apps.ClockApp.time")
    @patch("python_ledbox.apps.ClockApp.datetime")
    @patch("python_ledbox.apps.ClockApp.Matrix")
    @patch("python_ledbox.apps.ClockApp.ImageLoader")
    @patch("python_ledbox.apps.ClockApp.Image")
    def test_displays_correct_time(
        self, Mock_Image, Mock_ImageLoader, mock_matrix, mock_dt, mock_time
    ):
        """Test that app displays the current time."""

        mock_dt.now = Mock(return_value=datetime(2000, 1, 1, 13, 54))
        mock_dt.hour = Mock(return_value=13)
        mock_dt.minute = Mock(return_value=54)

        # forces thread to be switched
        mock_time.sleep = Mock(side_effect=lambda x: time.sleep(0.01))

        mock_ImageLoader = Mock_ImageLoader()
        mock_Image = Mock_Image()
        mock_ImageLoader.get = Mock(return_value=mock_Image)
        mock_Image.applyToFrame = Mock(return_value="Image")

        # create app and start
        frame = Frame(10, 10)
        matrix = mock_matrix()
        app = ClockApp(matrix, frame)
        app.start()

        # get digits from ImageLoader
        digits = ["1", "3", "5", "4"]

        for digit in digits:
            c = call(digit)
            self.assertIn(c, mock_ImageLoader.get.call_args_list)

        # printed images
        calls = [None] * 4
        recolor = {0: 16711680}
        calls[0] = call(frame, 0, 0, recolor)
        calls[1] = call(frame, 0, 7, recolor)
        calls[2] = call(frame, 5, 0, recolor)
        calls[3] = call(frame, 5, 7, recolor)

        for c in calls:
            self.assertIn(c, mock_Image.applyToFrame.call_args_list)

        matrix.applyChanges.assert_called_once_with(frame.getChanges())

        app.stop()

    @patch("python_ledbox.apps.ClockApp.time")
    @patch("python_ledbox.apps.ClockApp.datetime")
    @patch("python_ledbox.apps.ClockApp.Matrix")
    @patch("python_ledbox.apps.ClockApp.ImageLoader")
    @patch("python_ledbox.apps.ClockApp.Image")
    def test_clock_applies_whole_map(
        self, Mock_Image, Mock_ImageLoader, mock_matrix, mock_dt, mock_time
    ):
        """Test that app displays the current time."""

        mock_dt.now = Mock(return_value=datetime(2000, 1, 1, 13, 54))
        mock_dt.hour = Mock(return_value=13)
        mock_dt.minute = Mock(return_value=54)

        # forces thread to be switched
        mock_time.sleep = Mock(side_effect=lambda x: time.sleep(0.01))

        mock_ImageLoader = Mock_ImageLoader()
        mock_Image = Mock_Image()
        mock_ImageLoader.get = Mock(return_value=mock_Image)
        mock_Image.applyToFrame = Mock(return_value="Image")

        # create app and start
        frame = Frame(10, 10)
        matrix = mock_matrix()
        app = ClockApp(matrix, frame)
        app.start()

        # get digits from ImageLoader
        digits = ["1", "3", "5", "4"]

        for digit in digits:
            c = call(digit)
            self.assertIn(c, mock_ImageLoader.get.call_args_list)

        # printed images
        calls = [None] * 4
        recolor = {0: 16711680}
        calls[0] = call(frame, 0, 0, recolor)
        calls[1] = call(frame, 0, 7, recolor)
        calls[2] = call(frame, 5, 0, recolor)
        calls[3] = call(frame, 5, 7, recolor)

        for c in calls:
            self.assertIn(c, mock_Image.applyToFrame.call_args_list)

        matrix.applyChanges.assert_called_once_with(frame.getChanges())

        app.stop()

    @patch("python_ledbox.apps.ClockApp.time")
    @patch("python_ledbox.apps.ClockApp.datetime")
    @patch("python_ledbox.apps.ClockApp.Matrix")
    @patch("python_ledbox.apps.ClockApp.ImageLoader")
    @patch("python_ledbox.apps.ClockApp.Image")
    def test_stop_stops_updating_time(
        self, Mock_Image, Mock_ImageLoader, mock_matrix, mock_dt, mock_time
    ):
        """Test that displayed time is not updated when calling stop/kill."""

        mock_dt.now = Mock(return_value=datetime(2000, 1, 1, 13, 54))

        # forces thread to be switched
        mock_time.sleep = Mock(side_effect=lambda x: time.sleep(0.01))

        mock_ImageLoader = Mock_ImageLoader()
        mock_Image = Mock_Image()
        mock_ImageLoader.get = Mock(return_value=mock_Image)
        mock_Image.applyToFrame = Mock(return_value="Image")

        # create app and start
        frame = Frame(10, 10)
        matrix = mock_matrix()
        app = ClockApp(matrix, frame)
        app.applyMapOnChange = True
        app.start()

        app.stop()

        time.sleep(0.05)  # force other thread to continue running (not updating time)

        mock_dt.now = Mock(return_value=datetime(2000, 1, 1, 14, 00))

        # no further calls should be made
        self.assertNotIn(call("0"), mock_ImageLoader.get.call_args_list)
        self.assertEqual(4, len(mock_Image.applyToFrame.call_args_list))

        matrix.applyMap.assert_called_once_with(frame.getMap())

        app.stop()

    @patch("python_ledbox.apps.ClockApp.time")
    @patch("python_ledbox.apps.ClockApp.datetime")
    @patch("python_ledbox.apps.ClockApp.Matrix")
    @patch("python_ledbox.apps.ClockApp.ImageLoader")
    @patch("python_ledbox.apps.ClockApp.Image")
    def test_change_default_colors(
        self, Mock_Image, Mock_ImageLoader, mock_matrix, mock_dt, mock_time
    ):
        """Tets that time is displayed with changed colors."""

        mock_dt.now = Mock(return_value=datetime(2000, 1, 1, 13, 54))

        # forces thread to be switched
        mock_time.sleep = Mock(side_effect=lambda x: time.sleep(0.01))

        mock_ImageLoader = Mock_ImageLoader()
        mock_Image = Mock_Image()
        mock_ImageLoader.get = Mock(return_value=mock_Image)
        mock_Image.applyToFrame = Mock(return_value="Image")

        # create app and start
        frame = Frame(10, 10)
        matrix = mock_matrix()
        app = ClockApp(matrix, frame)

        app.hour_first_digit_color = 1
        app.hour_second_digit_color = 2
        app.minute_first_digit_color = 3
        app.minute_second_digit_color = 4

        app.start()

        # printed images with changed colors
        calls = [None] * 4
        calls[0] = call(frame, 0, 0, {0: 1})
        calls[1] = call(frame, 0, 7, {0: 2})
        calls[2] = call(frame, 5, 0, {0: 3})
        calls[3] = call(frame, 5, 7, {0: 4})

        for c in calls:
            self.assertIn(c, mock_Image.applyToFrame.call_args_list)

        matrix.applyChanges.assert_called_once_with(frame.getChanges())

        app.stop()

    @patch("python_ledbox.apps.ClockApp.time")
    @patch("python_ledbox.apps.ClockApp.datetime")
    @patch("python_ledbox.apps.ClockApp.Matrix")
    @patch("python_ledbox.apps.ClockApp.ImageLoader")
    @patch("python_ledbox.apps.ClockApp.Image")
    def test_change_default_positions(
        self, Mock_Image, Mock_ImageLoader, mock_matrix, mock_dt, mock_time
    ):
        """Test that digits are displayed at changed positions."""

        mock_dt.now = Mock(return_value=datetime(2000, 1, 1, 13, 54))

        # forces thread to be switched
        mock_time.sleep = Mock(side_effect=lambda x: time.sleep(0.01))

        mock_ImageLoader = Mock_ImageLoader()
        mock_Image = Mock_Image()
        mock_ImageLoader.get = Mock(return_value=mock_Image)
        mock_Image.applyToFrame = Mock(return_value="Image")

        # create app and start
        frame = Frame(10, 10)
        matrix = mock_matrix()
        app = ClockApp(matrix, frame)

        app.hour_first_digit_pos = (0, 0)
        app.hour_second_digit_pos = (5, 0)
        app.minute_first_digit_pos = (0, 4)
        app.minute_second_digit_pos = (5, 4)

        app.start()

        # printed images with changed colors
        calls = [None] * 4

        recolor = {0: 16711680}

        calls[0] = call(frame, 0, 0, recolor)
        calls[1] = call(frame, 5, 0, recolor)
        calls[2] = call(frame, 0, 4, recolor)
        calls[3] = call(frame, 5, 4, recolor)

        for c in calls:
            self.assertIn(c, mock_Image.applyToFrame.call_args_list)

        matrix.applyChanges.assert_called_once_with(frame.getChanges())

        app.stop()
