import sys
import logging
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('CSL Plasma Points Changer')
        self.setGeometry(100, 100, 600, 400)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        self.username_label = QLabel('Username:')
        self.username_input = QLineEdit()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)

        self.password_label = QLabel('Password:')
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)

        self.new_points_label = QLabel('New Points Balance:')
        self.new_points_input = QLineEdit()
        layout.addWidget(self.new_points_label)
        layout.addWidget(self.new_points_input)

        self.submit_button = QPushButton('Change Points Balance')
        self.submit_button.clicked.connect(self.change_points_balance)
        layout.addWidget(self.submit_button)

        central_widget.setLayout(layout)

    def change_points_balance(self):
        username = self.username_input.text()
        password = self.password_input.text()
        new_points_balance = self.new_points_input.text()

        if not all([username, password, new_points_balance]):
            QMessageBox.warning(self, 'Error', 'Please fill in all fields.')
            return

        try:
            new_points_balance = int(new_points_balance)
            response = requests.post('http://127.0.0.1:5000/update_points', json={
                'username': username,
                'password': password,
                'new_points_balance': new_points_balance
            })
            response_data = response.json()
            if 'error' in response_data:
                raise Exception(response_data['error'])
            updated_balance = response_data['new_balance']
            QMessageBox.information(self, 'Success', f'Points balance updated to: {updated_balance}')
        except ValueError:
            QMessageBox.warning(self, 'Error', 'Points balance must be a number.')
        except Exception as e:
            QMessageBox.critical(self, 'Error', str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
