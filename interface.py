# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'interface.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(333, 300)
        self.startButton = QtWidgets.QPushButton(Dialog)
        self.startButton.setGeometry(QtCore.QRect(120, 250, 91, 23))
        self.startButton.setObjectName("startButton")
        self.sizeBox = QtWidgets.QSpinBox(Dialog)
        self.sizeBox.setGeometry(QtCore.QRect(210, 90, 111, 22))
        self.sizeBox.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.sizeBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.sizeBox.setAutoFillBackground(False)
        self.sizeBox.setMaximum(10000)
        self.sizeBox.setProperty("value", 100)
        self.sizeBox.setObjectName("sizeBox")
        self.seedBox = QtWidgets.QSpinBox(Dialog)
        self.seedBox.setEnabled(False)
        self.seedBox.setGeometry(QtCore.QRect(210, 180, 111, 22))
        self.seedBox.setObjectName("seedBox")
        self.retryBox = QtWidgets.QSpinBox(Dialog)
        self.retryBox.setGeometry(QtCore.QRect(210, 150, 111, 22))
        self.retryBox.setMaximum(10000)
        self.retryBox.setProperty("value", 1000)
        self.retryBox.setObjectName("retryBox")
        self.rewritingBox = QtWidgets.QSpinBox(Dialog)
        self.rewritingBox.setGeometry(QtCore.QRect(210, 120, 111, 22))
        self.rewritingBox.setMinimum(1)
        self.rewritingBox.setProperty("value", 5)
        self.rewritingBox.setObjectName("rewritingBox")
        self.progressBar = QtWidgets.QProgressBar(Dialog)
        self.progressBar.setEnabled(False)
        self.progressBar.setGeometry(QtCore.QRect(17, 220, 301, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.generateLabel = QtWidgets.QLabel(Dialog)
        self.generateLabel.setGeometry(QtCore.QRect(10, 30, 181, 21))
        self.generateLabel.setObjectName("generateLabel")
        self.attackLabel = QtWidgets.QLabel(Dialog)
        self.attackLabel.setGeometry(QtCore.QRect(10, 60, 171, 16))
        self.attackLabel.setObjectName("attackLabel")
        self.vertexLabel = QtWidgets.QLabel(Dialog)
        self.vertexLabel.setGeometry(QtCore.QRect(10, 90, 191, 16))
        self.vertexLabel.setObjectName("vertexLabel")
        self.generateComboBox = QtWidgets.QComboBox(Dialog)
        self.generateComboBox.setGeometry(QtCore.QRect(210, 30, 111, 22))
        self.generateComboBox.setObjectName("generateComboBox")
        self.generateComboBox.addItem("")
        self.generateComboBox.addItem("")
        self.generateComboBox.addItem("")
        self.attackComboBox = QtWidgets.QComboBox(Dialog)
        self.attackComboBox.setGeometry(QtCore.QRect(210, 60, 111, 22))
        self.attackComboBox.setObjectName("attackComboBox")
        self.attackComboBox.addItem("")
        self.attackComboBox.addItem("")
        self.attackComboBox.addItem("")
        self.attackComboBox.addItem("")
        self.attackComboBox.addItem("")
        self.nodesLabel = QtWidgets.QLabel(Dialog)
        self.nodesLabel.setGeometry(QtCore.QRect(10, 120, 201, 16))
        self.nodesLabel.setObjectName("nodesLabel")
        self.seedCheckBox = QtWidgets.QCheckBox(Dialog)
        self.seedCheckBox.setGeometry(QtCore.QRect(190, 180, 16, 21))
        self.seedCheckBox.setText("")
        self.seedCheckBox.setObjectName("seedCheckBox")
        self.seedLabel = QtWidgets.QLabel(Dialog)
        self.seedLabel.setGeometry(QtCore.QRect(10, 180, 171, 16))
        self.seedLabel.setObjectName("seedLabel")
        self.retryLabel = QtWidgets.QLabel(Dialog)
        self.retryLabel.setGeometry(QtCore.QRect(10, 150, 191, 16))
        self.retryLabel.setObjectName("retryLabel")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.startButton.setText(_translate("Dialog", "Start"))
        self.generateLabel.setText(_translate("Dialog", "Метод генерации графа"))
        self.attackLabel.setText(_translate("Dialog", "Метод атаки на граф"))
        self.vertexLabel.setText(_translate("Dialog", "Количество вершин у графа"))
        self.generateComboBox.setItemText(0, _translate("Dialog", "Random"))
        self.generateComboBox.setItemText(1, _translate("Dialog", "Barabasi"))
        self.generateComboBox.setItemText(2, _translate("Dialog", "Small world"))
        self.attackComboBox.setItemText(0, _translate("Dialog", "Random"))
        self.attackComboBox.setItemText(1, _translate("Dialog", "Max"))
        self.attackComboBox.setItemText(2, _translate("Dialog", "Min"))
        self.attackComboBox.setItemText(3, _translate("Dialog", "Centrality"))
        self.attackComboBox.setItemText(4, _translate("Dialog", "Centrality with recalculation"))
        self.nodesLabel.setText(_translate("Dialog", "Cреднее количество узлов в вершинах"))
        self.seedLabel.setText(_translate("Dialog", "Использовать seed?"))
        self.retryLabel.setText(_translate("Dialog", "Введите количество повторов"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
