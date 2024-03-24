from PySide6.QtWidgets import QWidget

from logViewerUI import Ui_Form


class LogViewer(QWidget, Ui_Form):
    def __init__(self):
        super(LogViewer, self).__init__()

        self.setupUi(self)
        self.setWindowTitle("Logs")