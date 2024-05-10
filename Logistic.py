from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWidgets import QMessageBox
from PollVoteGUI import Ui_MainPage
from PollAdmin import Ui_Form


class MainPage(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainPage()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.PollAdmin)
        self.ui.pushButton_2.clicked.connect(self.saveOptions)
        self.uiPollAdmin = None
        self.VoteReg = {}

    def PollAdmin(self):                            #Functions as the "Admin" button on the main page, opens PollAdmin panel
        self.uiPollAdmin = QtWidgets.QMainWindow()
        self.uiPollAdminWidget = Ui_Form()
        self.uiPollAdminWidget.setupUi(self.uiPollAdmin)
        self.uiPollAdmin.show()

        if self.VoteReg:
            self.updateTable(self.uiPollAdminWidget, self.VoteReg)
            self.showPercentage(self.uiPollAdminWidget)



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
                self.showPercentage(self.uiPollAdminWidget)


    def updateTable(self, uiPollAdmin, dataDict):       #Updates the table displayed in PollAdmin panel
        Database = uiPollAdmin.tableWidget
        keyOrder = ["ID", "Name", "County", "Candidate"]
        Database.setColumnCount(len(keyOrder))
        Database.setRowCount(len(dataDict)+1)  


        for col, key in enumerate(keyOrder):
            headerItem = QtWidgets.QTableWidgetItem(key)
            Database.setItem(0, col, headerItem)


        row = 1
        for idNumber, data in dataDict.items():
            Database.setItem(row, 0, QtWidgets.QTableWidgetItem(str(idNumber)))
            for col, key in enumerate(keyOrder[1:], start=1):
                if key in data:
                    value = data[key]
                    valueItem = QtWidgets.QTableWidgetItem(str(value))
                    Database.setItem(row, col, valueItem)
            row += 1

    def calculatePercentages(self):
        totalVotes = len(self.VoteReg)
        if totalVotes == 0:
            return {}
        
        voteCounts = {}
        for data in self.VoteReg.values():
            candidate = data["Candidate"]
            voteCounts[candidate] = voteCounts.get(candidate, 0 ) + 1

        percentages = {}
        for candidate, votes in voteCounts.items():
            percentage = (votes/ totalVotes) * 100
            percentages[candidate] = percentage
        return percentages

    def showPercentage(self, uiPollAdmin):
        percentages = self.calculatePercentages()

        PercentTable = uiPollAdmin.tableWidget_2
        PercentTable.setColumnCount(len(percentages))
        PercentTable.setRowCount(2)

        for col, candidate in enumerate(percentages.keys()):
            PercentTable.setItem(0, col, QtWidgets.QTableWidgetItem(candidate)) 
            percentage = "{:.0f}%".format(percentages[candidate])
            PercentTable.setItem(1, col, QtWidgets.QTableWidgetItem(percentage))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainpage = MainPage()
    mainpage.show()
    sys.exit(app.exec())