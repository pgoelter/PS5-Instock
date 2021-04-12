import time
import logging
import pyconfig
import chromedriver_binary
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from mail import send_email

config = pyconfig.Config.from_json_file("config.json")
logging.basicConfig()

LOG_FORMAT = '%(levelname) -10s %(asctime)s %(name) -30s %(funcName) -35 %(lineno) -5d: %(message)s'
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def stock_routine():
    logger.info("- - - - - - - - - - Checking stock for all vendors - - - - - - - - - -")
    availability_list = []

    vendors = config.get("vendors")

    for vendor in vendors:
        check_stock(vendor)


def check_stock(vendor):
    logger.info(f"Checking availability at {vendor['vendor']}")

    chrome_options = Options()
    chrome_options.add_argument("--headless")

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
                   credentials={"login": config.get("mail.sender"),
                                "password": config.get("mail.password"),
                                "smtp_host": config.get("mail.smtp_host"),
                                "smtp_port": config.get("mail.smtp_port")})
        return vendor["vendor"], vendor["url"], available

    logger.info(f"Not available at {vendor['vendor']}")


def main():
    while True:
        try:
            stock_routine()
        except Exception:
            logger.error(f"Something went wrong trying again in {config.get('checkInterval')} seconds!")
        time.sleep(config.get("checkInterval"))


if __name__ == "__main__":
    main()
