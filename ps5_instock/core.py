import time
import logging
import pyconfig

# Import adds chromedriver automatically to the PATH
# Installed with pip install chromedriver-binary-auto
# Path to chromedriver binary can also be specified manually in function check_stock()
import chromedriver_binary

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from mail import send_email

# Loading config
config = pyconfig.Config.from_json_file("config.example.json")

# Logger configuration
logging.basicConfig()
LOG_FORMAT = '%(levelname) -10s %(asctime)s %(name) -30s %(funcName) -35 %(lineno) -5d: %(message)s'
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def stock_routine():
    """Checking stock for all vendors specified in config file.
    """
    logger.info("- - - - - - - - - - Checking stock for all vendors - - - - - - - - - -")

    vendors = config.get("vendors")

    for vendor in vendors:
        check_stock(vendor)


def check_stock(vendor):
    """Checking stock for one vendor as specified in config file.
    Args:
        vendor: Dictionary containing the name of the vendor, the url to the product and the id of the element to check for.
        For example check for the id of the add to cart button.

    """
    logger.info(f"Checking availability at {vendor['vendor']}")

    chrome_options = Options()
    chrome_options.add_argument("--headless")

    # You may pass the path to the chromedriver location if the python import chromedriver_binary
    # does not work for your version
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(vendor["url"])
    time.sleep(2)

    try:
        driver.find_element_by_id(vendor["lookfor"])
        available = True
    except Exception:
        available = False

    driver.quit()
    if available:
        logger.info(f"Playstation 5 available at {vendor['vendor']}: {vendor['url']}")
        content = f"Playstation 5 available at {vendor['vendor']}: {vendor['url']}"
        send_email(mail_content=content, receivers=config.get("mail.receivers"),
                   subject=f"{vendor['vendor']}: PS5 is available!!",
                   credentials={"login": config.get("mail.login"),
                                "password": config.get("mail.password"),
                                "smtp_host": config.get("mail.smtp_host"),
                                "smtp_port": config.get("mail.smtp_port")})
        return vendor["vendor"], vendor["url"], available

    logger.info(f"Not available at {vendor['vendor']}")


def main():
    """Main loop checking stock for all vendors every x seconds as specified in the config file."""
    while True:
        try:
            stock_routine()
        except Exception:
            logger.error(f"Something went wrong trying again in {config.get('checkInterval')} seconds!")
        time.sleep(config.get("checkInterval"))


if __name__ == "__main__":
    main()
