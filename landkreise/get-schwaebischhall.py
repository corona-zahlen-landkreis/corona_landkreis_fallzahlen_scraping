from bs4 import BeautifulSoup

import requests
import datetime
import re

import locale
locale.setlocale(locale.LC_TIME, "de_DE.utf-8")

from database_interface import *

main_url = "https://www.lrasha.de/index.php?id=953?&no_cache=1&publish[id]=1107342&publish[start]="

req = requests.get(main_url)
bs = BeautifulSoup(req.text, "html.parser")


cases_pattern = "haben wir aktuell [0-9]+"

#- Stand: Freitag, 20.03.2020, 18:45 Uhr -
status_raw = bs.findAll(text=re.compile("Stand:"))[0]
status= datetime.datetime.strptime(status_raw, '- Stand: %A, %d.%m.%Y, %H:%M Uhr -').strftime("%Y-%m-%d %H:%M:%S")



cases_raw = bs.find(text=re.compile(cases_pattern))
cases = int(re.findall(r'[0-9]+', cases_raw)[0])

add_to_database("Schwäbisch Hall", status, cases)
