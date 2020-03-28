from bs4 import BeautifulSoup

import requests
import datetime
import re

import scrape
import helper
from database_interface import *

main_url = "https://www.landkreis-goeppingen.de/start/_Aktuelles/coronavirus.html"

req=scrape.request_url(main_url)
bs = BeautifulSoup(req.text, "html.parser")


cases_pattern = "Bestätigte Corona-Fälle im Landkreis Göppingen: [0-9]+"

status_raw = bs.findAll(text=re.compile("Stand "))[0]
status = helper.get_status(status_raw)

cases_raw = bs.find(text=re.compile(cases_pattern))

cases = int(re.findall(r'[0-9]+', cases_raw)[0])

add_to_database("08117", status, cases, "Kreis Göppingen")
