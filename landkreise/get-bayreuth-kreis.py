from bs4 import BeautifulSoup

import requests
import datetime
import re

import locale
locale.setlocale(locale.LC_TIME, "de_DE.utf-8")

import scrape
from helper import *
from database_interface import *

main_url = "https://www.landkreis-bayreuth.de/der-landkreis/pressemitteilungen/coronavirus-startseite/"

req = scrape.request_url(main_url)
bs = BeautifulSoup(req.text, "html.parser")

# note special char
cases_pattern = "\d+ Infektionen"

deaths_pattern = "\d+ Todesfälle"
healed_pattern = "davon [0-9]+ inzwischen wieder negativ."

text=bs.getText()
text=clear_text_of_ambigous_chars(text)


status_raw = re.findall("Stand .*? Uhr",text)[0]
status= get_status(status_raw)

cases_raw = re.findall(cases_pattern,text)[0]
cases = int(re.findall(r'[0-9]+', cases_raw)[0])

add_to_database("09472", status, cases, "Kreis Bayreuth")
