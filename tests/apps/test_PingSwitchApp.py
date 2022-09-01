# import unittest
# from unittest.mock import patch, Mock

# from datetime import datetime
# import time

# from python_ledbox.apps.PingSwitchApp import PingSwitchApp

# # learning from testing with threads
# # - use time.sleep for forcing thread switch
# # - stop the thread after each testcase
# #   (Possble problem that I encountered: the patched methods are not properly patched anymore and lead to errors)


# class TestPingSwitchApp(unittest.TestCase):
#     def setUp(self):
#         self.switch = PingSwitchApp("localhost")
#         self.switch.startDelay = 1
#         self.switch.stopDelay = 5
#         self.switch.apps = [Mock(), Mock()]

#     @patch("python_ledbox.apps.PingSwitchApp.subprocess")
#     @patch("python_ledbox.apps.PingSwitchApp.datetime")
#     @patch("python_ledbox.apps.PingSwitchApp.time")
#     def test_start_app(self, mock_time, mock_dt, mock_subprocess):
#         """Test that starting app starts apps inside after startDelay."""

#         mock_subprocess.call = Mock(return_value=0)
#         mock_time.sleep = Mock(side_effect=lambda x: time.sleep(0.001))
#         mock_dt.utcnow = Mock(return_value=datetime(2000, 1, 1, 0, 0))

#         self.switch.start()

#         # switch should be running but apps not active
#         self.assertTrue(self.switch.isActive())
#         self.assertFalse(self.switch.apps[0].start.called)

#         # update time
#         mock_dt.utcnow = Mock(return_value=datetime(2000, 1, 1, 0, 1))
#         time.sleep(0.01)

#         # app should be running 1 minute later
#         self.assertTrue(self.switch.apps[0].start.called)
#         self.assertTrue(self.switch.apps[1].start.called)

#         self.switch.stop()

#     # # TODO eliminate repeated code by createing extra decorated method
#     @patch("python_ledbox.apps.PingSwitchApp.subprocess")
#     @patch("python_ledbox.apps.PingSwitchApp.datetime")
#     @patch("python_ledbox.apps.PingSwitchApp.time")
#     def test_stops_app(self, mock_time, mock_dt, mock_subprocess):
#         """Test that app is stopped after ip-address becomes unreachable."""

#         mock_subprocess.call = Mock(return_value=0)

#         # forces thread to be switched
#         mock_time.sleep = Mock(side_effect=lambda x: time.sleep(0.001))

#         mock_dt.utcnow = Mock(return_value=datetime(2000, 1, 1, 1, 0))
#         self.switch.start()

#         mock_dt.utcnow = Mock(return_value=datetime(2000, 1, 1, 1, 1))
#         time.sleep(0.01)

#         # switch should be running and apps active
#         self.assertTrue(self.switch.isActive())
#         self.assertTrue(self.switch.apps[0].start.called)

#         # ip is not responding
#         mock_subprocess.call = Mock(return_value=1)
#         time.sleep(0.01)

#         # stop interval reached
#         mock_dt.utcnow = Mock(return_value=datetime(2000, 1, 1, 1, 6))
#         time.sleep(0.01)
#         self.assertTrue(self.switch.apps[0].stop.called)

#         self.switch.stop()

#     @patch("python_ledbox.apps.PingSwitchApp.subprocess")
#     @patch("python_ledbox.apps.PingSwitchApp.datetime")
#     @patch("python_ledbox.apps.PingSwitchApp.time")
#     def test_kills_app(self, mock_time, mock_dt, mock_subprocess):
#         """Test that app is killed after ip-address becomes unreachable."""

#         self.switch.killOnStop = True

#         mock_subprocess.call = Mock(return_value=0)

#         # forces thread to be switched
#         mock_time.sleep = Mock(side_effect=lambda x: time.sleep(0.001))

#         mock_dt.utcnow = Mock(return_value=datetime(2000, 1, 1, 1, 0))
#         self.switch.start()

#         mock_dt.utcnow = Mock(return_value=datetime(2000, 1, 1, 1, 1))
#         time.sleep(0.01)

#         # switch should be running and apps active
#         self.assertTrue(self.switch.isActive())
#         self.assertTrue(self.switch.apps[0].start.called)

#         # ip is not responding
#         mock_subprocess.call = Mock(return_value=1)
#         time.sleep(0.01)

#         # stop interval reached
#         mock_dt.utcnow = Mock(return_value=datetime(2000, 1, 1, 1, 6))
#         time.sleep(0.01)
#         self.assertTrue(self.switch.apps[0].kill.called)

#         self.switch.stop()

#     # def test_exception_invalid_ip(self):
#     #     """Test that exception is thrown if the ip is invalid."""
