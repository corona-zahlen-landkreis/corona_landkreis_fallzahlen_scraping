from bs4 import BeautifulSoup

import requests
import datetime
import re


import helper
import scrape
import locale
locale.setlocale(locale.LC_TIME, "de_DE.utf-8")

from database_interface import *

main_url = "https://www.landkreis-freudenstadt.de/385534.html"

req = scrape.request_url(main_url)
bs = BeautifulSoup(req.text, "html.parser")

cases_pattern = "auf [0-9]+ erhöht"

text = helper.clear_text_of_ambigous_chars(bs.getText())

status_raw = re.findall("\([0-9]+.*\) eingegangenen", text)[0]
status= helper.get_status(status_raw)



cases_raw = re.findall(cases_pattern,bs.getText())[0]

cases = int(re.findall(r'[0-9]+', cases_raw)[0])

add_to_database("08237", status, cases, "Freudenstadt")
