from bs4 import BeautifulSoup

import requests
import datetime
import re

from database_interface import *

main_url = "https://www.info-corona-lrahdh.de/startseite"

req = requests.get(main_url)
bs = BeautifulSoup(req.text, "html.parser")

status_pattern = re.compile(r'.*Stand: .*')
cases_pattern = re.compile(r'.*Es gibt aktuell.*')


# Aktuelle Informationen zum Coronavirus (Stand: 18.03.2020, 12:00 Uhr)
status_raw = bs.findAll(text=re.compile("Stand"))[0]
status= datetime.datetime.strptime(status_raw, 'Aktuelle Informationen zum Coronavirus (Stand: %d.%m.%Y, %H:%M Uhr)').strftime("%Y-%m-%d %H:%M:%S")


cases_raw=bs.findAll(text=re.compile("Es gibt aktuell"))[0]
cases = int(re.findall(r'[0-9]+', cases_raw)[0])


add_to_database("08135", status, cases)
