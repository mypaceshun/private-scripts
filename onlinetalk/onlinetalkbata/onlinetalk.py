import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

BASEURL = 'https://online-talk.jp'


def main():
    username = os.environ.get('ONLINETALK_USERNAME', 'username')
    password = os.environ.get('ONLINETALK_PASSWORD', 'password')
    cookies = authentication(username, password)
    get_apply_list(cookies)


def get_apply_list(cookies):
    url = f'{BASEURL}/user/link'
    res = requests.get(url, cookies=cookies)
    print(res.text)


def authentication(username, password):
    authurl = f"{BASEURL}/auth"
    loginurl = f"{BASEURL}/auth/login"

    res = requests.get(authurl)
    soup = BeautifulSoup(res.text, 'html.parser')
    token_key = '_token'
    token_el = soup.find('input', attrs={'type': 'hidden', 'name': token_key})

    data = {'login_id': username,
            'password': password,
            token_key: token_el.get('value')}
    res = requests.post(loginurl, data=data, cookies=res.cookies)
    return res.cookies
