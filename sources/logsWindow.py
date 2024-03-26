from PySide6.QtWidgets import QListWidgetItem

from sources.pyui.logsWindowUI import Ui_Dialog
from sources.logViewer import LogViewer


class LogsWindow(Ui_Dialog):
    def __init__(self):
        super(LogsWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Logs")
        self.logViewer = LogViewer()

        self.logs = {}
        self.listWidget.itemClicked.connect(self.showLogs)

    def refresh(self):
        self.listWidget.clear()
        for log in self.logs.keys():
            item = QListWidgetItem(log)
            item.setData(1, self.logs[log])
            self.listWidget.addItem(item)

    def showLogs(self, item:QListWidgetItem):
        title = item.text()
        print("* Show Logs: " + title)
        self.logViewer.show_log(title)

    def appendLog(self, logname, path):
        self.logs.update({logname: path})
