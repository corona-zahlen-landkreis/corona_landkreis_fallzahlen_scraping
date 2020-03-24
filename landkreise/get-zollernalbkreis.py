from bs4 import BeautifulSoup

import requests
import datetime
import re

from database_interface import *

main_url = "https://www.zollernalbkreis.de/aktuelles/nachrichten/antworten+auf+haeufig+gestellte+fragen+zum+neuartigen+coronavirus"

req = requests.get(main_url)
bs = BeautifulSoup(req.text, "html.parser")

text=bs.getText()

#Gesamtzahl der an dem Coronavirus-Infizierten im Zollernalbkreis: 76 (
cases_pattern = "Gesamtzahl der an dem Coronavirus-Infizierten im Zollernalbkreis: [0-9]+"

status_raw = bs.findAll(text=re.compile("Stand:"))[0]
status= datetime.datetime.strptime(status_raw, '(Stand: %d.%m.%Y, %H.%M Uhr)').strftime("%Y-%m-%d %H:%M:%S")


cases_raw=re.findall(cases_pattern, text)[0]
cases = int(re.findall(r'[0-9]+', cases_raw)[0])

add_to_database("08417", status, cases, "Zollernalbkreis")
