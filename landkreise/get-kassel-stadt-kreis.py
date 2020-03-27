from bs4 import BeautifulSoup

import requests
import datetime
import re
import locale
locale.setlocale(locale.LC_TIME, "de_DE.utf-8")

import scrape
import helper
from database_interface import *

main_url = "https://www.kassel.de/aktuelles/aktuelle-meldungen/coronavirus.php"

req=scrape.request_url(main_url)
bs = BeautifulSoup(req.text, "html.parser")


data = []
table = bs.find('table')
table_body = table.find('tbody')

rows = table_body.find_all('tr')
for row in rows:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    data.append([ele for ele in cols if ele]) # Get rid of empty values
    

status_raw = re.findall("Stand: .* Uhr", bs.getText())[0]
status = helper.get_status(status_raw)

cases_stadt = data[0][1]
cases_kreis = data[1][1]

add_to_database("06611000", status, cases_stadt, "Stadt Kassel")
add_to_database("06633", status, cases_kreis, "Kreis Kassel")

