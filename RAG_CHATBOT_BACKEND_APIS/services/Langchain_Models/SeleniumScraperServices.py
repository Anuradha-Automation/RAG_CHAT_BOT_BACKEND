import logging
import time
import traceback
from urllib.parse import urljoin
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
from seleniumbase import Driver

# Set up logging
logger = logging.getLogger("myapp")
HEADLESS = True

class SeleniumScraperServices:
    """
    Selenium-based web scraper service class for extracting links and text content from websites.
    """

    @staticmethod
    def init_web_driver():
        """
        Initializes and returns a Selenium WebDriver instance.

        Returns:
            Driver or None: The initialized WebDriver instance or None if initialization fails.
        """
        try:
            user_agent = UserAgent().random
            logger.debug(f"Initializing WebDriver with User Agent: {user_agent}")
            options = {"uc": True, "headless": HEADLESS}
            driver = Driver(**options)
            driver.execute_script(
                f"Object.defineProperty(navigator, 'userAgent', {{get: function() {{ return '{user_agent}'; }} }});"
            )
            logger.debug("WebDriver initialized successfully")
            return driver
        except Exception as e:
            error_message = f"Error initializing WebDriver: {str(e)}\n{traceback.format_exc()}"
            logger.error(error_message)
            return None

    @staticmethod
    def get_links_selenium(website_url):
        """
        Extracts all links from a given website URL.

        Args:
            website_url (str): The URL of the website to scrape.

        Returns:
            tuple: (bool, list) - (success status, list of extracted links)
        """
        driver = None
        try:
            driver = SeleniumScraperServices.init_web_driver()
            if not driver:
                logger.error("WebDriver initialization failed")
                return False, []

            logger.info(f"Opening website: {website_url}")
            driver.get(website_url)
            time.sleep(3)  # Wait for page to load

            logger.debug(f"Finding elements with tag 'a' on {website_url}")
            elements = driver.find_elements(By.TAG_NAME, "a")
            links = {urljoin(website_url, elem.get_attribute("href")) for elem in elements if elem.get_attribute("href")}
            logger.debug(f"Extracted {len(links)} links from {website_url}")

            return True, list(links)
        except WebDriverException as e:
            error_message = f"Failed to open website {website_url}: {str(e)}\n{traceback.format_exc()}"
            logger.error(error_message)
            return False, []
        except Exception as e:
            error_message = f"Unexpected error extracting links from {website_url}: {str(e)}\n{traceback.format_exc()}"
            logger.error(error_message)
            return False, []
        finally:
            if driver:
                driver.quit()
                logger.debug(f"Closed WebDriver for {website_url}")

    @staticmethod
    def extract_text_selenium(url):
        """
        Extracts text content from a given URL.

        Args:
            url (str): The URL to extract text from.

        Returns:
            str: The extracted text content, or an empty string if extraction fails.
        """
        driver = None
        try:
            driver = SeleniumScraperServices.init_web_driver()
            if not driver:
                logger.error("WebDriver initialization failed")
                return ""

            logger.debug(f"Extracting text from: {url}")
            driver.get(url)
            time.sleep(5)  # Wait for page to load fully

            text = driver.find_element(By.TAG_NAME, "body").text
            logger.debug(f"Extracted text length: {len(text)} characters from {url}")
            return text
        except WebDriverException as e:
            error_message = f"Error extracting text from {url}: {str(e)}\n{traceback.format_exc()}"
            logger.error(error_message)
            return ""
        except Exception as e:
            error_message = f"Unexpected error extracting text from {url}: {str(e)}\n{traceback.format_exc()}"
            logger.error(error_message)
            return ""
        finally:
            if driver:
                driver.quit()
                logger.debug(f"Closed WebDriver for {url}")

    @staticmethod
    def get_links_selenium_get_response_data(website_url):
        """
        Extracts links and text content from a website URL.

        Args:
            website_url (str): The URL of the website to scrape.

        Returns:
            tuple: (bool, str, list) - (success status, message, list of extracted text data)
        """
        extracted_data = []
        logger.info(f"Starting data extraction from {website_url}")

        link_status, links = SeleniumScraperServices.get_links_selenium(website_url)
        logger.debug(f"Link extraction status: {link_status}, number of links: {len(links)}")

        if not link_status:
            error_message = f"Failed to open website: {website_url}"
            logger.error(error_message)
            return False, error_message, []

        for link in links:
            try:
                text = SeleniumScraperServices.extract_text_selenium(link)
                if text:
                    extracted_data.append(text)
                    logger.debug(f"Successfully extracted text from {link}, length: {len(text)}")
                else:
                    logger.debug(f"No text extracted from {link}")
            except Exception as e:
                error_message = f"Error extracting text from {link}: {str(e)}\n{traceback.format_exc()}"
                logger.error(error_message)

        if extracted_data:
            success_message = f"Successfully extracted data from {len(extracted_data)} URLs"
            logger.info(success_message)
            return True, success_message, extracted_data
        else:
            error_message = f"No data extracted from {website_url}"
            logger.warning(error_message)
            return False, error_message, []