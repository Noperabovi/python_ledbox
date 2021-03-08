import unittest
from unittest.mock import patch, call

from rpi_ws281x.rpi_ws281x import PixelStrip

from python_ledbox.Frames import Frame
from python_ledbox.Matrix import Matrix
from python_ledbox import PiMatrix
from python_ledbox import Color

# TODO add PixelStrip mocks to prevent segmentation fault error


def get_frame():

    frame = Frame(2, 2)

    frame[0, 0] = Color.from_rgb(255, 255, 255)
    frame[0, 1] = Color.from_rgb(255, 0, 0)
    frame[1, 0] = Color.from_rgb(0, 255, 0)
    frame[1, 1] = Color.from_rgb(0, 0, 255)

    return frame


def get_renderedMatrix():

    matrix = PiMatrix.PiMatrix(2, 2, 18)
    map = get_frame().getMap()

    matrix.applyMap(map)

    return matrix


class TestPiMatrix(unittest.TestCase):
    @patch("python_ledbox.PiMatrix.PixelStrip")
    def test_constructor_creates_PixelStrip(self, mock_PixelStrip):

        matrix = PiMatrix.PiMatrix(2, 2, 18)

        self.assertEqual(matrix.COLS, 2)
        self.assertEqual(matrix.ROWS, 2)

        args, kwargs = mock_PixelStrip.call_args

        self.assertEqual(4, args[0])
        self.assertEqual(18, args[1])

    @patch("python_ledbox.PiMatrix.PixelStrip")
    def test_apply_map(
        self, mock_PixelStrip
    ):
        # def test_apply_map(self):
        """Test that the applyMap() method calls setPixelColor method for every pixel on frame."""

        matrix = PiMatrix.PiMatrix(2, 2, 18)
        frame = get_frame()

        pixelStrip = matrix._PiMatrix__pixelStrip

        # expected print calls
        calls = [None] * 8

        calls[0] = call(0, Color.from_rgb(255, 255, 255))
        calls[1] = call(1, Color.from_rgb(255, 0, 0))
        calls[2] = call(2, Color.from_rgb(0, 255, 0))
        calls[3] = call(3, Color.from_rgb(0, 0, 255))

        # calls after changes
        calls[4] = call(0, Color.from_rgb(255, 0, 255))
        calls[5] = call(1, Color.from_rgb(255, 0, 0))
        calls[6] = call(2, Color.from_rgb(0, 0, 0))
        calls[7] = call(3, Color.from_rgb(0, 0, 255))

        # apply original map
        matrix.applyMap(frame.getMap())

        # change frame, test overwrite
        frame[0, 0] = Color.from_rgb(255, 0, 255)
        frame[1, 0] = None

        matrix.applyMap(frame.getMap())

        # setPixelColor should be called 8 times (4 initial + 4 after changes)
        self.assertEqual(len(pixelStrip.setPixelColor.call_args_list), 8)

        for index, value in enumerate(pixelStrip.setPixelColor.call_args_list):
            self.assertEqual(value, calls[index])

        self.assertEqual(2, len(pixelStrip.show.call_args_list))

    @patch("python_ledbox.PiMatrix.PixelStrip")
    def test_apply_changes(self, mock_pixelStrip):
        """Test that the applyChanges() method calls setPixelColor method for every pixel on frame."""

        matrix = get_renderedMatrix()
        frame = get_frame()

        pixelStrip = matrix._PiMatrix__pixelStrip

        frame.clearChanges()
        frame[0, 0] = Color.from_rgb(255, 0, 255)
        frame[1, 0] = None

        # get changes from frame
        matrix.applyChanges(frame.getChanges())

        # expected output
        calls = [None] * 2
        calls[0] = call(0, Color.from_rgb(255, 0, 255))
        calls[1] = call(2, Color.from_rgb(0, 0, 0))

        call_args = pixelStrip.setPixelColor.call_args_list

        # 6 lines should be written (4 from rendered map)
        self.assertEqual(len(call_args), 6)

        for i in range(4, 6):
            self.assertEqual(call_args[i], calls[i - 4])

        self.assertEqual(2, len(pixelStrip.show.call_args_list))

    @patch("python_ledbox.PiMatrix.PixelStrip", autospec=True)
    def test_clear_matrix(self, mock_PixelStrip):
        """Test that all pixels are turned off when calling clear method."""

        matrix = get_renderedMatrix()
        matrix.clear()

        pixelStrip = matrix._PiMatrix__pixelStrip

        for i in range(4):
            self.assertEqual(pixelStrip.setPixelColor.call_args_list[i + 4], call(i, 0))

        self.assertEqual(2, len(pixelStrip.show.call_args_list))

    @patch("python_ledbox.PiMatrix.PixelStrip", autospec=True)
    def test_clear_matrix(self, mock_PixelStrip):
        """Test that all pixels are turned off when calling clear method."""

        matrix = get_renderedMatrix()
        matrix.clear()

        pixelStrip = matrix._PiMatrix__pixelStrip

        for i in range(4):
            self.assertEqual(
                pixelStrip.setPixelColor.call_args_list[i + 4],
                call(i, 0),
            )

        self.assertEqual(2, len(pixelStrip.show.call_args_list))
