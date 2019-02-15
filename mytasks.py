#######################
### MyTasks - v1    ###
### by schiller83   ###
#######################

from PyQt5 import QtCore, QtGui, QtWidgets
import csv
import os

class Ui_Dialog(QtWidgets.QMainWindow):

    def __init__(self, fn=None,parent=None):
            super(Ui_Dialog, self).__init__()
            flags=QtCore.Qt.WindowMinimizeButtonHint|QtCore.Qt.WindowCloseButtonHint
            Dialog.setWindowFlags(flags)

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(486, 371)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(10, 6, 100, 20))
        self.label_message = QtWidgets.QLabel(Dialog)
        self.label_message.setGeometry(QtCore.QRect(120, 6, 150, 20))

        font = QtGui.QFont()
        font.setFamily("Lato")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.Button_Start = QtWidgets.QPushButton(Dialog)
        self.Button_Start.setGeometry(QtCore.QRect(10, 330, 89, 25))
        self.Button_Start.setObjectName("Button_Start")
        self.Button_Stop = QtWidgets.QPushButton(Dialog)
        self.Button_Stop.setGeometry(QtCore.QRect(110, 330, 89, 25))
        self.Button_Stop.setObjectName("Button_Stop")
        self.Button_Stop.setVisible(False)
        self.Button_Reset = QtWidgets.QPushButton(Dialog)
        self.Button_Reset.setGeometry(QtCore.QRect(210, 330, 89, 25))
        self.Button_Reset.setObjectName("Button_Reset")
        self.Button_Add = QtWidgets.QPushButton(Dialog)
        self.Button_Add.setGeometry(QtCore.QRect(310, 330, 25, 25))
        self.Button_Add.setObjectName("Button_Add")
        self.Button_Remove = QtWidgets.QPushButton(Dialog)
        self.Button_Remove.setGeometry(QtCore.QRect(346, 330, 25, 25))
        self.Button_Remove.setObjectName("Button_Remove")
        self.Button_Speichern = QtWidgets.QPushButton(Dialog)
        self.Button_Speichern.setGeometry(QtCore.QRect(382, 330, 89, 25))
        self.Button_Speichern.setObjectName("Button_Speichern")
        self.tableWidget = QtWidgets.QTableWidget(Dialog)
        self.tableWidget.setGeometry(QtCore.QRect(12, 40, 461, 281))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnWidth(0,300)
        self.lcdNumber = QtWidgets.QLCDNumber(Dialog)
        self.lcdNumber.setGeometry(QtCore.QRect(390, 6, 71, 23))
        self.lcdNumber.setObjectName("lcdNumber")
        self.lcdNumber.setDigitCount(8)
        self.lcdNumber.setStyleSheet("""QLCDNumber {background-color: green;color: white; }""")

        dirname = os.getcwd()
        self.csvfilename = os.path.join(dirname, 'tasks.csv')

        tab_row = 0

        with open(self.csvfilename) as csvDataFile:
            csvReader = csv.reader(csvDataFile, delimiter=';')
            for row in csvReader:
                self.tableWidget.insertRow(tab_row)
                self.tableWidget.setItem(tab_row, 0, QtWidgets.QTableWidgetItem(row[0]))
                self.tableWidget.setItem(tab_row, 1, QtWidgets.QTableWidgetItem(row[1]))
                tab_row+=1
        
        self.rownum = self.tableWidget.rowCount()

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.clock)

        self.tableWidget.selectRow(0)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        self.time_set = 0.0
        self.Button_Start.clicked.connect(self.start_clock)
        self.Button_Stop.clicked.connect(self.stop_clock)
        self.Button_Reset.clicked.connect(self.reset_table)
        self.Button_Speichern.clicked.connect(self.save_table)
        self.Button_Add.clicked.connect(self.add_row)
        self.Button_Remove.clicked.connect(self.remove_row)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "MyTasks"))
        self.Button_Start.setText(_translate("Dialog", "Start Task"))
        self.Button_Stop.setText(_translate("Dialog", "Stop Task"))
        self.Button_Reset.setText(_translate("Dialog", "Reset"))
        self.Button_Speichern.setText(_translate("Dialog", "Speichern"))
        self.Button_Add.setText(_translate("Dialog", "+"))
        self.Button_Remove.setText(_translate("Dialog", "-"))

    def start_clock(self):
        self.timer.start(360000)
        self.Button_Start.setVisible(False)
        self.Button_Stop.setVisible(True)
        self.curr_row = self.tableWidget.currentRow()
        self.time_item = self.tableWidget.item(self.curr_row, 1).text()
        self.time_set = float(self.time_item)
        self.lcdNumber.display(self.time_set)

    def clock(self):
        self.time_set += 0.1
        text = self.time_set
        self.lcdNumber.display("{:2.1f}".format(text))
        
    def stop_clock(self):
        self.timer.stop()
        self.Button_Start.setVisible(True)
        self.Button_Stop.setVisible(False)
        self.tableWidget.setItem(self.curr_row, 1, QtWidgets.QTableWidgetItem(str("{:2.1f}".format(self.time_set))))

    def reset_table(self):
        for i in range(0,self.rownum):
            self.tableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem(str(0.0)))

    def add_row(self):
        self.tableWidget.insertRow(self.rownum)
        self.tableWidget.setItem(self.rownum, 0, QtWidgets.QTableWidgetItem('Task Neu'))
        self.tableWidget.setItem(self.rownum, 1, QtWidgets.QTableWidgetItem('0.0'))       
        self.rownum = self.tableWidget.rowCount()

    def remove_row(self):
        self.curr_row = self.tableWidget.currentRow()
        self.tableWidget.removeRow(self.curr_row)
        self.rownum = self.tableWidget.rowCount()

    def save_table(self):
        try:
            with open(self.csvfilename, mode='w', newline='') as csvDataFile:
                csv_writer = csv.writer(csvDataFile, delimiter=';')
                for i in range(0,self.rownum):
                    csv_writer.writerow([self.tableWidget.item(i, 0).text(),self.tableWidget.item(i, 1).text()])
        except:
            self.label_message.setText(_translate("Dialog", "Speichern nicht erfolgreich!"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
