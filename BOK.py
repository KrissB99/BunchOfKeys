# External libraries
from PyQt5.QtWidgets import QApplication
import sys

# Internal libraries
from main import PasswordManager

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PasswordManager()   
    window.show()
    sys.exit(app.exec_())