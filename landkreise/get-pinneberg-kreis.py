from bs4 import BeautifulSoup

import requests
import datetime
import re

import locale
locale.setlocale(locale.LC_TIME, "de_DE.utf-8")

import helper
import scrape
from database_interface import *

main_url = "https://www.kreis-pinneberg.de/Coronavirus.html"

req = scrape.request_url(main_url)
bs = BeautifulSoup(req.text, "html.parser")

cases_pattern = "[0-9]+ Fälle"

text=bs.getText()

status_raw = re.findall("Stand.*Uhr",text)[0]
status= helper.get_status(status_raw)


cases_raw = re.findall(cases_pattern,text)[0]
cases = int(re.findall(r'[0-9]+', cases_raw)[0])

add_to_database("01056", status, cases, "Kreis Pinneberg")
