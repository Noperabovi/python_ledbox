#! /home/pi/.local/share/virtualenvs/python_ledbox-6hKBgy5z/bin/python

from piclap import *
from python_ledbox import Frames, TerminalMatrix, Images, PiMatrix
from python_ledbox import Color

from python_ledbox.apps.ClockApp import ClockApp
from python_ledbox.apps.PingSwitchApp import PingSwitchApp

import _thread as thread
import threading
import time
from datetime import datetime
import logging

logging.basicConfig(
    format="%(levelname)s %(asctime)s     %(message)s",
    filename="/home/pi/Documents/python_ledbox/.vscode/clapperclock.log",
    level=logging.INFO,
    datefmt="%m/%d/%Y %I:%M:%S %p",
)

class CustomDevice(Device):
    def readData(self):
        """Reads a single chunk of binary data from stream"""
        return self.stream.read(self.config.chunk_size, exception_on_overflow = False)

class CustomListener(Listener):
    def __init__(self, config=None, calibrate=True):
        super().__init__(config, calibrate)

        self.device = CustomDevice(self.config, calibrate)
        self.confirm()

        self.terminalMatrix = TerminalMatrix.TerminalMatrix(10, 10)
        self.piMatrix = PiMatrix.PiMatrix(10, 10, 18)
        self.frame = Frames.Frame(10, 10)

        self.IP_PC = "192.168.1.100"
        self.IP_Phone = "192.168.1.101"
        self.pcOnline = False
        self.phoneOnline = False

        self.clockApp = ClockApp(self.piMatrix, self.frame)

        self.clockApp.hour_first_digit_color = Color.from_rgb(25, 0, 0)
        self.clockApp.hour_second_digit_color = Color.from_rgb(25, 0, 5)
        self.clockApp.minute_first_digit_color = Color.from_rgb(25, 0, 5)
        self.clockApp.minute_second_digit_color = Color.from_rgb(25, 0, 0)

        # self.clockApp.hour_first_digit_color = Color.from_rgb(255, 0, 0)
        # self.clockApp.hour_second_digit_color = Color.from_rgb(255, 0, 5)
        # self.clockApp.minute_first_digit_color = Color.from_rgb(255, 0, 5)
        # self.clockApp.minute_second_digit_color = Color.from_rgb(255, 0, 0)


        self.clockApp.hour_first_digit_pos = (0, 1)
        self.clockApp.hour_second_digit_pos = (0, 6)
        self.clockApp.minute_first_digit_pos = (5, 1)
        self.clockApp.minute_second_digit_pos = (5, 6)

        # start checking if pc is online
        threading.Thread(target=self.__pingLoop, daemon=True).start()

    # overwrite to skip user interaction
    def confirm(self):
        pass

    def __pingLoop(self):
        while True:
            self.pcOnline = PingSwitchApp.ping(self.IP_PC)
            time.sleep(30)
            self.phoneOnline = PingSwitchApp.ping(self.IP_Phone)
            time.sleep(30)

    def listenClaps(self, threadName):
        """This method runs on a child thread with :attr:`lock` when :attr:`claps` equals ``1`` and reset the class property :attr:`claps` to ``0`` when execution is finished
        :param str threadName: Name of the child thread started
        """

        # setup clock app

        with self.lock:
            self.clapWait(self.claps)

            logText = "ACTIVATION THRESHOLD EXCEEDED  "

            hour = datetime.now().hour
            isActiveHour = hour >= 22 or hour <= 8

            # if not self.pcOnline and not self.phoneOnline and isActiveHour:
            #     self.clockApp.start()
            #     time.sleep(5)
            #     self.clockApp.stop()
            #     self.piMatrix.clear()
            #     logText = logText + "CLOCK ACTIVATED FOR 5 SECONDS  "
            # else:
            #     logText = logText + f"ACTIVE_HOUR: {isActiveHour}  "
            #     logText = logText + f"PC_ONLINE: {self.pcOnline}  "
            #     logText = logText + f"PHONE_ONLINE: {self.phoneOnline}  "

            logging.info(logText)

            self.claps = 0

    # overwrite clear matrix and stop clock on keyboard interrupt
    def start(self):
        """When this method is called, the listener start reading binary data from stream and sreach for claps inside the chunks of data using :class:`SignalProcessor` until :attr:`Settings.exit` flag is ``True``
        :raises: ``KeyboardInterrupt``: If **Control + C** is pressed on keyboard
        """
        try:
            self.device.openStream()
            logging.info("started clapperclock")
            logging.info(f"channel count: {self.config.channels}")
            while not self.config.exit:
                try:
                    data = self.device.readData()
                except (OSError, IOError):
                    data = None
                if self.processor.findClap(data):
                    self.claps += 1
                if self.claps == 1 and not self.lock.locked():
                    thread.start_new_thread(self.listenClaps, ("ListenClaps",))
        except (KeyboardInterrupt, SystemExit):
            logging.warning("stopped clapperclock")
            listener.clockApp.stop()
            listener.piMatrix.clear()
        self.stop()


class Config(Settings):
    """Describes custom configurations and action methods to be executed based
    on the number of claps detected.
    """

    def __init__(self):
        super().__init__()
        self.chunk_size = 512  # Reduce as power of 2 if pyaudio overflow
        self.wait = 0.5  # Adjust wait between claps
        self.method.value = 150  # Threshold value adjustment


if __name__ == "__main__":
    # TODO use >=150 as threshold

    try:
        config = Config()
        listener = CustomListener(config, calibrate=False)
        listener.piMatrix.clear()
        listener.start()
    except (SystemExit, KeyboardInterrupt) as e:
        logging.critical(f"clapperclock failed: {e}")
