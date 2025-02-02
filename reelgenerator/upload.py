from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
import os
import time
from datetime import datetime



YOUTUBE = 'https://www.youtube.com/'
GOOGLE = 'https://www.google.com/'

def main():
    upload_to_youtube()

# pre-condition: takes in file path, description text, title
# post condition: uploads to youtube

# add args: filepath, description, title
def upload_to_youtube():
    firefox_options = Options()
    firefox_options.set_preference("dom.webdriver.enabled", False)  # Prevent detection
    firefox_options.set_preference("useAutomationExtension", False)

    # Load your Firefox profile
    firefox_profile_path = "/Users/ss/Library/Application Support/Firefox/Profiles/16oxmr2p.default-release"
    firefox_options.profile = webdriver.FirefoxProfile(firefox_profile_path)

    # Start Firefox WebDriver
    driver = webdriver.Firefox(options=firefox_options)
    driver.get("https://www.youtube.com")

    # click on the create button
    create = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Create')]"))
    )
    print("clicked!")
    create.click()

    # click on the upload button
    upload = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//yt-formatted-string[@id='label' and contains(text(), 'Upload video')]"))
    )
    upload.click()

    file_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")

    # add short video to upload
    filepath = os.path.join('/Users/ss/Desktop/reelgenerator', 'shorts', 'short.mp4')
    file_input.send_keys(filepath)

    # make a title
    wait = WebDriverWait(driver, 5)
    title_box = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'input-container')]//div[@id='textbox']")))
    title_box.clear()
    title_box.send_keys(generate_title())

    # make a description
    description_box = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@id, 'description-container')]//div[@id='textbox']")))
    description_box.clear()
    description_box.send_keys(generate_description())

    # select video not made for kids
    button = driver.find_element(By.NAME, "VIDEO_MADE_FOR_KIDS_NOT_MFK")
    button.click()
    
    # skip to last page
    for i in range(3): 
        next = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@aria-label='Next']")))
        next.click()

    # select public video
    public = driver.find_element(By.NAME, "PUBLIC")
    public.click()

    # sleep 10 seconds to make sure video loads, can usually sleep less
    time.sleep(10)

    save = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@aria-label='Publish']")))
    save.click()

    input("Check if your profile is loaded. Press Enter to quit...")
    driver.quit()



def generate_title():
    today_date = datetime.now().strftime("%m/%d/%Y")
    return "AskReddit " + today_date
    

def generate_description():
    return """Like and subscribe if you enjoy this short form content, and remember to get up and do something with your life :)
    \n#shorts #AskReddit""" # stub

"""
steps to upload:

press create
press upload video

"""


if __name__ == "__main__":
    main()


