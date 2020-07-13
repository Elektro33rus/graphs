from interface import Ui_Dialog as myinterface
from MainFunctions import StartProgramThread
from PyQt5 import QtCore, QtWidgets
import sys
from PyQt5.Qt import QDialog
from PyQt5.QtGui import QIcon


class InfoDialog(QDialog):
    def __init__(self, intactness, deletedNodes, errors, success, parent=None):
        super(InfoDialog, self).__init__(parent)
        self.setWindowTitle('Results')
        self.setWindowIcon(QIcon('main.png'))
        self.intaktnostLabel = QtWidgets.QLabel(self)
        self.intaktnostLabel.setGeometry(QtCore.QRect(10, 10, 180, 25))
        self.intaktnostLabel.setObjectName("intaktnostLabel")
        self.intaktnostLabel.setText('Интактность: ' + str(intactness) + '%')

        self.deletedLabel = QtWidgets.QLabel(self)
        self.deletedLabel.setGeometry(QtCore.QRect(10, 30, 180, 25))
        self.deletedLabel.setObjectName("deletedLabel")
        self.deletedLabel.setText('Удаленных вершин: ' + str(deletedNodes) + '%')

        self.errorsLabel = QtWidgets.QLabel(self)
        self.errorsLabel.setGeometry(QtCore.QRect(10, 50, 180, 25))
        self.errorsLabel.setObjectName("errorsLabel")
        self.errorsLabel.setText('Успешность: ' + str(success) + '%')

        self.errorsLabel = QtWidgets.QLabel(self)
        self.errorsLabel.setGeometry(QtCore.QRect(10, 70, 180, 25))
        self.errorsLabel.setObjectName("errorsLabel")
        self.errorsLabel.setText('Ошибки: ' + str(errors) + '%')
        self.setFixedSize(170, 100)



class MainForm(QtWidgets.QMainWindow, myinterface):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.startButton.clicked.connect(self.StartProgram)
        self.startThread = None
        self.errors = 0
        self.intaktnost = 0
        self.deleted = 0
        self.success = 0

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
            self.startThread.intactness.connect(self.refreshIntaktnost)
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
        self.errors = round(val, 2)

    def refreshIntaktnost(self, val):
        self.intaktnost = round(val, 2)

    def refreshDeleted(self, val):
        self.deleted = round(val, 2)
        self.success = round(100.0 - ((self.intaktnost * self.deleted) / 100), 2)

    def addnewDialog(self):
        w = InfoDialog(self.intaktnost, self.deleted, self.errors, self.success, self)
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
