import unittest
from unittest.mock import patch, call

from sty import bg, rs

from python_ledbox.Frames import Frame
from python_ledbox.TerminalMatrix import TerminalMatrix
from python_ledbox import Color


def get_frame():

    frame = Frame(2, 2)

    frame[0, 0] = Color.from_rgb(255, 255, 255)
    frame[0, 1] = Color.from_rgb(255, 0, 0)
    frame[1, 0] = Color.from_rgb(0, 255, 0)
    frame[1, 1] = Color.from_rgb(0, 0, 255)

    return frame


def get_renderedMatrix():

    matrix = TerminalMatrix(2, 2)
    map = get_frame().getMap()

    matrix.applyMap(map)

    return matrix


class TestTerminalMatrix(unittest.TestCase):
    @patch("builtins.print")
    def test_apply_map(self, mock_print):
        # def test_apply_map(self):
        """Test that the applyMap() method displays frame in terminal."""

        matrix = TerminalMatrix(2, 2)
        frame = get_frame()

        # expected print calls
        calls = [None] * 7

        calls[0] = call("\n\n")
        calls[1] = call("\033[F" * (matrix.ROWS + 1))
        calls[2] = call(bg(255, 255, 255) + "  " + rs.bg + bg(255, 0, 0) + "  " + rs.bg)
        calls[3] = call(bg(0, 255, 0) + "  " + rs.bg + bg(0, 0, 255) + "  " + rs.bg)
        calls[4] = calls[1]
        calls[5] = call(bg(255, 0, 255) + "  " + rs.bg + bg(255, 0, 0) + "  " + rs.bg)
        calls[6] = call("  " + bg(0, 0, 255) + "  " + rs.bg)

        # apply original map
        matrix.applyMap(frame.getMap())

        # change frame, test overwrite
        frame[0, 0] = Color.from_rgb(255, 0, 255)
        frame[1, 0] = None

        matrix.applyMap(frame.getMap())

        # 7 lines should be written
        self.assertEqual(len(mock_print.call_args_list), 7)

        for index, value in enumerate(mock_print.call_args_list):
            self.assertEqual(value, calls[index])

    @patch("builtins.print")
    def test_apply_changes(self, mock_print):
        """Test that the applyChanges() method displays frame in terminal."""

        matrix = get_renderedMatrix()
        frame = get_frame()

        frame[0, 0] = Color.from_rgb(255, 0, 255)
        frame[1, 0] = None

        # get changes from frame
        matrix.applyChanges(frame.getChanges())

        # expected output
        calls = [None] * 3
        calls[0] = call("\033[F" * (matrix.ROWS + 1))
        calls[1] = call(bg(255, 0, 255) + "  " + rs.bg + bg(255, 0, 0) + "  " + rs.bg)
        calls[2] = call("  " + bg(0, 0, 255) + "  " + rs.bg)

        call_args = mock_print.call_args_list

        # 7 lines should be written (3 from rendered map)
        self.assertEqual(len(call_args), 7)

        for i in range(4, 7):
            self.assertEqual(call_args[i], calls[i - 4])
