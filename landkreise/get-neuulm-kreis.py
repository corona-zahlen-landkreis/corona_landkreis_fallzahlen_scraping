from bs4 import BeautifulSoup

import requests
import datetime
import re

import locale
locale.setlocale(locale.LC_TIME, "de_DE.utf-8")

import scrape
from helper import *
from database_interface import *

main_url = "https://landkreis.neu-ulm.de/de/aktuelles-detail/insgesamt-18-faelle-fuer-eine-coronavirus-erkrankung-im-landkreis-neu-ulm-gemeldet.html"

req = scrape.request_url(main_url)
bs = BeautifulSoup(req.text, "html.parser")

cases_pattern = "(?:Insgesamt [0-9]+ Fälle für)|(\d+ Personen im Landkreis)"

text=bs.getText()

status_raw = re.findall("Stand .*? Uhr",text)[0]
status= get_status(status_raw)

cases_raw = re.findall(cases_pattern,text)[0]
cases = int(re.findall(r'[0-9]+', cases_raw)[0])

add_to_database("09775", status, cases, "Kreis Neuulm")
