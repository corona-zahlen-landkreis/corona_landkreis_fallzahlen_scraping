from bs4 import BeautifulSoup

import requests
import datetime
import re

import locale
locale.setlocale(locale.LC_TIME, "de_DE.utf-8")

from database_interface import *

main_url = "https://www.burgenlandkreis.de/de/quicklinks/corona-virus-aktuelle-entwicklung-20049167.html"

req = requests.get(main_url)
bs = BeautifulSoup(req.text, "html.parser")

# note special char
cases_pattern = "Anzahl der Infizierten insgesamt: [0-9]+"

text=bs.getText()


status_raw = re.findall("Update vom .*? Uhr",text)[0]
status= datetime.datetime.strptime(status_raw, 'Update vom %d.%m.%Y, %H.%M Uhr').strftime("%Y-%m-%d %H:%M")

cases_raw = re.findall(cases_pattern,text)[0]
cases = int(re.findall(r'[0-9]+', cases_raw)[0])

add_to_database("15084", status, cases)
