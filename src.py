src = 'https://liveuamap.com/'


# Selenium Imports 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import uuid
import copy
from urllib.parse import urlparse
import numpy as np
import pandas as pd
import re 
from pathlib import Path
import os
import time
from datetime import date
from datetime import timedelta
from datetime import datetime
import dateutil.parser as parser
import re
import pandas as pd

import time

today = date.today()
cwd = os.getcwd()


# userprofile = 'main2'
options = webdriver.ChromeOptions()
# options.add_argument(f"user-data-dir={cwd}/."+userprofile+"UserProfile")
driver = webdriver.Chrome(ChromeDriverManager().install() , options=options)


from os import listdir
from os.path import isfile, join


while True:

    onlyfiles = [f for f in listdir('./output') if isfile(join('./output', f))]



    title_stack = [] 

    for fileName in onlyfiles:
        if 'csv' in fileName:
            df = pd.read_csv(f'./output/{fileName}')
            titles = df[['title']]['title'].tolist()
            title_stack = title_stack + titles
            

    print('------------ 1')

    driver.get(src)
    retrystack = 0

    siteLive = False
    while siteLive == False:
        print('------------ 1')
  
        check = driver.find_elements(By.XPATH,f"//a[@class='logo']")
        if len(check) > 0:
            siteLive = True
            retrystack = 0 
        else:
            retrystack = retrystack + 1 

            if retrystack >10:
                print('retrying- big ')

                time.sleep(5)
                driver.get(src)

            elif retrystack < 10:
                print('retrying- small ')

                time.sleep(100)
                driver.get(src)

    

    div = 'feedler'
    feedler = driver.find_element(By.XPATH,f"//div[@id='{div}']")

    cards = feedler.find_elements(By.XPATH,f'./*')



    write_flag = 0

    BIG_DATA = [] 

    for current_card in cards:
        print(current_card)
    # Check if title exists in stack 

        
        try:
#       
            webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
            webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()

            time.sleep(2)

            title_maybe = current_card.find_elements(By.XPATH,f".//div[@class='title']")
            if len(title_maybe)>0:
                pass
            else: 
                continue

            title = current_card.find_element(By.XPATH,f".//div[@class='title']").text


            if title in title_stack:
                break
            else:
            #     Run Code Here

                _uid = str(uuid.uuid4())


                _title = current_card.find_element(By.XPATH,f".//div[@class='title']").text
                print(_title)
                print('\n')
                _time = current_card.find_element(By.XPATH,f".//div[@class='time top-info']/span").text

                _src = current_card.find_element(By.XPATH,f".//div[@class='time top-info']/div[@class='top-right']/a").get_attribute('href')

                _time_capture = datetime.now()
                _screenshotted = False
                _domain = current_card.find_element(By.XPATH,f".//div[@class='time top-info']/img").get_attribute('src')
                time.sleep(1)
                try:
                    current_card.click()

                    current_card.click()
                except Exception:
                    print('nono')

                POPPUP = driver.find_element(By.XPATH,f"//div[@class='popup-info']")

                _full_text = POPPUP.text
                _screenshotted_2 = False


                time.sleep(1)

                _geo = POPPUP.find_element(By.XPATH,f".//div[@class='marker-time']/a").text



                webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
                webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()


                DATA = {
                    'uid' : _uid,
                    'title' : _title,
                    'time' : _time,
                    'source' : _src,
                    'time-capture' : _time_capture,
                    'sc' : _screenshotted,
                    'domain' : _domain,
                    'full-text' : _full_text,
                    'sc2' : _screenshotted_2,
                    'geo' : _geo



                }




                BIG_DATA.append(DATA)
        except Exception:
            print('EXITING PREMATURE')
            if len(BIG_DATA)>1 : 
                timenow = datetime.now()
                t =pd.DataFrame(BIG_DATA)
                t.to_csv(f'./output/{timenow}.csv')
                write_flag = 1 

    if write_flag == 0 and len(BIG_DATA)>1 :  
        timenow = datetime.now()
        t =pd.DataFrame(BIG_DATA)
        t.to_csv(f'./output/{timenow}.csv')

    print('\n\n sleeping----------\n\n')
    time.sleep(100)