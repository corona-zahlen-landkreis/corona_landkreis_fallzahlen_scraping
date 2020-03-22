from bs4 import BeautifulSoup

import requests
import datetime
import re

import locale
locale.setlocale(locale.LC_TIME, "de_DE.utf-8")

from database_interface import *

main_url = "https://www.enzkreis.de/Quicknavigation/Start/Gesundheitsamt-informiert-%C3%BCber-das-neue-Coronavirus-SARS-CoV-2-Fast-50-best%C3%A4tigte-F%C3%A4lle-in-Pforzheim-und-im-Enzkreis.php?object=tx,2891.6&ModID=7&FID=2891.1978.1"

req = requests.get(main_url)
bs = BeautifulSoup(req.text, "html.parser")

cases_pforzheim_pattern = "Aktuell gibt es in Pforzheim [0-9]+ bestätigte Corona-Fälle"
cases_enzkreis_pattern = "im Enzkreis [0-9]+"

text=bs.getText()

status_raw = re.findall("Stand: .* Uhr\)", text)[0]
status= datetime.datetime.strptime(status_raw, 'Stand: %d.%m.%Y, %H:%M Uhr)').strftime("%Y-%m-%d %H:%M:%S")


cases_pforzheim_raw = re.findall(cases_pforzheim_pattern,text)[0]
cases_pforzheim = int(re.findall(r'[0-9]+', cases_pforzheim_raw)[0])

cases_enzkreis_raw = re.findall(cases_enzkreis_pattern,text)[0]
cases_enzkreis = int(re.findall(r'[0-9]+', cases_enzkreis_raw)[0])


add_to_database("08231", status, cases_pforzheim, "Pforzheim")
add_to_database("08236", status, cases_enzkreis, "Enzkreis")
