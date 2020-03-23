from bs4 import BeautifulSoup

import requests
import datetime
import re

import locale
locale.setlocale(locale.LC_TIME, "de_DE.utf-8")

from database_interface import *

main_url = "https://www.landkreis-bayreuth.de/der-landkreis/pressemitteilungen/coronavirus-startseite/"

req = requests.get(main_url)
bs = BeautifulSoup(req.text, "html.parser")

# note special char
cases_pattern = "[0-9]+ positiv getestete Fälle"
healed_pattern = "davon [0-9]+ inzwischen wieder negativ."

text=bs.getText()


status_raw = re.findall("Stand .*? Uhr",text)[0]
status= datetime.datetime.strptime(status_raw, 'Stand %d.%m., %H:%M Uhr').strftime("2020-%m-%d %H:%M")

cases_raw = re.findall(cases_pattern,text)[0]
cases = int(re.findall(r'[0-9]+', cases_raw)[0])

add_to_database("09472", status, cases, "Kreis Bayreuth")
