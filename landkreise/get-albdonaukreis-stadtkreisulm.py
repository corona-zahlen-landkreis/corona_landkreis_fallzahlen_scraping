from bs4 import BeautifulSoup

import requests
import datetime
import re

import scrape
import helper
from database_interface import *

main_url = "https://www.alb-donau-kreis.de/alb-donau-kreis/startseite/dienstleistungen+service/coronavirus.html"

req = scrape.request_url(main_url)
bs = BeautifulSoup(req.text, "html.parser")

text=bs.getText()
status_raw = re.findall("Stand:.*?Uhr",text)[0]
status= helper.get_status(status_raw)

cases_raw=bs.findAll(text=re.compile("Alb-Donau-Kreis \("))[0]
cases = int(re.findall(r'[0-9]+', cases_raw)[2])


add_to_database("08425", status, cases, "Alb-Donau-Kreis")


cases_ulm_raw=bs.findAll(text=re.compile("Stadtkreis Ulm \("))[0]
cases_ulm = int(re.findall(r'[0-9]+', cases_ulm_raw)[2])


add_to_database("08421000", status, cases_ulm, "Stadtkreis Ulm")

