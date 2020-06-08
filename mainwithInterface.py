from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QDialogButtonBox
from interface import Ui_Dialog as myinterface
from mainTest3 import StartProgramThread
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PyQt5.QtCore import QThread, pyqtSignal
import os
import time
from time import gmtime, strftime
import sys
from PyQt5.Qt import QVBoxLayout, QLabel, QDialog, QDialogButtonBox, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QApplication


class InfoDialog(QDialog):
    def __init__(self, интактность, удаленныевершины, errors, success, parent=None):
        super(InfoDialog, self).__init__(parent)
        self.intaktnostLabel = QtWidgets.QLabel(self)
        self.intaktnostLabel.setGeometry(QtCore.QRect(10, 10, 181, 21))
        self.intaktnostLabel.setObjectName("intaktnostLabel")
        self.intaktnostLabel.setText('Интактность: ' + str(интактность) + '%')

        self.deletedLabel = QtWidgets.QLabel(self)
        self.deletedLabel.setGeometry(QtCore.QRect(10, 30, 181, 21))
        self.deletedLabel.setObjectName("deletedLabel")
        self.deletedLabel.setText('Удаленных вершин: ' + str(удаленныевершины) + '%')

        self.errorsLabel = QtWidgets.QLabel(self)
        self.errorsLabel.setGeometry(QtCore.QRect(10, 50, 181, 21))
        self.errorsLabel.setObjectName("errorsLabel")
        self.errorsLabel.setText('Успешность: ' + str(success) + '%')

        self.errorsLabel = QtWidgets.QLabel(self)
        self.errorsLabel.setGeometry(QtCore.QRect(10, 70, 181, 21))
        self.errorsLabel.setObjectName("errorsLabel")
        self.errorsLabel.setText('Ошибки: ' + str(errors) + '%')




class MainForm(QtWidgets.QMainWindow, myinterface):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.startButton.clicked.connect(self.StartProgram)
        self.startThread = None
        self.errors = 0
        self.intaktnost = 0
        self.deleted = 0
        self.uspeshnost = 0

    def StartProgram(self):
        if self.startButton.text() == 'Start':
            self.startThread = StartProgramThread(int(self.retryBox.text()),
                                            self.generateComboBox.currentText(),
                                            self.attackComboBox.currentText(),
                                            int(self.sizeBox.text()),
                                            int(self.rewritingBox.text()),
                                            None)
            self.startThread.change_progress_bar.connect(self.setProgressVal)
            self.startThread.change_start_button.connect(self.setStartButtonVal)
            self.startThread.add_new_dialog.connect(self.addnewDialog)
            self.startThread.errors.connect(self.refreshErrors)
            self.startThread.intaktnost.connect(self.refreshIntaktnost)
            self.startThread.deleted.connect(self.refreshDeleted)
            self.startThread.start()
            self.startButton.setText('Stop')
            self.progressBar.setDisabled(False)
        else:
            self.startButton.setText('Start')
            self.progressBar.setDisabled(True)
            self.progressBar.setValue(0)
            self.startThread.killThread = True

    def refreshErrors(self, val):
        self.errors = val

    def refreshIntaktnost(self, val):
        self.intaktnost = val

    def refreshDeleted(self, val):
        self.deleted = val
        self.uspeshnost = 100.0 - ((self.intaktnost * self.deleted) / float(self.sizeBox.text()))

    def addnewDialog(self):
        w = InfoDialog(self.intaktnost, self.deleted, self.errors, self.uspeshnost, self)
        w.exec_()

    def setProgressVal(self, val):
        self.progressBar.setValue(val)

    def setStartButtonVal(self, val):
        self.startButton.setText(val)
        if (val == 'Waiting'):
            self.startButton.setDisabled(True)
        else:
            self.startButton.setDisabled(False)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainForm()
    window.show()
    app.exec_()
