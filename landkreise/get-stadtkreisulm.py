from bs4 import BeautifulSoup

import requests
import datetime
import re

from database_interface import *

# yes, that url is  correct. 
main_url = "https://www.alb-donau-kreis.de/alb-donau-kreis/startseite/dienstleistungen+service/coronavirus.html"

req = requests.get(main_url)
bs = BeautifulSoup(req.text, "html.parser")

status_raw = bs.findAll(text=re.compile("Stand:"))[0]
status= datetime.datetime.strptime(status_raw, 'Stand: %d.%m.%Y, %H Uhr').strftime("%Y-%m-%d %H:%M:%S")

cases_raw=bs.findAll(text=re.compile("Stadtkreis Ulm \("))[0]
cases = int(re.findall(r'[0-9]+', cases_raw)[2])


add_to_database("08421000", status, cases, "Stadtkreis Ulm")
