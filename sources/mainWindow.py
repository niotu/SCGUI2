import json
import os.path

from PySide6.QtCore import Qt, QProcess, QSize
from PySide6.QtGui import QFont, QIcon
from PySide6.QtWidgets import QListWidgetItem, QFileDialog

from const.CONSTANTS import *
from sources.pyui.MainWindowUI import Ui_MainWindow
from sources.Logger import Logger
from sources.logsWindow import LogsWindow

logger = Logger()


class Task:
    pass


def translate(inp):
    res = ""
    for l in inp:
        if l in RUSSIAN:
            res += ALFA[l]
        else:
            res += l
    return res


class MainWindow(Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.default_icon = QIcon(COMMON_ICON_ROOT)
        self.loading_icon = QIcon(LOADING_ICON_ROOT)
        self.error_icon = QIcon(ERROR_ICON_ROOT)
        self.done_icon = QIcon(DONE_ICON_ROOT)
        self.settings_icon = QIcon(SETTINGS_ICON_ROOT)
        self.update_icon = QIcon(UPDATE_ICON_ROOT)
        self.tasks = []
        self.logsWindow = LogsWindow()

        self.setupUi(self)
        # self.logger = Logger()

        styles = open(STYLES_ROOT, encoding='utf-8').read()
        self.settingsButton = QListWidgetItem(self.listWidget_4)
        self.settingsButton.setTextAlignment(Qt.AlignCenter)
        self.settingsButton.setIcon(self.settings_icon)
        self.settingsButton.setText("Settings")

        self.updateButton = QListWidgetItem(self.listWidget_4)
        self.updateButton.setTextAlignment(Qt.AlignCenter)
        self.updateButton.setIcon(self.update_icon)
        self.updateButton.setText("Update")

        self.listWidget_4.setIconSize(QSize(28, 28))
        self.listWidget_4.itemClicked.connect(self.tool_bar_clicked)

        self.setStyleSheet(styles)

        self.listWidget.itemClicked.connect(self.clicked_on_parser)
        self.listWidget.setSpacing(SPACING)

        self.listWidget_2.itemClicked.connect(self.clicked_on_file)
        self.listWidget_2.setSpacing(SPACING)

        self.listWidget_3.itemClicked.connect(self.clicked_on_dir)
        self.listWidget_3.setSpacing(SPACING)

        self.label.setAlignment(Qt.AlignCenter)

        self.label_2.setAlignment(Qt.AlignCenter)

        self.label_3.setAlignment(Qt.AlignCenter)

        f = open(CONFIGURE, encoding="utf-8").read()

        self.scripts = json.loads(f)
        self.parsers = self.scripts["parsers"]
        self.on_file = self.scripts["on_file"]
        self.on_dir = self.scripts["on_dir"]
        self.python = self.scripts["programs"]["python"]

        print(self.parsers, self.on_dir, self.on_file)

        for elem in self.parsers.keys():
            item = QListWidgetItem(elem)
            item.setTextAlignment(Qt.AlignCenter)

            font = QFont('Inter')
            font.setKerning(True)

            item.setFont(font)

            item.setIcon(self.default_icon)

            self.listWidget.addItem(item)

        for elem in self.on_file.keys():
            item = QListWidgetItem(elem)
            item.setTextAlignment(Qt.AlignCenter)

            font = QFont('Inter')
            font.setKerning(True)

            item.setFont(font)

            item.setIcon(self.default_icon)

            self.listWidget_2.addItem(item)

        for elem in self.on_dir.keys():
            item = QListWidgetItem(elem)
            item.setTextAlignment(Qt.AlignCenter)

            font = QFont('Inter')
            font.setKerning(True)

            item.setFont(font)

            item.setIcon(self.default_icon)

            self.listWidget_3.addItem(item)

    def tool_bar_clicked(self, item: QListWidgetItem):
        title = item.text()
        print(f"* clicked - {title}")
        if title == "Settings":
            self.settings_clicked()
        if title == "Update":
            self.update_clicked()

    def update_clicked(self):
        print("* clicked - update, called function")

    def settings_clicked(self):
        print("* clicked - settings, called function")
        self.logsWindow.refresh()
        self.logsWindow.show()

    def clicked_on_dir(self, item: QListWidgetItem):
        title = item.text()
        item.setIcon(self.loading_icon)
        print("* clicked - on_dir", title)
        self.start_on_dir(item)

    def clicked_on_parser(self, item):
        title = item.text()
        item.setIcon(self.loading_icon)
        print("* clicked - on_parser", title)
        self.start_parser(item)

    def clicked_on_file(self, item):
        title = item.text()
        item.setIcon(self.loading_icon)
        print("* clicked - on_file", title)
        self.start_on_file(item)

    def start_on_dir(self, item):
        name = item.text()
        print("* started - on_dir", name)
        exec_path = self.on_dir[name]

    def start_on_file(self, item):
        name = item.text()
        print("* started - on_file", name)
        exec_path = self.on_file[name]

        dial = QFileDialog.getOpenFileName(None, "Choose file")
        print(dial)
        exec_path = f"{self.python} {exec_path} \"{dial[0]}\""
        working_dir = os.path.dirname(dial[0])

        task = Task()
        self.tasks.append(task)

        print(f"* execute:[{exec_path}] working in[{working_dir}]")

        process = QProcess(self)
        task.process = process
        task.owner = item

        process.setWorkingDirectory(working_dir)
        process.setObjectName(name)
        process.errorOccurred.connect(lambda: self.end_process(task, True))
        process.finished.connect(lambda: self.end_process(task))
        process.readyRead.connect(lambda: self.readout(process))

        process.readyReadStandardError.connect(lambda: self.readerror(process))

        process.start(exec_path)

    def start_parser(self, item):
        name = item.text()
        exec_path = self.parsers[name]
        working_dir = SEPARATOR.join(exec_path.split(SEPARATOR)[:-1])
        lang = exec_path.split(".")[-1]
        if lang == "py":
            exec_path = self.python + " \"" + exec_path + "\""
        process_name = translate(name)
        task = Task()
        print(f"* started - on_parser | name=[{name}], path=[{exec_path}], dir=[{working_dir}]")
        self.tasks.append(task)

        process = QProcess(self)
        task.process = process
        task.owner = item

        process.setWorkingDirectory(working_dir)
        process.setObjectName(process_name)
        process.errorOccurred.connect(lambda: self.end_process(task, is_error=True))
        process.finished.connect(lambda: self.end_process(task))
        process.readyRead.connect(lambda: self.readout(process))

        process.readyReadStandardError.connect(lambda: self.readerror(process))

        process.start(exec_path)

    def end_process(self, task, is_error=False):
        process = task.process
        print("is_error:", is_error)
        logname = translate(process.objectName().lower().rstrip())
        logger.write(logname, process.readAll())
        if process.state() == 0 and not is_error:
            task.owner.setIcon(self.done_icon)
            print(f"* DONE !!! {process.objectName()}")
            return
        else:
            task.owner.setIcon(self.error_icon)
            filepath = f'logs{SEPARATOR}{logname}_logs.log'
            self.logsWindow.appendLog(logname, filepath)
            print(f"* ERROR!!! error[{process.errorString()}]")

    def readout(self, process):
        name = process.objectName()
        logname = translate(name.lower().replace('\n', ''))
        info = process.readAll()
        if not info:
            return
        print(name, info)
        logger.write(logname, info)

    def readerror(self, process):
        name = process.objectName()
        logname = translate(name.lower().replace('\n', ''))

        err = process.readAllStandardError()
        print(f"called readerror name[{name}], err[{err}]")
        logger.write(logname, err)
