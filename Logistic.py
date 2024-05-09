from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWidgets import QMessageBox
from PollVoteGUI import Ui_MainPage
from PollAdmin import Ui_Form


class MainPage(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainPage()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.openPollAdmin)
        self.ui.pushButton_2.clicked.connect(self.saveOptions)
        self.uiPollAdmin = None
        self.VoteReg = {}

    def openPollAdmin(self):                            #Functions as the "Admin" button on the main page, opens PollAdmin panel
        self.uiPollAdmin = QtWidgets.QMainWindow()
        self.uiPollAdminWidget = Ui_Form()
        self.uiPollAdminWidget.setupUi(self.uiPollAdmin)
        self.uiPollAdmin.show()

        if self.VoteReg:
            self.updateTable(self.uiPollAdminWidget, self.VoteReg)



    def saveOptionsTable(self):                         #Takes the inputs from the GUI a puts them into the VoteReg Dictionary
        SelectedOptions = self.ui.comboBox.currentText()
        name = self.ui.lineEdit_4.text()
        idNumber = self.ui.lineEdit_6.text()

        selectedCandidate = ""
        if self.ui.radioButton.isChecked():
            selectedCandidate = self.ui.radioButton.text()
        elif self.ui.radioButton_2.isChecked():
            selectedCandidate = self.ui.radioButton_2.text()
        elif self.ui.radioButton_3.isChecked():
            selectedCandidate = self.ui.radioButton_3.text()
        elif self.ui.radioButton_4.isChecked():
            selectedCandidate = self.ui.radioButton_4.text()

        return  {
                "County": SelectedOptions,
                "Name": name,
                "ID": idNumber,
                "Candidate": selectedCandidate
        }

    def saveOptions(self):
        newEntry = self.saveOptionsTable()
        idNumber = newEntry["ID"]  # Extract ID from the new entry

        if idNumber in self.VoteReg:
            QMessageBox.critical(self, "ID Repeat", "ID Has Already Voted!")
        else:
            self.VoteReg[idNumber] = {
                    "Candidate": newEntry["Candidate"],
                    "Name": newEntry["Name"],
                    "County": newEntry["County"]
                }
            if self.uiPollAdmin is not None:
                self.updateTable(self.uiPollAdminWidget, self.VoteReg)



    def updateTable(self, uiPollAdmin, dataDict):       #Updates the table displayed in PollAdmin panel
        tableWidget = uiPollAdmin.tableWidget
        keyOrder = ["ID", "Name", "County", "Candidate"]
        tableWidget.setColumnCount(len(keyOrder))
        tableWidget.setRowCount(len(dataDict)+1)  


        for col, key in enumerate(keyOrder):
            headerItem = QtWidgets.QTableWidgetItem(key)
            tableWidget.setItem(0, col, headerItem)


        row = 1
        for idNumber, data in dataDict.items():
            tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(str(idNumber)))
            for col, key in enumerate(keyOrder[1:], start=1):
                if key in data:
                    value = data[key]
                    valueItem = QtWidgets.QTableWidgetItem(str(value))
                    tableWidget.setItem(row, col, valueItem)
            row += 1




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainpage = MainPage()
    mainpage.show()
    sys.exit(app.exec())