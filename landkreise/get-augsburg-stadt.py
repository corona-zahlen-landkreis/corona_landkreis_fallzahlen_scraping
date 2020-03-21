from bs4 import BeautifulSoup

import requests
import datetime
import re

from database_interface import *

main_url = "https://www.augsburg.de/umwelt-soziales/gesundheit/coronavirus"

req = requests.get(main_url)
bs = BeautifulSoup(req.text, "html.parser")

status_pattern = "Stand .* Uhr"
cases_pattern = "[0-9]+ COVID-19-Fälle"

text = bs.findAll(text=re.compile(status_pattern))[0]
status_raw = re.findall(status_pattern,text)[0]
status = datetime.datetime.strptime(status_raw, 'Stand %d.%m.%Y, %H:%M Uhr').strftime("%Y-%m-%d %H:%M:%S")

cases_raw = bs.find(text=re.compile(cases_pattern))
cases = int(re.findall(r'[0-9]+', cases_raw)[0])

add_to_database(9761, status, cases)
