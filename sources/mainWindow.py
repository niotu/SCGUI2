import sys

import json
from PyQt5.QtCore import Qt, QProcess, QSize
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QWidget, QMainWindow, QListWidgetItem, QFileDialog, QScrollBar

from const.CONSTANTS import *
from sources.MainWindowUI import Ui_MainWindow


class Task:
    pass


def translate(inp):
    res = ""
    for l in inp:
        res += ALFA[l]
    return res


class MainWindow(Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.default_icon = QIcon(COMMON_ICON_ROOT)
        self.loading_icon = QIcon(LOADING_ICON_ROOT)
        self.error_icon = QIcon(ERROR_ICON_ROOT)
        self.done_icon = QIcon(DONE_ICON_ROOT)
        self.tasks = []

        self.setupUi(self)

        styles = open(STYLES_ROOT, encoding='utf-8').read()

        self.setStyleSheet(styles)

        self.listWidget.itemClicked.connect(self.clicked_on_parser)

        self.listWidget.setSpacing(SPACING)
        # self.listWidget.
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
            font.setWeight(20)

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

    def clicked_on_dir(self, item: QListWidgetItem):
        title = item.text()
        item.setIcon(self.loading_icon)
        print("* clicked - on_dir", title)
        self.start_on_dir(title)

    def clicked_on_parser(self, item):
        title = item.text()
        item.setIcon(self.loading_icon)
        print("* clicked - on_parser", title)
        self.start_parser(title)

    def clicked_on_file(self, item):
        title = item.text()
        item.setIcon(self.loading_icon)
        print("* clicked - on_file", title)
        self.start_on_file(title)

    def start_on_file(self, name):
        print("* started - on_file", name)

    def start_on_dir(self, name):
        print("* started - on_dir", name)

    def start_parser(self, name):
        print("* started - on_parser", name)
        exec_path = self.parsers[name]
        working_dir = "/" + exec_path
        process_name = translate(name)
        task = Task()
        self.tasks.append(task)

        process = QProcess(self)
        task.process = process

        process.setWorkingDirectory(working_dir)
        process.setObjectName(process_name)
        process.errorOccurred.connect(lambda: self.end_process(process, is_error=True))
        process.finished.connect(lambda: self.end_process(process))

        process.start(exec_path)

    def end_process(self, process, is_error=False):
        print("is_error:", is_error)
