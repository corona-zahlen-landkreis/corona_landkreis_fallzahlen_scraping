from bs4 import BeautifulSoup

import requests
from datetime import date
import re

from helper import *
import scrape
from database_interface import *

main_url = "https://www.bodenseekreis.de/de/soziales-gesundheit/gesundheit/infektionsschutz/infektionskrankheiten/corona-virus/"

req = scrape.request_url(main_url)
bs = BeautifulSoup(req.text, "html.parser")

text = bs.getText()
# todo no status date, check if datapoint is present in database 
#status_raw = bs.findAll(text=re.compile("Stand:"))[0]
#status= datetime.datetime.strptime(status_raw, 'Stand: %d.%m.%Y, %H:%M Uhr').strftime("%Y-%m-%d %H:%M:%S")
status = date.today().strftime('%Y-%m-%d')


cases_raw= re.findall("Labordiagnostisch bestätigte Infektion.*?\d+",text)[0]
cases = get_number_only(cases_raw)

add_to_database("08435", status, cases, name="Bodenseekreis")
