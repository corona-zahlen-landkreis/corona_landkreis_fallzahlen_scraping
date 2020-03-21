from bs4 import BeautifulSoup

import requests
import datetime
import re

import locale
locale.setlocale(locale.LC_TIME, "de_DE.utf-8")

from database_interface import *

main_url = "https://www.kreis-paderborn.de/kreis_paderborn/aktuelles/pressemitteilungen/Informationen-zu-Coronaviren.php"

req = requests.get(main_url)
bs = BeautifulSoup(req.text, "html.parser")

cases_pattern = "sind insgesamt [0-9]+ Menschen positiv auf eine Co"

text=bs.getText()

# note special space
status_raw = re.findall("Stand: .*? Uhr",text)[0]
status= datetime.datetime.strptime(status_raw, 'Stand: %A, %d.%m.%Y -  %H:%M Uhr').strftime("%Y-%m-%d %H:%M")


cases_raw = re.findall(cases_pattern,text)[0]
cases = int(re.findall(r'[0-9]+', cases_raw)[0])

add_to_database("05774", status, cases)
