from datetime import datetime


class Logger(object):

    def __init__(self,no_timer):
        self._no_Timer = no_timer

    def log(self, level, msg):
        if self._no_Timer:
            print("[" + level + "] " + msg)
        else:
            print(str(datetime.now()) + " [" + level + "] " + msg)

    def warn(self, msg):
        self.log("Warning", msg)

    def error(self, msg):
        self.log("Error", msg)

    def info(self,msg):
        self.log("Info", msg)
