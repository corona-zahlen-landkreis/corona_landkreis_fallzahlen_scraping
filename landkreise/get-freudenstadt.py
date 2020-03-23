from bs4 import BeautifulSoup

import requests
import datetime
import re

from dateparser.search import search_dates
import helper

import locale
locale.setlocale(locale.LC_TIME, "de_DE.utf-8")

from database_interface import *

main_url = "https://www.landkreis-freudenstadt.de/385534.html"

req = requests.get(main_url)
bs = BeautifulSoup(req.text, "html.parser")

cases_pattern = "auf [0-9]+ erhöht"

text = helper.clear_text_of_ambigous_chars(bs.getText())

status_raw = re.findall("\([0-9]+.*Uhr\)", text)[0]
status= datetime.datetime.strptime(status_raw, '(%d. %B, %H Uhr)').strftime("2020-%m-%d")



cases_raw = re.findall(cases_pattern,bs.getText())[0]

cases = int(re.findall(r'[0-9]+', cases_raw)[0])

add_to_database("08237", status, cases, "Freudenstadt")
