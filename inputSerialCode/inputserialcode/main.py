#!./venv/bin/python

import os
from dotenv import load_dotenv
from selenium import webdriver

load_dotenv()

USERNAME = os.environ.get('USERNAME', 'username')
PASSWORD = os.environ.get('PASSWORD', 'pssword')

def main():
    driver = webdriver.Firefox()
    driver.get('https://mg.withlive-app.com/registerCodes')
    login(driver)


def login(driver):
    username_el = driver.find_element_by_id('input-28')
    username_el.send_keys(USERNAME)
    password_el = driver.find_element_by_id('input-31')
    password_el.send_keys(PASSWORD)
    submit_el = driver.find_element_by_tag_name('button')
    submit_el.click()

def input_serials(driver, selial_list):
    pass

if __name__ == '__main__':
    main()
