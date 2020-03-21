from bs4 import BeautifulSoup

import requests
import datetime
import re

import locale
locale.setlocale(locale.LC_TIME, "de_DE.utf-8")

from database_interface import *

main_url = "https://www.kreis-reutlingen.de/de/Aktuelles/Landkreis-aktuell/Landkreis-aktuell?view=publish&item=article&id=1923"

req = requests.get(main_url)
bs = BeautifulSoup(req.text, "html.parser")

cases_pattern = "Gesamtzahl laborbestätigter Fälle: [0-9]+"

text=bs.getText()

status_raw = re.findall("Stand: .*2020", text)[0]
status= datetime.datetime.strptime(status_raw, 'Stand: %d.%m.%Y').strftime("%Y-%m-%d")

cases_raw = re.findall(cases_pattern,text)[0]
cases = int(re.findall(r'[0-9]+', cases_raw)[0])

add_to_database(08415, status, cases)
