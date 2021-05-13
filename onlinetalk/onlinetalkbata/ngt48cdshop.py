import os
import requests
from datetime import datetime
from json.decoder import JSONDecodeError
from dotenv import load_dotenv

load_dotenv()

BASEURL = 'https://ngt48cd.shop'
APIURL = f'{BASEURL}/api/v1'

def main():
    username = os.environ.get('NGT48CD_USERNAME', 'username')
    password = os.environ.get('NGT48CD_PASSWORD', 'password')
    cookies = authentication(username, password)
    tickets = get_tickets(cookies)
    query = {
            'after_today': True,
            }
    tickets = filter_tickets(tickets, query)
    tickets = sum_tickets(tickets)
    keys = [int(k) for k in tickets.keys()]
    keys = [str(k) for k in sorted(keys)]
    print(keys)
    stotal = 0
    total = 0
    for _id in keys:
        member = tickets[_id]['member']
        bu = tickets[_id]['section']['name']
        count = tickets[_id]['count']
        success_count = tickets[_id]['success_count']
        date = tickets[_id]['date']
        row = f'{date} {member} {bu}: {success_count} / {count}'
        print(row)
        total += count
        stotal += success_count
    print(f'total: {stotal} / {total}')


def filter_tickets(tickets, query):
    for one_apply in tickets:
        entries = one_apply['entry']
        _entries = []
        for entry in entries:
            if query['after_today']:
                today = datetime.today()
                datestr = entry['date']
                date = datetime.strptime(datestr, '%Y-%m-%d')
                if today < date:
                    _entries.append(entry)
        one_apply['entry'] = _entries
    return tickets

def sum_tickets(tickets):
    sum_record = {}
    for one_apply in tickets:
        entries = one_apply['entry']
        for entry in entries:
            _id = entry['section']['id']
            count = int(entry['count'])
            success_count = int(entry['success_count'])
            if _id in sum_record:
                sum_record[_id]['count'] += count
                sum_record[_id]['success_count'] += success_count
            else:
                sum_record[_id] = entry
                sum_record[_id]['count'] = count
                sum_record[_id]['success_count'] = success_count
    return sum_record


def get_tickets(cookies):
    url = f'{APIURL}/clasptickets'
    params = {'group': 'NGT48', 'limit': 100, 'status': 'all'}
    res = requests.get(url, cookies=cookies, params=params)
    try:
        return res.json()
    except JSONDecodeError as error:
        print(error)
        return res.text

def authentication(username, password):
    auth_url = f'{APIURL}/authentication'
    jsondata = f'{{"id": "{username}", "password": "{password}"}}'
    res = requests.get(auth_url)
    res = requests.put(auth_url, data=jsondata, cookies=res.cookies)
    return res.cookies
