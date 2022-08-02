import platform
import subprocess
from threading import Thread
from typing import List
from datetime import datetime, timedelta
import time


from python_ledbox.App import App


class PingSwitchApp:
    def __init__(self, ipAddress: str):

        # configurables
        self.ipAddress: str = ipAddress
        self.startDelay: int = 60
        self.stopDelay: int = 300
        self.pingInterval: int = 60
        self.killOnStop: bool = False
        self.apps: List[App] = []

        self.__isActive: bool = None
        self.__appsRunning: bool = False
        self.__online_since: int = None
        self.__offline_since: int = None
        self.__pingThread = Thread(
            target=self.__pingLoop, daemon=True
        )  # get more info about daemonizing and what happens if not used

    def __ping(self, host: str):
        """
        Returns True if host (str) responds to a ping request.
        Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
        """

        # Option for the number of packets as a function of
        param = "-n" if platform.system().lower() == "windows" else "-c"

        # Building the command. Ex: "ping -c 1 google.com"
        command = ["ping", param, "1", host]

        # supress output with stdout=DEVNULL
        return subprocess.call(command, stdout=subprocess.DEVNULL) == 0

    def __pingLoop(self):
        while True:
            if self.__isActive:
                pingSuccessful = self.__ping(self.ipAddress)
                now = datetime.utcnow()
                seconds_online = (now - self.__online_since).total_seconds()
                seconds_offline = (now - self.__offline_since).total_seconds()

                # first uncessful ping
                if self.__appsRunning and not pingSuccessful:
                    if self.__offline_since is None:
                        self.__offline_since = now
                        self.__online_since = None

                    # stop matrix
                    # add 1 to account for deviations in time.sleep
                    if seconds_offline + 1 > self.stopDelay:
                        self.__appsRunning = False
                        for app in self.apps:
                            if self.killOnStop:
                                app.kill()
                            else:
                                app.start()

                # first successful ping
                elif not self.__appsRunning and pingSuccessful:
                    if self.__online_since is None:
                        self.__online_since = now
                        self.__offline_since = None

                    # start matrix
                    if seconds_online + 1 > self.startDelay:
                        self.__appsRunning = True
                        for app in self.apps:
                            if self.killOnStop:
                                app.start()
                            else:
                                app.resume()

                time.sleep(self.pingInterval)

            else:
                time.sleep(1)

    def start(self):
        if self.isActive is None:
            self.__pingThread.start()
            print("initialized")

        self.__isActive = True

    def stop(self):
        self.__isActive = False


if __name__ == "__main__":

    ps = PingSwitchApp()

    # print("ping localhost")
    # print(ps.__ping("localhost"))
    # print("ping asdf2324asdf")
    # print(ps.__ping("asdf2324asdf"))
    # time.sleep(4)

    print("phone online:")
    while True:
        print("YES" if ps.ping("192.168.1.69") else "NO")
        time.sleep(5)

    print("created but not started")
    time.sleep(1)
    print("starting, stopping after 5 more seconds")
    ps.start()
    time.sleep(5)
    ps.stop()
    print("stopped, starting in 2 seconds")
    time.sleep(2)
    print("starting")
    ps.start()
