import unittest

from python_ledbox.Images import ImageLoader, Image
from python_ledbox.Frames import Frame
from python_ledbox.Color import Color

BASE_PATH = "./tests/files/"


class TestImageLoader(unittest.TestCase):
    def setUp(self):
        """Create imageloader instance for each testcase."""
        self.imageLoader = ImageLoader()

    def test_load_get_single_image_successful(self):
        """Test that loading valid image and getting is successful."""

        self.imageLoader.load(f"{BASE_PATH}imagedir/testpic.png")
        self.assertIsNotNone(self.imageLoader.get("testpic"))

    def test_load_get_images_in_dir_successful(self):
        """Test that loading and gettings images from directory is successfull."""

        self.imageLoader.load(f"{BASE_PATH}imagedir/")

        self.assertIsNotNone(self.imageLoader.get("testpic"))
        self.assertIsNotNone(self.imageLoader.get("testpic2"))

    def test_load_image_not_exist(self):
        """Test that exception is raised if image in given path does not exist."""

        with self.assertRaises(FileNotFoundError) as context:
            self.imageLoader.load(f"{BASE_PATH}nonexistent.png")

    def test_load_image_name_already_used(self):
        """Test that exception is raised if image with same filename is already loaded."""

        self.imageLoader.load(f"{BASE_PATH}imagedir/testpic.png")

        with self.assertRaises(ValueError) as context:
            self.imageLoader.load(f"{BASE_PATH}imagedir/testpic.png")

        self.assertEqual(
            "Image with filename already loaded.", context.exception.__str__()
        )

    def test_load_image_name_already_used_overwrite(self):
        """Test that no exception is raided if image with same filename is already loaded and overwrite parameter is set to True."""

        try:
            self.imageLoader.load(f"{BASE_PATH}imagedir/testpic.png")
            self.imageLoader.load(f"{BASE_PATH}imagedir/testpic.png", overwrite=True)
        except ValueError:
            self.fail(
                "ValueError should not be raised, as overwrite parameter is set to True"
            )

    def test_get_image_not_found_returns_None(self):
        """Test that None is returned if the name given does not match a loaded image."""

        image = self.imageLoader.get("nonexistentfile")
        self.assertIsNone(image)

    def test_image_format_invalid(self):
        """Test that using not supported image type raises exception."""

        with self.assertRaises(ValueError) as context:
            self.imageLoader.load("filewithnoextension")

        self.assertEqual(
            "Image file format not supported.", context.exception.__str__()
        )

        with self.assertRaises(ValueError) as context:
            self.imageLoader.load("filewithin")
        self.assertEqual(
            "Image file format not supported.", context.exception.__str__()
        )


class TestImage(unittest.TestCase):
    def setUp(self):
        """Create objects necessary for each testcase."""

        imgLoader = ImageLoader()
        imgLoader.load(f"{BASE_PATH}imagedir/testpic2.png")

        self.image: Image = imgLoader.get("testpic2")

        self.frame: Frame = Frame(10, 7)

    def test_getRowCount(self):
        """Test that the getRowCount() method returns the amount of rows of the image."""
        self.assertEqual(self.image.getRowCount(), 4)

    def test_getColCount(self):
        """Test that the getColCount() method returns the amount of columns of the image."""
        self.assertEqual(self.image.getColCount(), 3)

    def test_applyToFrame(self):
        """Test that image can be applied to a frame."""

        self.image.applyToFrame(self.frame, 1, 1)

        # 12 changes should be recorded
        self.assertEqual(len(self.frame.getChanges()), 12)

        self.assertEqual(self.frame[1, 1], Color.from_rgb(0, 0, 0))
        self.assertEqual(self.frame[1, 2], Color.from_rgb(255, 255, 255))
        self.assertEqual(self.frame[1, 3], None)
        self.assertEqual(self.frame[2, 1], Color.from_rgb(255, 0, 0))
        self.assertEqual(self.frame[2, 2], Color.from_rgb(0, 0, 255))
        self.assertEqual(self.frame[2, 3], Color.from_rgb(0, 255, 0))

        # semi transparent colors should become completely transparent (None)
        self.assertEqual(self.frame[4, 1], None)
        self.assertEqual(self.frame[4, 2], None)
        self.assertEqual(self.frame[4, 3], None)

    def test_applyToFrame_recolor(self):
        """Test that image can be recolored and applied to frame."""

        # black -> white, red -> green, transparent -> red
        colorRemappings = {
            Color.from_rgb(0, 0, 0): Color.from_rgb(255, 255, 255),
            Color.from_rgb(255, 0, 0): Color.from_rgb(0, 255, 0),
            None: Color.from_rgb(255, 0, 0),
        }

        self.image.applyToFrame(self.frame, 1, 1, colorRemappings)

        self.assertEqual(self.frame[1, 1], Color.from_rgb(255, 255, 255))
        self.assertEqual(self.frame[2, 1], Color.from_rgb(0, 255, 0))
        self.assertEqual(self.frame[1, 3], Color.from_rgb(255, 0, 0))

        # semi transparent should be red as well
        self.assertEqual(self.frame[4, 1], Color.from_rgb(255, 0, 0))

    def test_applyImage_cutoff_positive(self):
        """Test that image that would overhang the frame in positive x-y direction is cut off."""

        # only first two rows of first column should be applied
        self.image.applyToFrame(self.frame, 8, 6)

        self.assertEqual(len(self.frame.getChanges()), 2)

        self.assertEqual(self.frame[8, 6], Color.from_rgb(0, 0, 0))
        self.assertEqual(self.frame[9, 6], Color.from_rgb(255, 0, 0))

    def test_applyImage_cutoff_negative(self):
        """Test that image that would overhang the frame in negative x-y direction is cut off."""

        # only first two rows of first column should be applied
        self.image.applyToFrame(self.frame, -2, -1)

        self.assertEqual(len(self.frame.getChanges()), 4)

        self.assertEqual(self.frame[0, 0], Color.from_rgb(0, 255, 255))
        self.assertEqual(self.frame[0, 1], Color.from_rgb(255, 255, 0))
        self.assertEqual(self.frame[1, 0], None)
        self.assertEqual(self.frame[1, 1], None)
