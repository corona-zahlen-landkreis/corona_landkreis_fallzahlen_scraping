from bs4 import BeautifulSoup

import requests
import datetime
import re

import scrape
from helper import *
from database_interface import *

main_url = "https://www.landkreis-goeppingen.de/start/_Aktuelles/coronavirus.html"

req=scrape.request_url(main_url)
bs = BeautifulSoup(req.text, "html.parser")

text=bs.getText()
text=clear_text_of_ambigous_chars(text)
text=remove_chars_from_text(text,["\n"])

cases_pattern = "Bestätigte Corona-Fälle: \d+"

status_raw = re.findall("Stand: .*? Uhr",text)[0]
status = get_status(status_raw)

cases_raw = bs.find(text=re.compile(cases_pattern))

cases = int(re.findall(r'[0-9]+', cases_raw)[0])

add_to_database("08117", status, cases, "Kreis Göppingen")
