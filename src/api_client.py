# api_client.py

import requests

class CSLPlasmaAPIClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_points_balance(self, username, password):
        # Define API endpoint for retrieving points balance
        endpoint = f"{self.base_url}/login"
        
        # Create request payload with username and password
        data = {
            'username': username,
            'password': password
        }

        try:
            # Make HTTP POST request to authenticate and retrieve points balance
            response = requests.post(endpoint, json=data)
            response.raise_for_status()  # Raise an exception for any HTTP error
            balance_data = response.json()

            # Extract points balance from response data
            points_balance = balance_data['points_balance']
            return points_balance
        except requests.RequestException as e:
            print(f"Error retrieving points balance: {e}")
            return None
