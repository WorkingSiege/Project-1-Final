from Logistic import *
from PyQt6.QtWidgets import QApplication


def main():
    app = QApplication([])
    
    VoteSystem = MainPage()

    VoteSystem.show()

    app.exec()

if __name__ == "__main__":
    main()