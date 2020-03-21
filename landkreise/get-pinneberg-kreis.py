from bs4 import BeautifulSoup

import requests
import datetime
import re

import locale
locale.setlocale(locale.LC_TIME, "de_DE.utf-8")

from database_interface import *

main_url = "https://www.kreis-pinneberg.de/Coronavirus.html"

req = requests.get(main_url)
bs = BeautifulSoup(req.text, "html.parser")

cases_pattern = "[0-9]+ Fälle"

text=bs.getText()

status_raw = re.findall("Stand .* Uhr",text)[0]
status= datetime.datetime.strptime(status_raw, 'Stand %d.%m.%Y; %H:%M Uhr').strftime("%Y-%m-%d %H:%M")


cases_raw = re.findall(cases_pattern,text)[0]
cases = int(re.findall(r'[0-9]+', cases_raw)[0])

add_to_database("Kreis Pinneberg", status, cases)
