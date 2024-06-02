import sys
import json
import logging
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton, QLineEdit, QMessageBox
from PyQt5.QtCore import Qt
import requests
from scraper import login_and_get_points
import tkinter as tk
from tkinter import messagebox
import subprocess


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Points Balance Scraper')
        self.setGeometry(100, 100, 800, 600)

        self.url = self.load_config()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('Enter username')
        self.layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('Enter password')
        self.password_input.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.password_input)

        self.points_label = QLabel('Points Balance: Not Retrieved')
        self.layout.addWidget(self.points_label)

        self.refresh_button = QPushButton('Refresh Points Balance')
        self.refresh_button.clicked.connect(self.refresh_points_balance)
        self.layout.addWidget(self.refresh_button)

        self.url_input = QLineEdit(self.url)
        self.url_input.setPlaceholderText('Enter URL')
        self.layout.addWidget(self.url_input)

        self.update_url_button = QPushButton('Update URL')
        self.update_url_button.clicked.connect(self.update_url)
        self.layout.addWidget(self.update_url_button)

        self.points_input = QLineEdit()
        self.points_input.setPlaceholderText('Enter new points balance')
        self.layout.addWidget(self.points_input)

        self.update_points_button = QPushButton('Update Points Balance')
        self.update_points_button.clicked.connect(self.update_points_balance)
        self.layout.addWidget(self.update_points_button)

        self.set_dark_mode()

    def set_dark_mode(self):
        self.setStyleSheet('''
            QWidget {
                background-color: #2e2e2e;
                color: #ffffff;
            }
            QPushButton {
                background-color: #444444;
                color: #ffffff;
                border: none;
                padding: 10px;
            }
            QLineEdit {
                background-color: #3e3e3e;
                color: #ffffff;
                border: 1px solid #5e5e5e;
                padding: 5px;
            }
        ''')

    def load_config(self):
        try:
            with open('config.json', 'r') as file:
                config = json.load(file)
                return config.get('url', 'https://rewards.cslplasma.com/rewards')
        except FileNotFoundError:
            logging.error('Config file not found. Using default URL.')
            return 'https://rewards.cslplasma.com/rewards'

    def save_config(self, url):
        try:
            with open('config.json', 'w') as file:
                json.dump({'url': url}, file)
            logging.info('Config file updated successfully.')
        except Exception as e:
            logging.error(f'Error saving config file: {e}')

    def refresh_points_balance(self):
        username = self.username_input.text()
        password = self.password_input.text()
        try:
            points_balance = login_and_get_points(username, password, self.url)
            self.points_label.setText(f'Points Balance: {points_balance}')
        except Exception as e:
            logging.error(f'Error retrieving points balance: {e}')
            QMessageBox.critical(self, 'Error', 'Failed to retrieve points balance.')

    def update_url(self):
        new_url = self.url_input.text()
        self.url = new_url
        self.save_config(new_url)
        QMessageBox.information(self, 'URL Updated', 'The URL has been updated successfully.')

    def update_points_balance(self):
        try:
            new_balance = int(self.points_input.text())
            response = requests.post('http://127.0.0.1:5000/update_points', json={'new_points': new_balance})
            if response.status_code == 200:
                QMessageBox.information(self, 'Success', 'Points balance updated successfully.')
                self.refresh_points_balance()
            else:
                QMessageBox.critical(self, 'Error', 'Failed to update points balance.')
        except ValueError:
            QMessageBox.critical(self, 'Error', 'Invalid points balance. Please enter an integer.')
        except Exception as e:
            logging.error(f'Error updating points balance: {e}')
            QMessageBox.critical(self, 'Error', 'Failed to update points balance.')


def run_scraper():
    username = username_entry.get()
    password = password_entry.get()

    if not username or not password:
        messagebox.showwarning("Input Error", "Please enter both username and password.")
        return

    try:
        subprocess.run(["python", "web_scraper.py", username, password], check=True)
        messagebox.showinfo("Success", "Points balance updated successfully.")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Failed to update points balance: {e}")
