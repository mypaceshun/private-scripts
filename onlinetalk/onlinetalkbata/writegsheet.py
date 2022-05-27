'''
Write Google Spread Sheet
'''
import os
from datetime import datetime
from pathlib import Path

import gspread
from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials

from onlinetalkbata.ngt48cdshop import (DATE_FORMAT, authentication,
                                        filter_tickets, get_tickets,
                                        sum_tickets)

load_dotenv()

USERNAME = os.environ.get('NGT48CD_USERNAME', 'username')
PASSWORD = os.environ.get('NGT48CD_PASSWORD', 'password')
START_DATE = os.environ.get('NGT48CD_START_DATE', None)
END_DATE = os.environ.get('NGT48CD_END_DATE', None)
SECRET_JSON_FILE = os.environ.get(
    "GOOGLE_APPLICATION_CREDENTIALS", "secret.json")
SHEET_ID = os.environ.get("GOOGLE_SPREADSHEET_ID", "sheetid")

SIGLE_DATELIST = [['20201120', '20201231', '5thシングル(シャーベットピンク)'],
                  ['20210601', '20211031', '6thシングル(Awesome)'],
                  ['20220101', '20220430', '7thシングル(ポンコツな君が好きだ)'],
                  ['20220701', '20221001', '1stアルバム'], ]


def get_spreadsheets_obj(json_key_file, sheetid):
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    cred = ServiceAccountCredentials.from_json_keyfile_name(
        json_key_file, scope)
    gc = gspread.authorize(cred)
    worksheet = gc.open_by_key(sheetid)
    return worksheet


def get_ticket_data(start=None, end=None):
    cookies = authentication(USERNAME, PASSWORD)
    tickets = get_tickets(cookies)
    if start is None:
        start = datetime(2020, 1, 1)
    query = {
        "start_date": start,
    }
    tickets = filter_tickets(tickets, query)
    tickets = sum_tickets(tickets)
    return tickets


def write_gsheet(gsheets, tickets, title):
    sheet = None
    try:
        sheet = gsheets.worksheet(title)
    except gspread.exceptions.WorksheetNotFound:
        gsheets.add_worksheet(title=title, rows="300", cols="20")
        sheet = gsheets.worksheet(title)
    headers = [['日付', 'メンバー名', '部数', '当選枚数', '応募枚数']]
    sheet.update(f'A1', headers)
    sheet.update(
        f'F1', f"最終更新時刻 {datetime.now().strftime('%Y/%m/%d %H:%M:%S')}")
    length = len(tickets)
    range = f"A2:E{length+2}"
    celldata = []
    keys = [int(k) for k in tickets.keys()]
    keys = [str(k) for k in sorted(keys)]
    for _id in keys:
        member = tickets[_id]['member']
        bu = tickets[_id]['section']['name']
        count = tickets[_id]['count']
        success_count = tickets[_id]['success_count']
        date = tickets[_id]['date']
        celldata.append([date, member, bu, success_count, count])
    sheet.update(range, celldata)


def main():
    secret_json_path = Path(SECRET_JSON_FILE).expanduser()
    sheets = get_spreadsheets_obj(secret_json_path, SHEET_ID)
    for singledate in SIGLE_DATELIST:
        start = datetime.strptime(singledate[0], DATE_FORMAT)
        end = datetime.strptime(singledate[1], DATE_FORMAT)
        title = singledate[2]
        tickets = get_ticket_data(start, end)
        write_gsheet(sheets, tickets, title)


if __name__ == '__main__':
    main()
