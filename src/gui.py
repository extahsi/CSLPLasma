import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QVBoxLayout, QWidget, QLabel, QLineEdit, QFormLayout
from PyQt5.QtGui import QPalette, QColor
from web_scraper import WebScraper
from database import Database

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Vulnerability Scraper and Points Manipulator")
        self.setGeometry(100, 100, 800, 600)
        self.set_dark_mode()  # Ensure this method is defined

        self.scraper = WebScraper()
        self.database = Database()

        self.initUI()

    def set_dark_mode(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
        palette.setColor(QPalette.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
        palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
        palette.setColor(QPalette.Text, QColor(255, 255, 255))
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
        palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
        palette.setColor(QPalette.Highlight, QColor(142, 45, 197).lighter())
        palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))
        self.setPalette(palette)

    def initUI(self):
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.points_input = QLineEdit()

        form_layout.addRow(QLabel("Username:"), self.username_input)
        form_layout.addRow(QLabel("Password:"), self.password_input)
        form_layout.addRow(QLabel("New Points Balance:"), self.points_input)

        button_scrape = QPushButton("Scrape for Vulnerabilities")
        button_scrape.clicked.connect(self.scrape_vulnerabilities)

        button_update_points = QPushButton("Update Points Balance")
        button_update_points.clicked.connect(self.update_points_balance)

        layout.addLayout(form_layout)
        layout.addWidget(button_scrape)
        layout.addWidget(button_update_points)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def scrape_vulnerabilities(self):
        vulnerabilities = self.scraper.scrape()
        self.database.save_vulnerabilities(vulnerabilities)
        # Implement further logic to display scraped vulnerabilities

    def update_points_balance(self):
        username = self.username_input.text()
        password = self.password_input.text()
        new_points = int(self.points_input.text())
        updated_points = self.scraper.manipulate_points(username, password, new_points)
        # Implement further logic to confirm the points update
        print(f"Updated points balance: {updated_points}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
