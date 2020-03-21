from bs4 import BeautifulSoup

import requests
import datetime
import re

from database_interface import *

main_url = "https://www.landkreis-goeppingen.de/start/_Aktuelles/coronavirus.html"

req=requests.get(main_url)
bs = BeautifulSoup(req.text, "html.parser")


cases_pattern = "Bestätigte Corona-Fälle im Landkreis Göppingen: [0-9]+"

status_raw = bs.findAll(text=re.compile("Stand "))[0]
status= datetime.datetime.strptime(status_raw, '(Stand %d.%m.%Y)').strftime("%Y-%m-%d")

cases_raw = bs.find(text=re.compile(cases_pattern))

cases = int(re.findall(r'[0-9]+', cases_raw)[0])

add_to_database("08117", status, cases)
