from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
import os
import logging

def get_selenium_driver():
    """Initialize and return a new Selenium WebDriver instance."""
    try:
        options = Options()
        options.headless = True  # Run in headless mode

        # Check if running inside Docker
        if os.path.exists("/.dockerenv"):
            options.binary_location = "/usr/bin/firefox"  # Path to Firefox binary in Docker
            service = Service(executable_path="/usr/local/bin/geckodriver")  # Path to Geckodriver in Docker
        else:
            # Use WebDriver Manager to download and set up Geckodriver for local environment
            service = Service(GeckoDriverManager().install())

        driver = webdriver.Firefox(service=service, options=options)
        logging.info("Selenium WebDriver initialized successfully.")
        return driver
    except Exception as e:
        logging.error(f"Failed to initialize Selenium WebDriver: {e}")
        return None
