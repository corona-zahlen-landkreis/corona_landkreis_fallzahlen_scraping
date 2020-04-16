from bs4 import BeautifulSoup

import requests
import datetime
import re

import locale
locale.setlocale(locale.LC_TIME, "de_DE.utf-8")

import scrape
import helper
from database_interface import *

main_url = "https://kreis-borken.de/de/"

req = scrape.request_url(main_url)
bs = BeautifulSoup(req.text, "html.parser")

cases_pattern = "insgesamt \d+ bestätigte Fälle"

text=bs.getText()

status_raw = re.findall("im Kreis Borken \(.*? Uhr",text)[0].replace("im Kreis Borken (","")
status= helper.get_status(status_raw)

cases_raw = re.findall(cases_pattern,text)[0]
cases = int(re.findall(r'[0-9]+', cases_raw)[0])

add_to_database("05554", status, cases, "Kreis Borken")
