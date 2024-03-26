import io

from PySide6.QtWidgets import QWidget

from const.CONSTANTS import SEPARATOR
from sources.pyui.logViewerUI import Ui_Form


class LogViewer(QWidget, Ui_Form):
    def __init__(self):
        super(LogViewer, self).__init__()

        self.setupUi(self)
        self.setWindowTitle("Logs")

    def read(self, name):
        filepath = f'logs{SEPARATOR}{name}_logs.log'
        with open(filepath, 'r') as f:
            try:
                lines = f.readlines()
            except io.UnsupportedOperation:
                lines = f.readlines()
        return lines

    def show_log(self, logname):
        lines = self.read(logname)
        for line in lines:
            self.plainTextEdit.setPlainText(line + "\n")
        self.show()
