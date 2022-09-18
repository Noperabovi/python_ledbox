import unittest
from unittest.mock import Mock, patch
from queue import Queue
import time

from python_ledbox.App import App
from python_ledbox.apps.mainapp import MainApp
from python_ledbox.events import AppEvent, Signal, MouseEvent
from python_ledbox.Matrix import MatrixEvent
from python_ledbox.Frames import Frame, FrameComponent


class TestMainApp(unittest.TestCase):
    def fake_mainloop(self):
        while True:
            time.sleep(1)

    @patch.multiple(App, __abstractmethods__=set())
    @patch.object(App, "_mainloop", fake_mainloop)
    def setUp(self):
        self.app: App = App()
        self.app2: App = App()
        self.signalQueue: Queue[Signal] = Queue()
        self.mainApp: MainApp = MainApp(
            Mock(), signalQueue=self.signalQueue, apps=[self.app, self.app2]
        )

    def test_initialisation_and_start(self):
        """Test that calling start() on mainapp will start the first app."""

        # app should not be running
        self.assertFalse(self.app.isInitialised())
        self.assertFalse(self.app.isActive())

        # start mainapp for first time
        self.mainApp.start()

        # should also start first app
        self.assertTrue(self.app.isInitialised())
        self.assertTrue(self.app.isActive())
        self.assertTrue(self.app._mainloopThread.is_alive())

        # should not start second app
        self.assertFalse(self.app2.isInitialised())
        self.assertFalse(self.app2.isActive())
        self.assertFalse(self.app2._mainloopThread.is_alive())

    def test_stop_stopps_app(self):
        """Test that calling stop() on mainapp will cause the current app to stop"""

        self.mainApp.start()
        self.app.signalQueue.get()  # clear start signal in queue

        # stop mainapp
        self.mainApp.stop()

        # first app should be stopped
        self.assertFalse(self.app.isActive())
        self.assertEqual(self.app.signalQueue.get().event, AppEvent.STOP)

    def test_kill_kills_all_apps(self):

        self.mainApp.start()
        self.app2.start()  # start second app manually
        self.app.signalQueue.get()  # clear start signal in queue
        self.app2.signalQueue.get()  # clear start signal in queue

        self.mainApp.kill()

        # both apps should be stopped and exited
        self.assertFalse(self.app.isInitialised())
        self.assertFalse(self.app.isActive())
        self.assertEqual(self.app.signalQueue.get().event, AppEvent.KILL)

        self.assertFalse(self.app2.isInitialised())
        self.assertFalse(self.app2.isActive())
        self.assertEqual(self.app2.signalQueue.get().event, AppEvent.KILL)

        # mainloop should exit
        time.sleep(0.1)  # wait for thread to receive signal
        self.assertFalse(self.mainApp._mainloopThread.is_alive())

    def test_no_app_fails_initialization(self):
        """Test that mainapp cannot be initialized without at least one app."""

        with self.assertRaises(ValueError):
            MainApp(None, Queue(), [])

    def test_switching_to_next_app(self):
        """Test that switching to next app will stop the current one and start the next."""

        self.mainApp.start()
        self.mainApp.next_app()

        self.assertFalse(self.app.isActive())
        self.assertTrue(self.app2.isActive())

    def test_switching_to_previous_app(self):
        """Test that switching to previous app will stop the current one and start the previous."""

        self.mainApp.start()
        self.mainApp.prev_app()

        self.assertFalse(self.app.isActive())
        self.assertTrue(self.app2.isActive())

    def test_matrix_update_on_update_event(self):
        """Test that putting a MatrixEvent.UPDATE Signal into the mainapp's signalQueue will call applyChanges on matrix."""

        self.mainApp.start()
        time.sleep(0.1)
        self.mainApp.signalQueue.put(Signal(MatrixEvent.UPDATE, {1: 1}))
        time.sleep(0.1)

        call_args: Signal = self.mainApp._MainApp__matrix.applyChanges.call_args.args
        self.assertEqual(1, len(call_args))
        self.assertEqual({1: 1}, call_args[0])

    def test_matrix_repaint_on_repaint_event(self):
        """Test that putting a MatrixEvent.REPAINT Signal into the mainapp's signalQueue will call applyMap on matrix."""

        self.mainApp.start()
        self.mainApp.signalQueue.put(Signal(MatrixEvent.REPAINT, {1: 1}))
        time.sleep(0.1)

        call_args: Signal = self.mainApp._MainApp__matrix.applyMap.call_args.args
        self.assertEqual(1, len(call_args))
        self.assertEqual({1: 1}, call_args[0])

    def test_matrix_clear_on_clear_event(self):
        """Test that putting a MatrixEvent.CLEAR Signal into the mainapp's signalQueue will call clear on matrix."""

        self.mainApp.start()
        self.mainApp.signalQueue.put(Signal(MatrixEvent.CLEAR))
        time.sleep(0.1)

        self.mainApp._MainApp__matrix.clear.assert_called_once()

    def test_call_nextapp_on_nextapp_event(self):
        """est that next_app method is called when putting next_app_event signal into queue."""

        self.mainApp.next_app = Mock()
        self.mainApp.next_app_event = MouseEvent.MOUSE_CLICK_LEFT
        self.mainApp.start()
        self.mainApp.signalQueue.put(Signal(self.mainApp.next_app_event))
        time.sleep(0.1)

        self.assertEqual(1, self.mainApp.next_app.call_count)

    def test_call_prevapp_on_prevapp_event(self):
        """Test that prev_app method is called when putting prev_app_event signal into queue."""

        self.mainApp.prev_app = Mock()
        self.mainApp.prev_app_event = MouseEvent.MOUSE_CLICK_LEFT
        self.mainApp.start()
        self.mainApp.signalQueue.put(Signal(self.mainApp.prev_app_event))
        time.sleep(0.1)

        self.assertEqual(1, self.mainApp.prev_app.call_count)

    def test_equal_prev_next_events_fails_initialization(self):
        """Test that prev_app_event and next_app_event cannot be qual"""

        with self.assertRaises(ValueError):
            MainApp(
                "matrix",
                self.signalQueue,
                [self.app],
                prev_app_event=MouseEvent.MOUSE_CLICK_LEFT,
                next_app_event=MouseEvent.MOUSE_CLICK_LEFT,
            )
