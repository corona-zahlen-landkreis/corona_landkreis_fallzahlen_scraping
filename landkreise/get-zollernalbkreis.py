from bs4 import BeautifulSoup

import requests
import datetime
import re

from database_interface import *

main_url = "https://www.zollernalbkreis.de/aktuelles/nachrichten/antworten+auf+haeufig+gestellte+fragen+zum+neuartigen+coronavirus"

req = requests.get(main_url)
bs = BeautifulSoup(req.text, "html.parser")


#Gesamtzahl der an dem Coronavirus-Infizierten im Zollernalbkreis: 76 (
cases_pattern = "Gesamtzahl der an dem Coronavirus-Infizierten im Zollernalbkreis: [0-9]+ \("

status_raw = bs.findAll(text=re.compile("Stand:"))[0]
status= datetime.datetime.strptime(status_raw, '(Stand: %d.%m.%Y, %H Uhr)').strftime("%Y-%m-%d %H:00:00")


cases_raw=re.findall(cases_pattern, bs.find('div', {"id": "boxid16843898"}).getText() )[0]
cases = int(re.findall(r'[0-9]+', cases_raw)[0])

add_to_database("Zollernalbkreis", status, cases)
