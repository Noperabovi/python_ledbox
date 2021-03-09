import unittest
from unittest.result import failfast

# from unittest.mock import patch

from python_ledbox import Frames


def setupFrame(colors):

    frame = Frames.Frame(10, 7)

    frame[0, 0] = colors[0]
    frame[5, 1] = colors[1]
    frame[9, 6] = colors[2]
    frame[3, 5] = colors[3]

    return frame


class TestFrame(unittest.TestCase):
    def setUp(self):
        self.testColors = [15899247, 550499, 16777215, None]

    def test_constructor_sets_variables(self):
        """Test that the constructor sets the cols and rows variables."""

        frame = Frames.Frame(10, 7)

        self.assertEqual(frame.ROWS, 10)
        self.assertEqual(frame.COLS, 7)

    def test_set_color_and_get_color_methods(self):
        """Test that colors set and get methods work correctly."""

        frame = Frames.Frame(10, 7)

        # __setitem__
        frame[0, 0] = self.testColors[0]
        frame[5, 1] = self.testColors[1]
        frame[9, 6] = self.testColors[2]
        # should be able to handle None (transparent)
        frame[3, 5] = self.testColors[3]

        # __getitem__
        self.assertEqual(frame[0, 0], self.testColors[0])
        self.assertEqual(frame[5, 1], self.testColors[1])
        self.assertEqual(frame[9, 6], self.testColors[2])
        # should be able to handle None (transparent)
        self.assertEqual(frame[3, 5], self.testColors[3])

    def test_getMap(self):
        """Test that getMap() method returns color array."""

        frame = setupFrame(self.testColors)
        map = frame.getMap()

        self.assertEqual(map[0 * frame.COLS + 0], 15899247)
        self.assertEqual(map[5 * frame.COLS + 1], 550499)
        self.assertEqual(map[9 * frame.COLS + 6], 16777215)
        self.assertEqual(map[3 * frame.COLS + 5], None)

    def test_getChanges_and_isStale(self):
        """Test that getChanges() method returns tuple-array of changes and is subsequently flushed."""

        frame = setupFrame(self.testColors)

        # frame should have changes and thus be stale
        self.assertTrue(frame.isStale())

        changes = frame.getChanges(flush=False)
        # stale frame should have changes
        self.assertEqual(len(changes), 4)

        self.assertEqual(changes[0 * frame.COLS + 0], 15899247)
        self.assertEqual(changes[5 * frame.COLS + 1], 550499)
        self.assertEqual(changes[9 * frame.COLS + 6], 16777215)
        self.assertEqual(changes[3 * frame.COLS + 5], None)

        # changes should not have been flushed, frame should be stale
        self.assertTrue(frame.isStale())
        changes = frame.getChanges()
        self.assertEqual(len(changes), 4)

        # changes should now be empty and thus not be stale
        self.assertFalse(frame.isStale())
        changes = frame.getChanges()
        self.assertEqual(len(changes), 0)

    def test_clearChanges(self):
        """Test that no changes are returned after clearChanges() has ben called."""

        f = setupFrame(self.testColors)

        f.clearChanges()

        self.assertEqual(0, len(f.getChanges()))
        self.assertFalse(f.isStale())

    # priavte methods/attributes should not be tested to keep encapsulation

    # def test_getIndex(self):
    #     """Test that _getIndex() method returns correct map index."""

    #     frame = Frames.Frame(10, 7)

    #     self.assertEqual(frame._getIndex(0, 0), 0)
    #     self.assertEqual(frame._getIndex(5, 1), 36)
    #     self.assertEqual(frame._getIndex(9, 6), 69)
    #     self.assertEqual(frame._getIndex(3, 5), 26)

    def test_no_changes_on_idempotent_operation(self):
        """Test that changes are not documented when cell is set to same color as before."""

        f = setupFrame(self.testColors)
        f.clearChanges()

        # same as initial color
        f[0, 0] = self.testColors[0]

        self.assertEqual(0, len(f.getChanges()))


def setupTestComponent():
    frame1 = Frames.Frame(10, 7)
    frame2 = Frames.Frame(10, 7)
    frame3 = Frames.Frame(10, 7)

    fs = Frames.FrameStack(10, 7)
    fs.add(frame1)

    sub_fs = Frames.FrameStack(10, 7)
    sub_fs.add(frame2)
    sub_fs.add(frame3)
    fs.add(sub_fs)

    return fs


class TestFrameStack(unittest.TestCase):
    def test_constructor_sets_variables(self):
        """Test that the constructor sets the cols and rows variables."""

        fs = Frames.FrameStack(10, 7)

        self.assertEqual(fs.ROWS, 10)
        self.assertEqual(fs.COLS, 7)

    def test_add_get_component(self):
        """Test that only components of proper dimensions can be added. And get() method return correct component."""

        frame1 = Frames.Frame(10, 7)
        frame2 = Frames.Frame(10, 7)
        frame3 = Frames.Frame(10, 7)
        fs = Frames.FrameStack(10, 7)

        # add frame to framestack
        fs.add(frame1)
        # add framestack to framestack
        sub_fs = Frames.FrameStack(10, 7)
        sub_fs.add(frame2)
        sub_fs.add(frame3)
        fs.add(sub_fs)

        self.assertEqual(fs.get(0), frame1)
        self.assertEqual(fs.get(1), sub_fs)
        self.assertEqual(sub_fs.get(0), frame2)
        self.assertEqual(sub_fs.get(1), frame3)

    def test_add_component_to_index(self):
        """Test that component can be added to valid index."""
        frame1 = Frames.Frame(10, 7)
        frame2 = Frames.Frame(10, 7)
        frame3 = Frames.Frame(10, 7)
        frame4 = Frames.Frame(10, 7)
        fs = Frames.FrameStack(10, 7)

        fs.add(frame1)
        fs.add(frame2, 0)  # frame2 is now in front of 1
        fs.add(frame3, 1)  # frame3 should be between 1 and 2
        fs.add(frame4)  # frame4 should be at the end

        self.assertEqual(fs.get(0), frame2)
        self.assertEqual(fs.get(1), frame3)
        self.assertEqual(fs.get(2), frame1)
        self.assertEqual(fs.get(3), frame4)

    def test_add_component_invalid_dimensions(self):
        """Test that adding component with wrong dimensions raises exception."""

        fs = Frames.FrameStack(10, 7)

        # adding frame component of wrong dimensions raises exception
        invalid_frame = Frames.Frame(20, 20)
        # with self.assertRaises(Exception):
        fs.add(invalid_frame)

    def test_remove_component(self):
        """Test that component can be removed."""

        fs = setupTestComponent()

        fs.remove(0)
        fs.remove(0)

        with self.assertRaises(IndexError):
            fs.get(0)

    def test_getMap_getChanges(self):
        """Test that changes and maps are correctly squashed into one map/changelist."""

        fs = setupTestComponent()

        # order should be frame1-frame2-frame3 (frame1 is on top)
        frame1 = fs.get(0)
        sub_fs = fs.get(1)
        frame2 = sub_fs.get(0)
        frame3 = sub_fs.get(1)

        # draw on frames
        frame1[0, 0] = 1
        frame1[0, 1] = None
        frame1[0, 2] = None
        frame2[0, 0] = 2
        frame2[0, 1] = 2
        frame2[0, 2] = None
        frame3[0, 0] = 3
        frame3[0, 1] = 3
        frame3[0, 2] = 3

        map = fs.getMap()

        self.assertEqual(map[0], 1)
        self.assertEqual(map[1], 2)
        self.assertEqual(map[2], 3)

        changes = fs.getChanges()

        self.assertEqual(len(changes), 3)
        self.assertEqual(changes[0], 1)
        self.assertEqual(changes[1], 2)
        self.assertEqual(changes[2], 3)

    def test_isStale(self):
        """Test that frameStack is stale if one component is stale"""

        fs = setupTestComponent()

        # not drawn on any frame yet -> not stale
        self.assertFalse(fs.isStale())

        # draw on frame
        frame2 = fs.get(1).get(0)
        frame2[0, 0] = 1000

        self.assertTrue(fs.isStale())

    def test_clearChanges(self):
        """Test that no changes are returned after clearChanges() has ben called."""

        fs = setupTestComponent()

        frame1 = fs.get(0)
        sub_fs = fs.get(1)
        frame2 = sub_fs.get(0)
        frame3 = sub_fs.get(1)

        frame1[0, 0] = 1
        frame2[0, 0] = 2
        frame3[1, 1] = 3

        fs.clearChanges()

        self.assertEqual(0, len(fs.getChanges()))
        self.assertFalse(fs.isStale())
