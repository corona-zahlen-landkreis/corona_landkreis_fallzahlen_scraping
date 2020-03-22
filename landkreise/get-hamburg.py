from bs4 import BeautifulSoup

import requests
import datetime
import re

import locale
locale.setlocale(locale.LC_TIME, "de_DE.utf-8")

from database_interface import *

main_url = "https://www.hamburg.de/coronavirus/"

req = requests.get(main_url)
bs = BeautifulSoup(req.text, "html.parser")

text=bs.getText()

status_raw = re.findall("Stand: .*? 2020",text)[0]
status= datetime.datetime.strptime(status_raw, 'Stand: %A, %d. %B %Y').strftime("%Y-%m-%d")

cases_raw = bs.find('h2',{'class':'c_chart_h2'}).getText()
cases = int(re.findall(r'[0-9]+', cases_raw)[0])

add_to_database("02000000", status, cases, "Hamburg")
