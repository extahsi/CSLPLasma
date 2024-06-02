import requests
import logging

class CSLPlasmaAPIClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.logger = logging.getLogger(__name__)

    def get_points_balance(self, username, password):
        endpoint = '/get_points'
        url = self.base_url + endpoint
        try:
            response = requests.get(url, auth=(username, password))
            response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
            data = response.json()
            points_balance = data.get('points_balance')
            return points_balance
        except Exception as e:
            self.logger.error(f"Error retrieving points balance: {e}")
            return None

    def update_points_balance(self, username, password, new_balance):
        endpoint = '/update_points'
        url = self.base_url + endpoint
        try:
            response = requests.post(url, json={'new_points': new_balance}, auth=(username, password))
            response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
            data = response.json()
            new_balance = data.get('new_balance')
            return new_balance
        except Exception as e:
            self.logger.error(f"Error updating points balance: {e}")
            return None
