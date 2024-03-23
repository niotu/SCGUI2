from os import walk
import sys
from argparse import ArgumentParser
from shutil import copy
from PySide6.QtWidgets import QFileDialog, QApplication
from const.CONSTANTS import SEPARATOR

p = ArgumentParser(prog="checker.py", description="program check for .error files")
p.add_argument("directory")
p.add_argument("curr")
directory = p.parse_args().directory
curr = p.parse_args().curr

dailApp = QApplication(sys.argv)

dial = QFileDialog.getExistingDirectory(None, "Choose dir", directory + curr)
print(dial)
dir = dial

files = list(walk(dir))[0][2]
print(files)

for file in files:
    print(dir + SEPARATOR + file, directory[:-1])
    copy(dir + SEPARATOR + file, directory[:-1])
