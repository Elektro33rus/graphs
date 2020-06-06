# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Graph program")
        Dialog.resize(543, 371)
        self.comboBoxGraphType = QtWidgets.QComboBox(Dialog)
        self.comboBoxGraphType.setGeometry(QtCore.QRect(19, 60, 171, 21))
        self.comboBoxGraphType.setObjectName("comboBoxGraphType")
        self.comboBoxGraphType.addItem("")
        self.comboBoxGraphType.addItem("")
        self.comboBoxGraphType.addItem("")
        self.Label1 = QtWidgets.QLabel(Dialog)
        self.Label1.setGeometry(QtCore.QRect(19, 20, 181, 16))
        self.Label1.setObjectName("Label1")
        self.label2 = QtWidgets.QLabel(Dialog)
        self.label2.setGeometry(QtCore.QRect(19, 110, 81, 16))
        self.label2.setObjectName("label2")
        self.label3 = QtWidgets.QLabel(Dialog)
        self.label3.setGeometry(QtCore.QRect(19, 150, 81, 16))
        self.label3.setObjectName("label3")
        self.spinBoxNodes = QtWidgets.QSpinBox(Dialog)
        self.spinBoxNodes.setGeometry(QtCore.QRect(130, 110, 61, 22))
        self.spinBoxNodes.setMaximum(1000)
        self.spinBoxNodes.setObjectName("spinBoxNodes")
        self.spinBoxConnetions = QtWidgets.QSpinBox(Dialog)
        self.spinBoxConnetions.setGeometry(QtCore.QRect(130, 150, 61, 22))
        self.spinBoxConnetions.setObjectName("spinBoxConnetions")
        self.label4 = QtWidgets.QLabel(Dialog)
        self.label4.setGeometry(QtCore.QRect(20, 190, 81, 16))
        self.label4.setObjectName("label4")
        self.spinBoxSeed = QtWidgets.QSpinBox(Dialog)
        self.spinBoxSeed.setGeometry(QtCore.QRect(130, 190, 61, 22))
        self.spinBoxSeed.setObjectName("spinBoxSeed")
        self.spinBoxSeed.setDisabled(True)
        self.label5 = QtWidgets.QLabel(Dialog)
        self.label5.setGeometry(QtCore.QRect(20, 230, 171, 16))
        self.label5.setObjectName("label5")
        self.doubleSpinBoxPeremontirovanie = QtWidgets.QDoubleSpinBox(Dialog)
        self.doubleSpinBoxPeremontirovanie.setGeometry(QtCore.QRect(210, 230, 62, 22))
        self.doubleSpinBoxPeremontirovanie.setDecimals(5)
        self.doubleSpinBoxPeremontirovanie.setMaximum(1.0)
        self.doubleSpinBoxPeremontirovanie.setSingleStep(0.01)
        self.doubleSpinBoxPeremontirovanie.setObjectName("doubleSpinBoxPeremontirovanie")
        self.pushButtonStart = QtWidgets.QPushButton(Dialog)
        self.pushButtonStart.setGeometry(QtCore.QRect(340, 160, 75, 23))
        self.pushButtonStart.setObjectName("pushButtonStart")
        self.label6 = QtWidgets.QLabel(Dialog)
        self.label6.setGeometry(QtCore.QRect(300, 20, 121, 16))
        self.label6.setObjectName("label6")
        self.comboBoxAttackType = QtWidgets.QComboBox(Dialog)
        self.comboBoxAttackType.setGeometry(QtCore.QRect(300, 60, 171, 21))
        self.comboBoxAttackType.setObjectName("comboBoxAttackType")
        self.comboBoxAttackType.addItem("")
        self.comboBoxAttackType.addItem("")
        self.comboBoxAttackType.addItem("")
        self.comboBoxAttackType.addItem("")
        self.comboBoxAttackType.addItem("")
        self.checkBoxSeed = QtWidgets.QCheckBox(Dialog)
        self.checkBoxSeed.setGeometry(QtCore.QRect(100, 190, 16, 17))
        self.checkBoxSeed.setText("")
        self.checkBoxSeed.setObjectName("checkBoxSeed")
        self.checkBoxSeed.toggled.connect(self.onCheckBoxSeed_Trigger)
        self.checkBoxPeremontirovanie = QtWidgets.QCheckBox(Dialog)
        self.checkBoxPeremontirovanie.setGeometry(QtCore.QRect(190, 230, 16, 17))
        self.checkBoxPeremontirovanie.setText("")
        self.checkBoxPeremontirovanie.setObjectName("checkBoxPeremontirovanie")
        self.checkBoxResult = QtWidgets.QCheckBox(Dialog)
        self.checkBoxResult.setGeometry(QtCore.QRect(450, 110, 16, 17))
        self.checkBoxResult.setText("")
        self.checkBoxResult.setObjectName("checkBoxResult")
        self.label7 = QtWidgets.QLabel(Dialog)
        self.label7.setGeometry(QtCore.QRect(300, 110, 131, 16))
        self.label7.setObjectName("label7")
        self.listView = QtWidgets.QListView(Dialog)
        self.listView.setGeometry(QtCore.QRect(140, 270, 241, 71))
        self.listView.setObjectName("listView")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Graph program", "Graph program"))
        self.comboBoxGraphType.setItemText(0, _translate("Dialog", "Random"))
        self.comboBoxGraphType.setItemText(1, _translate("Dialog", "Small world"))
        self.comboBoxGraphType.setItemText(2, _translate("Dialog", "Barabasi_albert"))
        self.Label1.setText(_translate("Dialog", "Выберите метод генерации графа"))
        self.label2.setText(_translate("Dialog", "Число вершин"))
        self.label3.setText(_translate("Dialog", "Связность, %"))
        self.label4.setText(_translate("Dialog", "Seed (optional)"))
        self.label5.setText(_translate("Dialog", "Вероятность перемонтирования"))
        self.pushButtonStart.setText(_translate("Dialog", "Start"))
        self.label6.setText(_translate("Dialog", "Выберите метод атаки"))
        self.comboBoxAttackType.setItemText(0, _translate("Dialog", "Random"))
        self.comboBoxAttackType.setItemText(1, _translate("Dialog", "Clustering coefficient"))
        self.comboBoxAttackType.setItemText(2, _translate("Dialog", "Eigenvector centrality"))
        self.comboBoxAttackType.setItemText(3, _translate("Dialog", "By degree - either starting with the lowest"))
        self.comboBoxAttackType.setItemText(4, _translate("Dialog", "By degree - either starting with the highest"))
        self.label7.setText(_translate("Dialog", "Сохранить результаты?"))

    def onCheckBoxSeed_Trigger(self):
        if self.checkBoxSeed.isChecked():
            self.spinBoxSeed.setDisabled(False)
        else:
            self.spinBoxSeed.setDisabled(True)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
