from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient
from selenium.common import exceptions


def _parse_element(element, class_name):
    result = WebDriverWait(element, 15).until(
        EC.presence_of_element_located((By.CLASS_NAME, class_name))).text
    return result

def parse_email(element):
    single_letter = {}
    single_letter['from'] = _parse_element(
        element, 'letter-contact')
    single_letter['date'] = _parse_element(
        element, 'letter__date')
    single_letter['subject'] = _parse_element(
        element, 'thread__subject')
    single_letter['body'] = _parse_element(
        element, 'letter-body__body')

    return single_letter


client = MongoClient('127.0.0.1', 27017)
db = client['letters']
letters = db.letters

chrome_options = Options()
chrome_options.add_argument('start-maximized')

driver = webdriver.Chrome('./chromedriver.exe',options=chrome_options)
driver.get('https://mail.ru/')

login = driver.find_element_by_id('mailbox:login-input')
login.send_keys('study.ai_172@mail.ru')
login.send_keys(Keys.RETURN)

time.sleep(2)
passw = driver.find_element_by_id('mailbox:password-input')
passw.send_keys('NextPassword172')

passw.send_keys(Keys.RETURN)
wait_load = WebDriverWait(driver, 10)

div = WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.CLASS_NAME, 'dataset__items'))
)

first_letter = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located(
        (By.CLASS_NAME, 'js-letter-list-item')
    )
)
first_letter.click()

wait = WebDriverWait(driver, 10)
while True:
    try:
        letters.insert_one(parse_email(driver))
        print(parse_email(driver))
        button_next = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'button2_arrow-down')))
        button_next.click()
    except exceptions.TimeoutException:
        print('E-mails are over')
        break
driver.quit()
