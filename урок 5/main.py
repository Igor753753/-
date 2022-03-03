# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from lib2to3.pgen2 import driver
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
from pymongo import MongoClient
from datetime import datetime
import re


def parse_mail():
    mongo_db = MongoClient('localhost', 27017)['lesson_5']
    collection = mongo_db['mailru' + datetime.today().strftime('_on_%d_%m_%Y')]

    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get('https://mail.ru/')

    # Авторизация
    # Логин
    form = WDW(driver, 5).until(
        EC.element_to_be_clickable((By.NAME, 'login'))
    )
    form.send_keys('study.ai_172@mail.ru')

    button = WDW(driver, 5).until(
        EC.element_to_be_clickable((By.NAME, 'saveauth'))
    )
    button.click()
    #  пароль
    button = WDW(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, '//button[contains(@data-tested, "enter-password")]'))
    )
    button.click()
    # Пароль
    form = WDW(driver, 5).until(
        EC.element_to_be_clickable((By.NAME, 'password'))
    )
    form.send_keys('NextPassword172#')
    # войти
    button = WDW(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, '//button[contains(@data-tested, "login-to-mail")]'))
    )
    button.click()

    #  первое письмо
    button = WDW(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, '//a[contains(@class, "js-letter-list-item")]'))
    )
    driver.get(button.get_attribute('href'))

    while True:
        from_user = WDW(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'span.letter-contact'))
        ).get_attribute('title')
        sent_date = WDW(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.letter__date'))
        ).text
        subject = WDW(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'h2.thread__subject'))
        ).text
        text = WDW(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.letter-body'))
        ).text
        text = re.sub('^\s+', '', re.sub('\s{2,}', ' ', text))

        collection.insert_one({
            'from_user': from_user,
            'sent_date': sent_date,
            'subject': subject,
            'text': text
        })

        try:
            button = WDW(driver, 5).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//span[contains(@title, "Следующее")] | //span[contains(@data-title, "Следующее")]')
                )
            )
            button.click()
            WDW(driver, 10).until(EC.url_changes(driver.current_url))
        except:
            print(f'С почтового ящика study.ai_172@mail.ru собрано {collection.count_documents()} писем')
            break


driver.quit()
