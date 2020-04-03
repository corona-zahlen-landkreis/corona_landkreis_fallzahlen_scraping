from bs4 import BeautifulSoup

import requests
import datetime
import re
import locale

locale.setlocale(locale.LC_TIME, "de_DE.utf-8")

import scrape
from helper import *
from database_interface import *

main_url = "https://www.landkreis-mittelsachsen.de/corona.html"

req=scrape.request_url(main_url)
bs = BeautifulSoup(req.text, "html.parser")

text=bs.getText()

data = []


text_match = re.compile("Entwicklung der Erkrankungszahlen:")
text_position = bs.find(text=text_match)
table = text_position.findNext('table')
table_body = table.find('tbody')

rows = table_body.find_all('tr')
for row in rows:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    data.append([ele for ele in cols if ele]) # Get rid of empty values
    

status_raw = re.findall("\(\d+. \w+.*?2020\)",text)[0]
status_raw=remove_chars_from_text(status_raw,["(",")"])
status= get_status(status_raw)

cases = data[1][-1]
add_to_database("14522", status, cases, "Kreis Mittelsachsen")

