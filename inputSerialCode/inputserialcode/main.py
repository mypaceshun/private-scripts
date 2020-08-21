#!./venv/bin/python

import os
import sys
import time
from pathlib import Path
from dotenv import load_dotenv
from selenium import webdriver

load_dotenv()

USERNAME = os.environ.get('USERNAME', 'username')
PASSWORD = os.environ.get('PASSWORD', 'pssword')
SERIALCODES_PATH = os.environ.get('SERIALCODES_PATH', 'serialcodes.txt')

def main():
    driver = webdriver.Firefox()
    driver.get('https://mg.withlive-app.com/registerCodes')
    login(driver)
    serials = load_serials(SERIALCODES_PATH)
    # 10件ずつしか登録出来ない
    serials_sp = serial_split(serials)
    total_serials = len(serials)
    curr_serials = 1
    for _serials in serials_sp:
        input_serials(driver, _serials)
        curr_serials += len(_serials)
        print(f'Input {curr_serials-len(_serials)} - {curr_serials-1}')
        if curr_serials < total_serials:
            try:
                input(f'Enter Next serials [{curr_serials}〜/{total_serials}]: ')
                driver.get('https://mg.withlive-app.com/registerCodes')
            except KeyboardInterrupt as error:
                print('\nInput Finish!')
                write_unused_serials(serials, curr_serials)
                sys.exit(0)
        else:
            pass
    print('\nInput Finish!')

def login(driver):
    username_el = driver.find_element_by_id('input-28')
    username_el.send_keys(USERNAME)
    password_el = driver.find_element_by_id('input-31')
    password_el.send_keys(PASSWORD)
    submit_el = driver.find_element_by_tag_name('button')
    submit_el.click()
    time.sleep(3)


def load_serials(serialcodes_path):
    spath = Path(serialcodes_path)
    serials = []
    with spath.open('r') as fd:
        serials = [serial.strip() for serial in fd]
    return serials


def serial_split(serials, split_num=10):
    serials_sp = []
    tmp_serials = []
    for serial in serials:
        tmp_serials.append(serial)
        if len(tmp_serials) >= split_num:
            serials_sp.append(tmp_serials)
            tmp_serials = []
    if len(tmp_serials) != 0:
        serials_sp.append(tmp_serials)
    return serials_sp


def write_unused_serials(serials, curr_serials):
    filename = 'unused_serialcodes.txt'
    unused_serial_path = Path(filename)
    unused_num = curr_serials - 1
    unused_serials = serials[unused_num:]
    with unused_serial_path.open('w') as fd:
        for serial in unused_serials:
            fd.write(f'{serial}\n')
    print(f'Wrote unused serialcodes[{filename}]')


def input_serials(driver, serial_list):
    serial_num = len(serial_list)
    assert serial_num < 11
    add_el_button = driver.find_element_by_tag_name('button')
    for i in range(serial_num - 1):
        add_el_button.click()
    input_els = driver.find_elements_by_tag_name('input')
    assert len(input_els) == serial_num
    for _el, _serial in zip(input_els, serial_list):
        _el.clear()
        _el.send_keys(_serial)
    send_button_el = driver.find_element_by_class_name('input-send-button')
    send_button_el.click()

if __name__ == '__main__':
    main()
