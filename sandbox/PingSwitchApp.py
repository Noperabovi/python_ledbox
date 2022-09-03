import platform
import subprocess
from threading import Thread
from typing import List
from datetime import datetime  # , timedelta
import time


from python_ledbox.App import App


class PingSwitchApp(App):
    def __init__(self, ipAddress: str):
        App.__init__(self)
        # configurables
        self.ipAddress: str = ipAddress
        self.startDelay: int = 60
        self.stopDelay: int = 300
        self.pingInterval: int = 60
        self.killOnStop: bool = False
        self.apps: List[App] = []

        self.__appsRunning: bool = False
        self.__online_since: int = None
        self.__offline_since: int = None

    def __ping(self, host: str):
        """
        Returns True if host (str) responds to a ping request.
        Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
        """

        # Option for the number of packets as a function of
        packets = "-n" if platform.system().lower() == "windows" else "-c"

        # Building the command. Ex: "ping -c 1 google.com"
        command = f"ping -w 1 {packets} 1 {host}".split(" ")

        # supress output with stdout=DEVNULL
        return subprocess.call(command, stdout=subprocess.DEVNULL) == 0

    def __updateStatus(self, now: datetime) -> None:

        pingSuccessful = self.__ping(self.ipAddress)
        print(pingSuccessful)

        # first uncessful ping
        if self.__appsRunning and not pingSuccessful:
            if self.__offline_since is None:
                self.__offline_since = now
                self.__online_since = None

            seconds_offline = (now - self.__offline_since).total_seconds()

            # print(seconds_offline)

            # stop matrix
            # add 1 to account for deviations in time.sleep
            if seconds_offline + 1 > self.stopDelay:
                self.__appsRunning = False
                for app in self.apps:
                    if self.killOnStop:
                        app.kill()
                    else:
                        app.stop()

        # first successful ping
        elif not self.__appsRunning and pingSuccessful:
            if self.__online_since is None:
                self.__online_since = now
                self.__offline_since = None

            seconds_online = (now - self.__online_since).total_seconds()

            # start matrix
            if seconds_online + 1 > self.startDelay:
                self.__appsRunning = True
                for app in self.apps:
                    app.start()

    def __pingLoop(self):
        while self._isActive:
            self.__updateStatus(datetime.utcnow())
            time.sleep(self.pingInterval)

    def start(self):
        super().start()
        Thread(target=self.__pingLoop, daemon=True).start()

    def stop(self):
        super().stop()
