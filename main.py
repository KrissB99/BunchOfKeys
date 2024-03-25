import sqlite3
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import  QMainWindow, QWidget, QVBoxLayout, \
                             QHBoxLayout, QPushButton, QMessageBox, \
                             QListWidget, QInputDialog, QStyleFactory

class PasswordManager(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        QApplication.setStyle(QStyleFactory.create('Fusion'))
        self.setWindowIcon(QtGui.QIcon('static/icon.png')) # Icon
        self.setWindowTitle("Password Manager") # Title
        self.setGeometry(100, 100, 400, 400) # Geometry

        # Database setup
        self.conn = sqlite3.connect('passwords.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS passwords (service TEXT, password TEXT, email TEXT, login TEXT)')

        self.initUI()

    def initUI(self):
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.password_list = QListWidget()
        self.layout.addWidget(self.password_list)

        # Buttons layout
        self.button_layout = QHBoxLayout()
        self.layout.addLayout(self.button_layout)
        self.central_widget.setLayout(self.layout)
        
        # Adding password
        self.add_button = QPushButton("Add Password")
        self.button_layout.addWidget(self.add_button)
        self.add_button.setStyleSheet("background-color: #4B4453; color: white;")
        self.add_button.clicked.connect(self.add_password)
        
        # Retriving password
        self.retrieve_button = QPushButton("Get Password")
        self.button_layout.addWidget(self.retrieve_button)
        self.retrieve_button.setStyleSheet("background-color: #296073; color: white;")
        self.retrieve_button.clicked.connect(self.retrieve_password)
        
        # Deleting password
        self.delete_button = QPushButton("Delete Password")
        self.button_layout.addWidget(self.delete_button)
        self.delete_button.setStyleSheet("background-color: #D73222; color: white;")
        self.delete_button.clicked.connect(self.delete_password)

        self.load_passwords()

    def load_passwords(self):
        self.password_list.clear()
        self.cursor.execute("SELECT service FROM passwords")
        services = [row[0] for row in self.cursor.fetchall()]
        self.password_list.addItems(services)

    def add_password(self):
        service, ok = QInputDialog.getText(self, "Add Password", "Service:")
        if service and ok:
            email, ok = QInputDialog.getText(self, "Add e-mail address", "E-mail:")
            if ok:
                login, ok = QInputDialog.getText(self, "Add login", "Login:")
                if (email or login) and ok:
                    password, ok = QInputDialog.getText(self, "Add Password", f"Password for {service}:")
                    if ok:
                        self.cursor.execute("INSERT INTO passwords VALUES (?, ?, ?, ?)", (service, email, login, password))
                        self.conn.commit()
                        self.load_passwords()
                        QMessageBox.information(self, "Success", f"Password for {service} has been added successfully.")

    def retrieve_password(self):
        current_item = self.password_list.currentItem()
        if current_item:
            service = current_item.text()
            self.cursor.execute("SELECT password FROM passwords WHERE service=?", (service,))
            password = self.cursor.fetchone()
            if password:
                password = password[0]
                clipboard = QApplication.clipboard()
                clipboard.setText(password)
                QMessageBox.information(self, "Password", f"Password for {service} copied to clipboard.")
            else:
                QMessageBox.warning(self, "Password not found", f"No password found for {service}")
    
    def delete_password(self):
        current_item = self.password_list.currentItem()
        if current_item:
            service = current_item.text()
            confirmation = QMessageBox.question(self, "Confirm deletion!" , 
                                                 f"Are you sure you want to delete the password for {service}?", 
                                                 QMessageBox.Yes | QMessageBox.No)
            if confirmation:
                self.cursor.execute("DELETE FROM passwords WHERE service=?", (service,))
                self.conn.commit()
                self.load_passwords()
                QMessageBox.information(self, "Success", f"Password for {service} has been deleted successfully.")