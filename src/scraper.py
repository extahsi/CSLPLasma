
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def login_and_get_points(username, password):
    driver = None  # Initialize driver to None
    try:
        # Automatically download and setup the correct chromedriver
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

        # Open the login page
        logging.info('Opening login page.')
        driver.get('https://rewards.cslplasma.com/rewards')

        # Find the login elements and enter credentials
        logging.info('Entering username and password.')
        username_field = driver.find_element(By.NAME, 'username')  # Update according to actual element name
        password_field = driver.find_element(By.NAME, 'password')  # Update according to actual element name
        username_field.send_keys(username)
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)

        # Allow time for the page to load
        time.sleep(5)

        # Navigate to the page showing the points balance
        logging.info('Navigating to points balance page.')
        driver.get('https://rewards.cslplasma.com/rewards/points_balance')
        time.sleep(3)

        # Extract the points balance
        logging.info('Extracting points balance.')
        points_element = driver.find_element(By.ID, 'points-balance')  # Update according to actual element ID
        points_balance = points_element.text

        # Close the driver
        driver.quit()
        logging.info('Points balance retrieved successfully.')

        return points_balance
    except Exception as e:
        if driver:
            driver.quit()  # Ensure the driver is closed if an exception occurs
        logging.error(f'Error occurred: {e}')
        raise e
