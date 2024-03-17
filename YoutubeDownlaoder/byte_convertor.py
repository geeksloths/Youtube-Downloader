import math


class Convertor:
    def __init__(self, size):
        self.size = int(size)

    def convert(self):
        # 1kb = 1024 byte
        # 1MB = 1048576 byte
        # 1GB = 1073741824 byte
        if self.size < 1048576:
            unit_scale = 1024
            unit = "KB"
            return self.converting(unit, unit_scale)
        elif 1048576 < self.size < 1073741824:
            unit_scale = 1048576
            unit = "MB"
            return self.converting(unit, unit_scale)
        elif self.size > 1073741824:
            unit_scale = 1073741824
            unit = "GB"
            converted_size = self.size / 1024000
            return self.converting(unit, unit_scale)

    def converting(self, unit, unit_scale):
        converted_size = self.size / unit_scale
        complete_num = math.floor(converted_size)
        left_num = converted_size - complete_num
        left_num = math.floor(left_num * 10)
        converted_size = str(complete_num) + "." + str(left_num)
        return converted_size + " " + unit
