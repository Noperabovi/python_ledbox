import python_ledbox
import unittest
from unittest.mock import patch
from python_ledbox.Matrix import Matrix
from python_ledbox import Frames


class TestMatrix(unittest.TestCase):

    # patch abstract methods to prevent errors
    @patch.multiple(Matrix, __abstractmethods__=set())
    def test_constructor_sets_variables(self):
        """Test that the constructor sets the cols and rows variables."""

        aMatrix = Matrix(10, 7)

        self.assertEqual(aMatrix.ROWS, 10)
        self.assertEqual(aMatrix.COLS, 7)

    # patch abstract methods to prevent errors
    @patch.multiple(Matrix, __abstractmethods__=set())
    def testCreateFrame(self):
        """Test that the createFrame method returns FrameStack of correct dimensions."""
        aMatrix = Matrix(10, 7)
        frame = aMatrix.createFrame()

        self.assertIsInstance(frame, Frames.Frame)

        self.assertTrue(frame.ROWS, 10)
        self.assertTrue(frame.COLS, 7)

    # patch abstract methods to prevent errors
    @patch.multiple(Matrix, __abstractmethods__=set())
    def testCreateFrameStack(self):
        """Test that the createFrameStack method returns FrameStack of correct dimensions."""
        aMatrix = Matrix(10, 7)

        frameStack = aMatrix.createFrameStack()
        self.assertIsInstance(frameStack, Frames.FrameStack)

        self.assertTrue(frameStack.ROWS, 10)
        self.assertTrue(frameStack.COLS, 7)
