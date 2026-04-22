import os
import time
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager

from modules.logger import setup_logger
from config import SCREENSHOTS_DIR

logger = setup_logger(__name__)

class BrowserBot:
    def __init__(self, headless: bool = False):
        self.headless = headless
        self.driver = None
        self.wait = None

    def start_browser(self):
        """
        Initializes the Chrome WebDriver.
        """
        try:
            logger.info("Starting browser...")
            chrome_options = Options()
            if self.headless:
                chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            
            # Setup service using webdriver_manager
            service = Service(ChromeDriverManager().install())
            
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.maximize_window()
            self.wait = WebDriverWait(self.driver, 10) # 10 seconds explicit wait
            
            logger.info("Browser launched successfully.")
        except Exception as e:
            logger.error(f"Failed to start browser: {e}")
            raise

    def visit(self, url: str):
        """
        Navigates to a target URL.
        """
        if not self.driver:
            logger.error("Browser not started. Call start_browser() first.")
            return

        try:
            logger.info(f"Navigating to {url}")
            self.driver.get(url)
            logger.info(f"Successfully visited {url}")
        except WebDriverException as e:
            logger.error(f"Failed to visit {url}. Error: {e}")

    def login(self, url: str, username_locator: tuple, password_locator: tuple, submit_locator: tuple, username: str, password: str):
         """
         Performs login automation.
         Locators should be tuples like (By.ID, 'username')
         """
         self.visit(url)
         try:
             logger.info("Attempting login...")
             # Wait for fields to be present
             user_field = self.wait.until(EC.presence_of_element_located(username_locator))
             pass_field = self.wait.until(EC.presence_of_element_located(password_locator))
             submit_btn = self.wait.until(EC.element_to_be_clickable(submit_locator))

             # Fill forms
             user_field.clear()
             user_field.send_keys(username)
             pass_field.clear()
             pass_field.send_keys(password)
             
             # Click submit
             submit_btn.click()
             logger.info("Login form submitted.")
             
         except TimeoutException:
             logger.error("Login elements not found within timeout period.")
         except Exception as e:
             logger.error(f"Error during login: {e}")

    def fill_form(self, locator: tuple, text: str):
        """
        Fills a specific input field.
        """
        try:
            element = self.wait.until(EC.presence_of_element_located(locator))
            element.clear()
            element.send_keys(text)
            logger.info(f"Filled form element {locator} with text.")
        except Exception as e:
            logger.error(f"Failed to fill form element {locator}. Error: {e}")

    def click_element(self, locator: tuple):
        """
        Clicks a specific element.
        """
        try:
            element = self.wait.until(EC.element_to_be_clickable(locator))
            element.click()
            logger.info(f"Clicked element {locator}.")
        except Exception as e:
            logger.error(f"Failed to click element {locator}. Error: {e}")

    def capture_screenshot(self, filename: str = "screenshot.png"):
        """
        Captures a screenshot of the current page.
        """
        if not self.driver:
            return

        filepath = SCREENSHOTS_DIR / filename
        try:
            self.driver.save_screenshot(str(filepath))
            logger.info(f"Screenshot saved to {filepath}")
        except Exception as e:
            logger.error(f"Failed to save screenshot. Error: {e}")

    def extract_text(self, locator: tuple) -> str:
        """
        Extracts visible text from a specific element.
        """
        try:
            element = self.wait.until(EC.presence_of_element_located(locator))
            text = element.text
            logger.info(f"Extracted text from {locator}.")
            return text
        except NoSuchElementException:
             logger.error(f"Element {locator} not found for text extraction.")
             return ""
        except Exception as e:
            logger.error(f"Failed to extract text from {locator}. Error: {e}")
            return ""

    def close_browser(self):
        """
        Closes the browser safely.
        """
        if self.driver:
            try:
                self.driver.quit()
                logger.info("Browser closed safely.")
            except Exception as e:
                logger.error(f"Error while closing browser: {e}")
        else:
            logger.warning("Attempted to close browser, but it was not running.")
