import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QLineEdit
from scraper import login_and_get_points

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Points Scraper")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.layout = QVBoxLayout()

        self.username_label = QLabel('Username:')
        self.layout.addWidget(self.username_label)
        
        self.username_input = QLineEdit(self)
        self.layout.addWidget(self.username_input)

        self.password_label = QLabel('Password:')
        self.layout.addWidget(self.password_label)
        
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.password_input)

        self.points_label = QLabel('Points Balance:')
        self.layout.addWidget(self.points_label)
        
        self.refresh_button = QPushButton('Refresh', self)
        self.refresh_button.clicked.connect(self.refresh_points)
        self.layout.addWidget(self.refresh_button)
        
        self.central_widget.setLayout(self.layout)
        
    def refresh_points(self):
        username = self.username_input.text()
        password = self.password_input.text()
        try:
            points = login_and_get_points(username, password)
            self.points_label.setText(f'Points Balance: {points}')
        except Exception as e:
            self.points_label.setText(f'Error: {str(e)}')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
