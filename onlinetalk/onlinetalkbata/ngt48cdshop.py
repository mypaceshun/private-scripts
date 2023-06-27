import os
from datetime import datetime
from json.decoder import JSONDecodeError
from pprint import pprint

import requests
from dotenv import load_dotenv

load_dotenv()

DATE_FORMAT = '%Y%m%d'
START_DATE = os.environ.get('NGT48CD_START_DATE', None)
AFTER_TODAY = os.environ.get(
    'NGT48CD_AFTER_TODAY', 'False').lower() == 'True'.lower()
FORMAT = os.environ.get('NGT48CD_FORMAT', 'text')

BASEURL = 'https://ngt48cd.shop'
APIURL = f'{BASEURL}/api/v1'


def main():
    username = os.environ.get('NGT48CD_USERNAME', 'username')
    password = os.environ.get('NGT48CD_PASSWORD', 'password')
    cookies = authentication(username, password)
    tickets = get_tickets(cookies)
    query = {
        'after_today': False,
        'start_date': datetime(2000, 1, 1)
    }
    if AFTER_TODAY:
        query['after_today'] = AFTER_TODAY
    if START_DATE is not None:
        start_date = datetime.strptime(START_DATE, DATE_FORMAT)
        query['start_date'] = start_date
    print(query)
    tickets = filter_tickets(tickets, query)
    tickets = sum_tickets(tickets)
    keys = [int(k) for k in tickets.keys()]
    keys = [str(k) for k in sorted(keys)]
    if FORMAT == 'csv':
        print_csv(tickets, keys)
    else:
        print_text(tickets, keys)


def print_text(tickets, keys):
    total = 0
    stotal = 0
    ftotal = 0
    ltotal = 0
    for _id in keys:
        member = tickets[_id]['member']
        bu = tickets[_id]['section']['name']
        count = tickets[_id]['count']
        success_count = tickets[_id]['success_count']
        failur_count = tickets[_id]['failur_count']
        lottery_count = tickets[_id]['lottery_count']
        date = tickets[_id]['date']
        row = f'{date} {member} {bu}: {success_count:2} / {failur_count:2} / {lottery_count:2}'
        print(row)
        total += count
        stotal += success_count
        ftotal += failur_count
        ltotal += lottery_count
    print(f'success: {stotal:4}, failur: {ftotal:4}, lottery: {ltotal:4}')


def print_csv(tickets, keys):
    for _id in keys:
        member = tickets[_id]['member']
        bu = tickets[_id]['section']['name']
        count = tickets[_id]['count']
        success_count = tickets[_id]['success_count']
        date = tickets[_id]['date']
        row = f'{date},{member},{bu},{success_count},{count}'
        print(row)


def filter_tickets(tickets, query):
    for one_apply in tickets:
        entries = one_apply['entry']
        _entries = []
        start_date = datetime(2000, 1, 1)
        end_date = datetime(2100, 1, 1)
        if 'start_date' in query:
            start_date = query['start_date']
        if 'end_date' in query:
            end_date = query['end_date']
        if 'after_today' in query and query['after_today']:
            start_date = datetime.today()
        for entry in entries:
            datestr = entry['date']
            date = datetime.strptime(datestr, '%Y-%m-%d')
            if start_date <= date and date <= end_date:
                _entries.append(entry)
        one_apply['entry'] = _entries
    return tickets


def sum_tickets(tickets):
    sum_record = {}
    for one_apply in tickets:
        lottery_id = int(one_apply['clasp']['lottery']['id'])
        # 未抽選 lottery_id=0
        # 抽選済み lottery_id=2
        entries = one_apply['entry']
        for entry in entries:
            _id = entry['section']['id']
            count = int(entry['count'])
            success_count = int(entry['success_count'])
            if _id not in sum_record:
                sum_record[_id] = entry
                sum_record[_id]['count'] = 0
                sum_record[_id]['success_count'] = 0
                sum_record[_id]['failur_count'] = 0
                sum_record[_id]['lottery_count'] = 0
            sum_record[_id]['count'] += count
            sum_record[_id]['success_count'] += success_count
            diff_count = count - success_count
            if lottery_id == 0:  # 未抽選
                sum_record[_id]['lottery_count'] += diff_count
            else:  # 抽選済み
                sum_record[_id]['failur_count'] += diff_count
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
