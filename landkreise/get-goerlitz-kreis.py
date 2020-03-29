from bs4 import BeautifulSoup

import requests
import datetime
import re
import locale

locale.setlocale(locale.LC_TIME, "de_DE.utf-8")

import scrape
import helper
from database_interface import *

main_url = "https://www.kreis-goerlitz.de/city_info/webaccessibility/index.cfm?item_id=873097"

req=scrape.request_url(main_url)
bs = BeautifulSoup(req.text, "html.parser")

text=bs.getText()

data = []
table = bs.find('table')
table_body = table.find('tbody')

rows = table_body.find_all('tr')
for row in rows:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    if(cols[0] == 'Gesamtzahl der Infektionen'):
        data.append([ele for ele in cols if ele]) # Get rid of empty values
    

data=data[0]

status_raw = re.findall("Stand: .*?\)",text)[0]
status=helper.get_status(status_raw)

cases = int(data[1].split("m",1)[0])

add_to_database("14626", status, cases, "Kreis Goerlitz")
