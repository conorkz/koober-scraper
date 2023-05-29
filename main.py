from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime
import pytz
from bs4 import BeautifulSoup
import re
import os
directory = 'your_directory' #directory where you've saved all txt files from final.py file
s = Service("PATH_TO_CHROMEDRIVER")
driver = webdriver.Chrome(service=s)
driver.get('https://koober.com/fr/login')
time.sleep(5)
driver.find_element(By.CSS_SELECTOR, '[name=_username]').send_keys('your_login')
time.sleep(2)
driver.find_element(By.CSS_SELECTOR, '[name=_password]').send_keys('your_password')
time.sleep(2)
driver.find_element(By.CSS_SELECTOR, '[type=submit]').click()
time.sleep(5)
for file_name in os.listdir(directory):
    if file_name.endswith(".txt"):
        file_path = os.path.join(directory, file_name)
        with open(file_path, "r", encoding="utf-8") as file:
            contents = file.read()
            url = re.findall(r"https://koober.com/en/fiche/\S+", contents)[0]
            link = url.replace('fiche', 'lecture')
            print(link)
            driver.get(link)
            try:
                WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'button[type=button].btn.btn-danger.margin-top-20')))
                time.sleep(4)
            except:
                continue
            driver.find_element(By.CSS_SELECTOR, 'button[type=button].btn.btn-danger.margin-top-20').click()
            with open(file_path, "a", encoding="utf-8") as txtfile:
                current_time = datetime.now(pytz.timezone('Europe/Berlin'))
                berlin = current_time.strftime('%Y-%m-%d %H:%M:%S %Z')
                txtfile.write(f'Berlin time: {berlin}\n\n')
                while True:
                    WebDriverWait(driver, 180).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#lectureDiv')))
                    time.sleep(4)
                    soup = BeautifulSoup(driver.page_source, "html.parser")
                    for s in soup.find(id='lectureDiv').find_all(['p']):
                        txtfile.write(f'{s.text.strip()}\n\n')
                    try:
                        driver.find_element(By.CSS_SELECTOR, '.fa.fa-arrow-circle-right.fa-3x').click()
                    except:
                        break