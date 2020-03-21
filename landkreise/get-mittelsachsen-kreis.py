from bs4 import BeautifulSoup

import requests
import datetime
import re
import locale

locale.setlocale(locale.LC_TIME, "de_DE.utf-8")

from database_interface import *

main_url = "https://www.landkreis-mittelsachsen.de/corona.html"

req=requests.get(main_url)
bs = BeautifulSoup(req.text, "html.parser")

text=bs.getText()

data = []
table = bs.find('table', attrs={'class':'contenttable'})
table_body = table.find('tbody')

rows = table_body.find_all('tr')
for row in rows:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    data.append([ele for ele in cols if ele]) # Get rid of empty values
    

status_raw = re.findall("Stand .*? 2020",text)[0].replace("\xa0", " ")
# note special space
status= datetime.datetime.strptime(status_raw, 'Stand %d. %B %Y').strftime("%Y-%m-%d")

cases = data[1][-1]
add_to_database(14522, status, cases)

