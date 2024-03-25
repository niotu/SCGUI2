import io
from const.CONSTANTS import SEPARATOR
from PySide6.QtCore import QByteArray

class Logger:
    def __init__(self):
        pass

    def write(self, name, info: QByteArray):
        mode = "ab"
        if name == 'errors_QT':
            mode = 'a'
            info += '\n'
        print("calling write")

        filepath = f'logs{SEPARATOR}{name}_logs.log'
        with open(filepath, mode) as f:
            f.write(bytes(info))

    def read(self, name):
        filepath = f'logs{SEPARATOR}{name}_logs.log'
        with open(filepath, 'r') as f:
            try:
                lines = f.readlines()
            except io.UnsupportedOperation:
                lines = f.readlines()
        return lines
