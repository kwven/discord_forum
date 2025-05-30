import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
from selenium.webdriver.common.keys import Keys
import json
from datetime import datetime
from get_message_thread import thread_extracts
from postgres_code import *


EMAIL = os.getenv('EMAIL')
PASSWORD = os.getenv('PASSWORD')
SERVER_ID = os.getenv('SERVER_ID')
CHANNEL_ID = os.getenv('CHANNEL_ID')
#chrome setup

chrome_options = Options()
chrome_options.headless=False
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

#login 
driver.get("https://discord.com/login")
# Wait for login to load
WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.NAME, "email"))
        )
time.sleep(6)       
# Enter email and password
driver.find_element(By.NAME, "email").send_keys(EMAIL)
driver.find_element(By.NAME, "password").send_keys(PASSWORD)
time.sleep(2)


# Click the login button
driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
WebDriverWait(driver, 30).until(
EC.presence_of_element_located((By.CSS_SELECTOR, "[class*='sidebar']")),
message="Timed out waiting for Discord to load after login"
)
time.sleep(5)
print("Successfully logged in to Discord")
#go to the forum
forum_url = f"https://discord.com/channels/{SERVER_ID}/{CHANNEL_ID}"
driver.get(forum_url)
time.sleep(5)
# Wait for the forum to load
WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div[class*='container']"))
)
time.sleep(4)
#click tout button 
tout_buttons = driver.find_elements(By.CSS_SELECTOR, "button[class*='tagsButton']")
for button in tout_buttons:
        time.sleep(3)
        if button.is_displayed():
                driver.execute_script("arguments[0].click();", button)
                time.sleep(2)
                print(f"Clicked on tout button")
                break
time.sleep(3)

