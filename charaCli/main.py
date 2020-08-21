import os
import re
import datetime
from dotenv import load_dotenv
from tqdm import tqdm
from texttable import Texttable
from pychara.session import Session

load_dotenv()

USERNAME = os.environ.get('CHARACLI_USERNAME', 'username')
PASSWORD = os.environ.get('CHARACLI_PASSWORD', 'password')
PAGENUM = int(os.environ.get('CHARACLI_PAGENUM', 10))

AFTER_TODAY = os.environ.get('CHARACLI_AFTER_TODAY', False) == 'True'  # 今日以降のみ出力
ONLY_HIT = os.environ.get('CHARACLI_ONLY_HIT', False) == 'True'  # 当選のみ出力


def main():
    s = Session()
    s.login(USERNAME, PASSWORD)
    items = []
    for i in tqdm(range(1, PAGENUM+1)):
        items += s.fetch_apply_list(page=i)

    items = id_rewrite(items)
    items = generate_bu(items)
    items = sum_id(items)
    items = replace_date(items)
    items = filter_items(items)
    output(items)

def output(items):
    '''
    いい感じに出力する
    '''
    def _key(x):
        return x['date'].strftime('%Y%m%D') + str(x['bu'])
    sorted_items = sorted(items, key=_key)
    table = Texttable()
    table.add_row(['name', 'num', 'status'])
    for item in sorted_items:
        row = [item['name'], f"{item['num']}枚", item['status']]
        table.add_row(row)
    print(table.draw())

def filter_items(items):
    _items = []
    _today = datetime.datetime.today()
    for item in items:
        if AFTER_TODAY and item['date'] < _today:
            continue
        if ONLY_HIT and item['status_code'] != 0:
            continue
        _items.append(item)
    return _items

def replace_date(items):
    pattern = '[\d/]*'
    repattern = re.compile(pattern)

    format = '%m/%d'

    result_list = []
    for item in items:
        res = repattern.match(item['name'])
        apply_date = item['date']
        date_str = res.group()
        date = datetime.datetime.strptime(date_str, format)
        date = date.replace(year=apply_date.year)
        if date < apply_date:
            date = date.replace(year=apply_date.year+1)
        item['date'] = date
        result_list.append(item)
    return result_list


def sum_id(items):
    '''
    idごとに枚数を集計する
    '''
    result = {}
    for item in items:
        id = item['id']
        if id in result:
            result[id]['num'] += item['num']
            result[id]['total_money'] += item['total_money']
        else:
            result[id] = item
    apply_list = []
    for id in result:
        apply_list.append(result[id])
    return apply_list

def generate_bu(items):
    '''
    部を追加
    '''
    pattern = '.*第(\d)部.*'
    repattern = re.compile(pattern)
    _items = []
    for d in items:
        result = repattern.match(d['name'])
        if result is None:
            print('{} is not found bu'.format(d['name']))
        else:
            d['bu'] = int(result.group(1))
            _items.append(d)
    return _items


def id_rewrite(items):
    '''
    抽選状況ごとに分別するためにidの後ろにstatus_codeを付ける
    '''
    for item in items:
        id = item['id']
        status_code = item['status_code']
        id += str(status_code)
        item['id'] = id
    return items

if __name__ == '__main__':
    main()
