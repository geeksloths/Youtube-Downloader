import math


class Time:
    def __init__(self, time=0):
        self.time = time
        self.hour = "00"
        self.minute = "00"
        self.second = "00"
        self.converted = ""

    def convert(self):
        self.set_hour()
        self.set_minute()
        self.set_seconds()
        return self.converted

    def set_hour(self):
        hour = self.time / 3600
        hour = math.floor(hour)
        if not hour == 0:
            if hour < 10:
                self.hour = "0" + str(hour)
            else:
                self.hour = str(hour)
            self.converted += self.hour
        else:
            self.hour = None

    def set_minute(self):
        if self.hour is None:
            minute = self.time / 60
            minute = math.floor(minute)
            if minute < 10:
                self.minute = "0" + str(minute)
            else:
                self.minute = str(minute)
            self.converted += self.minute
        else:
            hour = math.floor(self.time / 3600)
            left_sec = self.time - (hour * 3600)
            minute = math.floor(left_sec / 60)
            if minute < 10:
                self.minute = "0" + str(minute)
            else:
                self.minute = str(minute)
            self.converted += ":" + self.minute

    def set_seconds(self):
        left_sec = self.time - (math.floor(self.time / 3600) * 3600)
        left = left_sec - (math.floor(left_sec / 60) * 60)
        if left < 10:
            self.second = "0" + str(left)
        else:
            self.second = str(left)
        self.converted += ":" + self.second
