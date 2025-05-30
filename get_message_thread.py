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
from postgres_code import *
def thread_extracts(driver,scroll_number,category_id):     
        all_titles=[]
        thread_id=1
        for k in range(scroll_number):     
                thread_elements = driver.find_elements(By.CSS_SELECTOR, "li[class*='card_f369db']")
                print(f"Found {len(thread_elements)} thread cards")
                for i in range(len(thread_elements)):
                        all_messages=[]
                        thread_elements = driver.find_elements(By.CSS_SELECTOR, "li[class*='card_f369db']")
                        thread_element=thread_elements[i]
                        #title working good
                        title_element = thread_element.find_element(By.CSS_SELECTOR, "h3[class*='lineClamp2Plus_4bd52'], div[class*='headerText_faa96b'] span")
                        title = title_element.text.strip()
                        if title not in all_titles:
                                all_titles.append(title)
                                print(title)
                                title_db=title
                                time.sleep(3) 
                                #no we will enter the threads
                                clickable_element = thread_element.find_element(By.CSS_SELECTOR, "div[class*='focusTarget_faa96b'], div[role='button'], div[tabindex='-1']")
                                driver.execute_script("arguments[0].click();", clickable_element)
                                time.sleep(2)
                                WebDriverWait(driver, 10).until(
                                EC.presence_of_element_located((By.CSS_SELECTOR, "div[class*='cozyMessage']"))
                                )
                                #scrappe all messages from the 
                                messages_container=driver.find_elements(By.CSS_SELECTOR,"div[class*='cozyMessage']")
                                for msg_id,msg_element in enumerate(messages_container,start=1):
                                        try:
                                                #extract content
                                                content_element = msg_element.find_element(By.CSS_SELECTOR,"div[class*='messageContent']")
                                                if not content_element:
                                                        content="image"
                                                else:
                                                        content = content_element.text
                                                try:
                                                        # Extract author
                                                        author_element = msg_element.find_element(By.CSS_SELECTOR, "[class*='username']")
                                                        author = author_element.text
                                                #sometimes people send 2 to 3 messages one after one so we need to give the message same author 
                                                except:
                                                        author=all_messages[-1]['author']
                                                # Extract timestamp
                                                timestamp_element = msg_element.find_element(By.CSS_SELECTOR, "time")
                                                timestamp = timestamp_element.get_attribute("datetime")
                                                clean_ts = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d %H:%M:%S")
                                                all_messages.append({
                                                "content": content,
                                                "author": author,
                                                "timestamp": clean_ts,
                                                "id": msg_id
                                                })
                                        except:
                                                pass
                                        
                                try:
                                        insert_threads(category_id,thread_id,title_db,all_messages[0]["content"],all_messages[0]["author"],all_messages[0]["timestamp"])
                                        try:
                                                for message in all_messages[1:]:
                                                        insert_answers(category_id,thread_id,message["id"],message["content"],message["author"],message["timestamp"])
                                        except Exception as e:
                                                print("Error inserting answers:", e)
                                except Exception as e:
                                        print("Error inserting thread:", e)     
                        thread_id+=1         
                #how to scroll
                scroll_step = 1000
                #script to scroll
                message_container = driver.find_element(By.CSS_SELECTOR, "div[class*='auto']")
                driver.execute_script("arguments[0].scrollTop += arguments[1];", message_container, scroll_step)
                time.sleep(5)

