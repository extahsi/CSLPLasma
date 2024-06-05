import logging
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def change_points_balance(username, password, new_points_balance):
    url = "https://rewards.cslplasma.com/login"
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

        # Inject JavaScript to change the points balance
        logging.info('Changing points balance')
        js_script = f'''
        const pointsElements = document.querySelectorAll('*');
        pointsElements.forEach(el => {{
            if (el.nodeType === Node.TEXT_NODE && el.nodeValue.trim().match(/^\\d+$/)) {{
                el.nodeValue = '{new_points_balance}';
            }} else if (el.innerText && (el.innerText.includes('points') || el.innerText.includes('pts') || el.innerText.includes('#text'))) {{
                el.innerText = '{new_points_balance} pts';
            }}
        }});
        '''
        driver.execute_script(js_script)
        logging.info(f'Points balance changed to: {new_points_balance} pts')

        # Verify the change
        time.sleep(5)  # Wait to see the change
        logging.info('Fetching updated points balance')
        updated_points_element = driver.find_element(By.CSS_SELECTOR, '.col-10.pl-0.mt-1 p')
        updated_points_text = updated_points_element.text
        updated_points_balance = int(updated_points_text.split()[0])  # Extracting the numeric value

        if updated_points_balance != new_points_balance:
            logging.error('Failed to change the points balance')
            driver.quit()
            raise Exception('Failed to change the points balance')

        logging.info(f'Updated points balance retrieved: {updated_points_balance}')

        driver.quit()
        return updated_points_balance
    except Exception as e:
        logging.error(f'Error in change_points_balance: {e}')
        driver.quit()
        raise
