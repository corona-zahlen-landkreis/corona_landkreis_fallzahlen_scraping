from bs4 import BeautifulSoup

import requests
import datetime
import re

import locale
locale.setlocale(locale.LC_TIME, "de_DE.utf-8")

from database_interface import *

main_url = "https://www.minden-luebbecke.de/Startseite/Informationen-zum-Coronavirus/index.php?La=1&object=tx,2832.3002.1&kat=&kuo=2&sub=0"

req = requests.get(main_url)
bs = BeautifulSoup(req.text, "html.parser")

cases_pattern = ""

text=bs.getText()

# non zero padded month
status_raw = re.findall("Stand .*? Uhr",text)[0]
status= datetime.datetime.strptime(status_raw, 'Stand %d. %B %Y, %H Uhr').strftime("%Y-%m-%d %H:%M")


cases_raw = re.findall(cases_pattern,text)[0]
cases = int(re.findall(r'[0-9]+', cases_raw)[0])

#add_to_database("Kreis Minden-Lübbecke", status, cases)
