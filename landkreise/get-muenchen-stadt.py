from bs4 import BeautifulSoup

import requests
import datetime
import re

from database_interface import *

main_url = "https://www.muenchen.de/aktuell/2020-03/coronavirus-muenchen-infektion-aktueller-stand.html"

req = requests.get(main_url)
bs = BeautifulSoup(req.text, "html.parser")

status_pattern = "(.*) Das Referat .*"
cases_pattern = "[0-9|.]+ Infektionen"

text = bs.findAll(text=re.compile(status_pattern))[0]
status_raw = re.findall(status_pattern,text)[0]
status = datetime.datetime.strptime(status_raw, '(%d.%m.%Y)').strftime("%Y-%m-%d %H:%M:%S")

cases_raw = bs.find(text=re.compile(cases_pattern))
cases = int(re.findall(r'[0-9|.]+', cases_raw)[0].replace('.',''))

add_to_database(9162000, status, cases)
