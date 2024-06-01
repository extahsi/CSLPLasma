
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QPushButton, QWidget, QLineEdit, QHBoxLayout, QDialog, QFormLayout, QDialogButtonBox
import requests
from scraper import login_and_get_points

class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Login')
        
        self.username = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        
        layout = QFormLayout()
        layout.addRow('Username:', self.username)
        layout.addRow('Password:', self.password)
        
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        
        layout.addWidget(self.buttons)
        self.setLayout(layout)
    
    def get_credentials(self):
        return self.username.text(), self.password.text()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.set_dark_mode()

    def init_ui(self):
        self.setWindowTitle('Points Balance Manager')

        self.label = QLabel('Current Points Balance: ')
        self.balance_label = QLabel('Fetching...')

        self.update_label = QLabel('Update Points Balance:')
        self.points_input = QLineEdit()

        self.update_button = QPushButton('Update Balance')
        self.update_button.clicked.connect(self.update_balance)

        self.refresh_button = QPushButton('Refresh Balance')
        self.refresh_button.clicked.connect(self.fetch_balance)

        self.login_button = QPushButton('Login')
        self.login_button.clicked.connect(self.login)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.balance_label)

        refresh_layout = QHBoxLayout()
        refresh_layout.addWidget(self.update_label)
        refresh_layout.addWidget(self.points_input)
        refresh_layout.addWidget(self.update_button)
        refresh_layout.addWidget(self.refresh_button)
        refresh_layout.addWidget(self.login_button)

        layout.addLayout(refresh_layout)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def set_dark_mode(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #2e2e2e;
                color: #ffffff;
            }
            QPushButton {
                background-color: #5e5e5e;
                color: #ffffff;
            }
            QLineEdit {
                background-color: #4e4e4e;
                color: #ffffff;
            }
        """)

    def fetch_balance(self):
        try:
            response = requests.get('http://127.0.0.1:5000/get_points')
            if response.status_code == 200:
                balance = response.json().get('points_balance')
                self.balance_label.setText(str(balance))
            else:
                self.balance_label.setText('Error fetching balance')
        except Exception as e:
            self.balance_label.setText(f'Error: {str(e)}')

    def update_balance(self):
        try:
            new_points = int(self.points_input.text())
            response = requests.post('http://127.0.0.1:5000/update_points', json={'new_points': new_points})
            if response.status_code == 200:
                self.fetch_balance()
            else:
                self.balance_label.setText('Error updating balance')
        except Exception as e:
            self.balance_label.setText(f'Error: {str(e)}')

    def login(self):
        dialog = LoginDialog()
        if dialog.exec_():
            username, password = dialog.get_credentials()
            try:
                points_balance = login_and_get_points(username, password)
                self.balance_label.setText(points_balance)
            except Exception as e:
                self.balance_label.setText(f'Error: {str(e)}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
