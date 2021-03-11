import unittest
from unittest.mock import Mock, MagicMock

from python_ledbox.App import App


class TestApp(unittest.TestCase):
    def test_initialisation_and_start(self):
        """Test that calling start for the first time causes app to be initialized and active."""

        app = App()

        # app should not be running
        self.assertFalse(app.isInitialised())
        self.assertFalse(app.isActive())

        # start app for first time
        app.start()

        self.assertTrue(app.isInitialised())
        self.assertTrue(app.isActive())

    def test_stop_stopps_app(self):
        """Test that calling stop() methods makes app be inactive."""

        # initialize and start app
        app = App()
        app.start()

        # stop app
        app.stop()
        self.assertFalse(app.isActive())

    def test_kill_calls_stop(self):
        """Test that calling kill() will call stop() by default."""

        app = App()
        app.start()

        # mock stop method to count calls
        app.stop = MagicMock(side_effect=app.stop)

        # kill app
        app.kill()

        app.stop.assert_called_once()
        self.assertFalse(app.isInitialised())
        self.assertFalse(app.isActive())

    # def test_resume_calls_start(self):
    #     """Test that calling resume() will call start() by default."""

    #     app = App(mockMatrix)

    #     # mock start method to count calls
    #     app.start = MagicMock(side_effect=app.start)

    #     app.start()
    #     # stop app
    #     app.stop()

    #     # resume app
    #     app.resume()
    #     self.assertEqual(len(app.start.call_args_list), 2)
    #     self.assertTrue(app.isActive())

    # def test_resume_before_initialize_raises_exeption(self):
    #     """Test that calling resume before starting app raises an exception."""

    #     app = App(mockMatrix)

    #     with self.assertRaises(Exception):
    #         app.resume()
