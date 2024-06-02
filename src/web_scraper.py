import logging
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import requests
import json

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def login_and_get_points(username, password, url):
    try:
        # Configure Chrome options
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--start-maximized')

        # Setup Chrome driver
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

        logging.info(f'Navigating to {url}')
        driver.get(url)

        # Wait for the login form to load and input credentials
        time.sleep(5)

        logging.info('Entering login credentials')
        driver.find_element(By.CSS_SELECTOR, '.input-no-border.ml-md-3.ml-1[maxlength="10"]').send_keys(username)
        driver.find_element(By.CSS_SELECTOR, '.form-control').send_keys(password)
        driver.find_element(By.CSS_SELECTOR, '.form-control').send_keys(Keys.RETURN)

        # Wait for the login process to complete and the rewards page to load
        time.sleep(10)

        # Ensure we are on the correct page
        logging.info('Checking if login was successful')
        if "rewards" not in driver.current_url:
            logging.error('Failed to log in, check your credentials and URL.')
            driver.quit()
            raise Exception('Failed to log in')

        # Find the points balance element on the page
        logging.info('Fetching points balance')
        points_element = driver.find_element(By.CSS_SELECTOR, '.col-10.pl-0.mt-1 p')
        points_text = points_element.text
        points_balance = int(points_text.split()[0])  # Extracting the numeric value
        logging.info(f'Points balance retrieved: {points_balance}')

        driver.quit()
        return points_balance
    except Exception as e:
        logging.error(f'Error in login_and_get_points: {e}')
        driver.quit()
        raise

def update_points_balance(driver, new_balance):
    try:
        points_element = driver.find_element(By.CSS_SELECTOR, '.col-10.pl-0.mt-1 p')
        driver.execute_script("arguments[0].childNodes[0].nodeValue = arguments[1]", points_element, f"{new_balance} pts")
        time.sleep(2)  # Wait for the changes to take effect
        updated_balance = driver.find_element(By.CSS_SELECTOR, '.col-10.pl-0.mt-1 p').text.split()[0]
        if updated_balance == str(new_balance):
            logging.info(f'Points balance updated to: {updated_balance}')
            return True
        else:
            logging.error('Failed to update points balance')
            return False
    except Exception as e:
        logging.error(f'Error updating points balance: {e}')
        return False

def update_points_on_server(new_balance, api_url):
    try:
        response = requests.post(api_url, json={'new_points': new_balance})
        if response.status_code == 200:
            logging.info('Points balance updated on server')
            return True
        else:
            logging.error(f'Failed to update points balance on server: {response.status_code}')
            return False
    except Exception as e:
        logging.error(f'Error updating points balance on server: {e}')
        return False

def main(username, password):
    with open('config.json', 'r') as file:
        config = json.load(file)

    try:
        points_balance = login_and_get_points(username, password, config['login_url'])

        if points_balance is not None:
            new_balance = 150  # New points balance to set

            # Configure Chrome options
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--start-maximized')

            # Setup Chrome driver
            driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

            logging.info(f'Navigating to {config["login_url"]}')
            driver.get(config["login_url"])

            # Wait for the login form to load and input credentials
            time.sleep(5)

            logging.info('Entering login credentials')
            driver.find_element(By.CSS_SELECTOR, '.input-no-border.ml-md-3.ml-1[maxlength="10"]').send_keys(username)
            driver.find_element(By.CSS_SELECTOR, '.form-control').send_keys(password)
            driver.find_element(By.CSS_SELECTOR, '.form-control').send_keys(Keys.RETURN)

            # Wait for the login process to complete and the rewards page to load
            time.sleep(10)

            # Ensure we are on the correct page
            logging.info('Checking if login was successful')
            if "rewards" not in driver.current_url:
                logging.error('Failed to log in, check your credentials and URL.')
                driver.quit()
                raise Exception('Failed to log in')

            if update_points_balance(driver, new_balance):
                update_points_on_server(new_balance, config['api_url'])

            driver.quit()
    except Exception as e:
        logging.error(f'Error in main: {e}')

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        logging.error('Usage: python web_scraper.py <username> <password>')
        sys.exit(1)
    username = sys.argv[1]
    password = sys.argv[2]
    main(username, password)
