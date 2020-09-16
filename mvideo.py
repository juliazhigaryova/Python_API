from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient
from selenium.common import exceptions

client = MongoClient('127.0.0.1', 27017)
db = client['hits']
hits = db.hits

chrome_options = Options()
chrome_options.add_argument('start-maximized')

driver = webdriver.Chrome('./chromedriver.exe',options=chrome_options)
driver.get('https://www.mvideo.ru')

assert 'М.Видео' in driver.title


try:
    bests = driver.find_element_by_xpath(
        '//div[contains(text(),"Хиты продаж")]/ancestor::div[@data-init="gtm-push-products"]'
    )
except exceptions.NoSuchElementException:
    print('Bestsellers has not been found')

while True:
    try:
        next_button = WebDriverWait(bests, 5).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'a[class="next-btn sel-hits-button-next"]')
            )
        )

        driver.execute_script("$(arguments[0]).click();", next_button)
    except exceptions.TimeoutException:
        print('Сбор данных окончен')
        break

goods = bests.find_elements_by_css_selector('li.gallery-list-item')
item = {}
for good in goods:
    item['title'] = good.find_element_by_class_name('sel-product-tile-title').text
    item['good_link'] = good.find_element_by_xpath(".//a[@class='sel-product-tile-title']").get_attribute('href')

    item['price'] = good.find_element_by_class_name('c-pdp-price__current').text.replace(
                '&nbsp;', '').replace('¤', '')
    hits.update_one({'good_link': item['good_link']}, {'$set': item},upsert=True)
driver.quit()
