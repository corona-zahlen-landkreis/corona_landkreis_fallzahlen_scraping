from bs4 import BeautifulSoup

import requests
import datetime
import re

import scrape
from helper import *
from database_interface import *

main_url = "https://www.muenchen.de/aktuell/2020-03/coronavirus-muenchen-infektion-aktueller-stand.html"

req = scrape.request_url(main_url)
bs = BeautifulSoup(req.text, "html.parser")
raw_text=bs.getText()

status_pattern = "(.*) Das Referat .*"
cases_pattern = "insgesamt.*?[0-9|.]+.*?Infektionen"

text = bs.findAll(text=re.compile(status_pattern))[0]
status_raw = re.findall(status_pattern,text)[0].replace("(","").replace(")","")
status = get_status(status_raw)

cases_raw = bs.findAll(text=re.compile(cases_pattern))[0].replace('.','')
cases = int(re.findall(r'[0-9|.]+', cases_raw)[0])

add_to_database("09162000", status, cases, "Stadt München")
