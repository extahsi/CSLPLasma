import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def login_and_get_points(username, password, url):
    try:
        # Configure Chrome options
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')

        # Setup Chrome driver
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
        
        logging.info(f'Navigating to {url}')
        driver.get(url)

        # Wait for the login form to load and input credentials
        time.sleep(5)
        
        logging.info('Entering login credentials')
        driver.find_element(By.NAME, 'username').send_keys(username)
        driver.find_element(By.NAME, 'password').send_keys(password)
        driver.find_element(By.NAME, 'password').send_keys(Keys.RETURN)

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
        points_balance_element = driver.find_element(By.ID, 'points_balance')  # Update this to the correct selector
        points_balance = points_balance_element.text
        logging.info(f'Points balance retrieved: {points_balance}')
        
        driver.quit()
        return points_balance
    except Exception as e:
        logging.error(f'Error in login_and_get_points: {e}')
        driver.quit()
        raise

