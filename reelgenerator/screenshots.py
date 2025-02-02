from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
import time


def get_title_screenshot(post_url, post_id, output_path):
    try:
        firefox_options = Options()
        firefox_options.set_preference("dom.webdriver.enabled", False) 
        firefox_options.set_preference("useAutomationExtension", False)

        firefox_profile_path = "/Users/ss/Library/Application Support/Firefox/Profiles/16oxmr2p.default-release"
        firefox_options.profile = webdriver.FirefoxProfile(firefox_profile_path)

        driver = webdriver.Firefox(options=firefox_options)
        driver.get(post_url)

        handle = By.ID
        id = f"post-title-t3_{post_id}"
        Wait = WebDriverWait(driver, 10)
        search = Wait.until(EC.presence_of_element_located((handle, id)))

        search.screenshot(output_path)
        print(f"Screenshot of element saved to {output_path}")

    finally:
        driver.quit()
