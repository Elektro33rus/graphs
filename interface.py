# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
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
        self.progressBar.setGeometry(QtCore.QRect(17, 220, 301, 23))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(10, 30, 181, 21))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(10, 60, 171, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(10, 90, 191, 16))
        self.label_3.setObjectName("label_3")
        self.comboBox = QtWidgets.QComboBox(Dialog)
        self.comboBox.setGeometry(QtCore.QRect(210, 30, 111, 22))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox_2 = QtWidgets.QComboBox(Dialog)
        self.comboBox_2.setGeometry(QtCore.QRect(210, 60, 111, 22))
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(10, 120, 201, 16))
        self.label_4.setObjectName("label_4")
        self.checkBox = QtWidgets.QCheckBox(Dialog)
        self.checkBox.setGeometry(QtCore.QRect(190, 180, 16, 21))
        self.checkBox.setText("")
        self.checkBox.setObjectName("checkBox")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(10, 180, 171, 16))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(10, 150, 191, 16))
        self.label_6.setObjectName("label_6")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.startButton.setText(_translate("Dialog", "Start"))
        self.label.setText(_translate("Dialog", "Метод генерации графа"))
        self.label_2.setText(_translate("Dialog", "Метод атаки на граф"))
        self.label_3.setText(_translate("Dialog", "Количество вершин у графа"))
        self.comboBox.setItemText(0, _translate("Dialog", "Random"))
        self.comboBox.setItemText(1, _translate("Dialog", "Barabasi"))
        self.comboBox.setItemText(2, _translate("Dialog", "Small world"))
        self.comboBox_2.setItemText(0, _translate("Dialog", "Random"))
        self.comboBox_2.setItemText(1, _translate("Dialog", "Max"))
        self.comboBox_2.setItemText(2, _translate("Dialog", "Min"))
        self.comboBox_2.setItemText(3, _translate("Dialog", "Centrality"))
        self.comboBox_2.setItemText(4, _translate("Dialog", "Centrality ultra"))
        self.label_4.setText(_translate("Dialog", "Cреднее количество узлов в вершинах"))
        self.label_5.setText(_translate("Dialog", "Использовать seed?"))
        self.label_6.setText(_translate("Dialog", "Введите количество повторов"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
