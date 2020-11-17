import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASEURL = 'https://ngt48cd.shop'
APIURL = f'{BASEURL}/api/v1'

def main():
    username = os.environ.get('NGT48CD_USERNAME', 'username')
    password = os.environ.get('NGT48CD_PASSWORD', 'password')
    cookies = authentication(username, password)
    tickets = get_tickets(cookies)
    print(tickets)

def get_tickets(cookies):
    url = f'{APIURL}/clasptickets'
    params = {'group': 'NGT48', 'limit': 10, 'status': 'all'}
    res = requests.get(url, cookies=cookies, params=params)
    return res.json()

def authentication(username, password):
    auth_url = f'{APIURL}/authentication'
    jsondata = f'{{"id": "{username}", "password": "{password}"}}'
    res = requests.get(auth_url)
    res = requests.put(auth_url, data=jsondata, cookies=res.cookies)
    return res.cookies
