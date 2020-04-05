from bs4 import BeautifulSoup

import requests
import datetime
import re

import scrape
from helper import *
from database_interface import *

# (Labordiagnostisch bestätigt, Stand 21.03.2020)

url = "https://www.segeberg.de/Quicknavigation/Startseite"

req = scrape.request_url(url)
bs = BeautifulSoup(req.text, "html.parser")

prefix = "FÄLLE IM KREIS SEGEBERG: \d+"
prefix_date = "Stand.*\)"

text=bs.getText()

status_raw = re.findall(prefix_date,text)[0].replace(")","")
status = get_status(status_raw)

cases_raw = re.findall(prefix,text)[0]
cases = get_number_only(cases_raw)

add_to_database("01060", status, cases, name="Kreis Segeberg")



