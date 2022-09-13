from multiprocessing.connection import wait
import unittest
from unittest.mock import Mock, MagicMock, patch

from python_ledbox.App import App
from python_ledbox.events import AppEvent

import time


class TestApp(unittest.TestCase):
    def fake_mainloop(self):
        while True:
            time.sleep(1)

    @patch.multiple(App, __abstractmethods__=set())
    @patch.object(App, "_mainloop", fake_mainloop)
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
        self.assertEqual(app.signalQueue.get(block=False).event, AppEvent.START)
        self.assertTrue(app._mainloopThread.is_alive())

    @patch.multiple(App, __abstractmethods__=set())
    @patch.object(App, "_mainloop", fake_mainloop)
    def test_stop_stopps_app(self):
        """Test that calling stop() methods makes app be inactive."""

        # initialize and start app
        app = App()
        app.start()
        app.signalQueue.get()  # clear start signal in queue

        # stop app
        app.stop()
        self.assertFalse(app.isActive())
        self.assertEqual(app.signalQueue.get().event, AppEvent.STOP)

    @patch.multiple(App, __abstractmethods__=set())
    @patch.object(App, "_mainloop", fake_mainloop)
    def test_kill_calls_stop(self):
        """Test that calling kill() will call stop() by default."""

        app = App()
        app.start()

        # mock stop method to count calls
        # app.stop = MagicMock(side_effect=app.stop)
        app.signalQueue.get()  # clear start signal in queue

        # kill app
        app.kill()

        self.assertFalse(app.isInitialised())
        self.assertFalse(app.isActive())
        self.assertEqual(app.signalQueue.get().event, AppEvent.KILL)

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
