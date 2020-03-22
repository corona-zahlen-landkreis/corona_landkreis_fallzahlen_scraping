from bs4 import BeautifulSoup

import requests
import datetime
import re

from database_interface import *

main_url = "https://www.augsburg.de/umwelt-soziales/gesundheit/coronavirus"

req = requests.get(main_url)
bs = BeautifulSoup(req.text, "html.parser")

#(Stand 22.3.2020, 09:30 Uhr)
status_pattern = "Stand.*?Uhr"
cases_pattern = "aktuell.*?[0-9]+.*?COVID"

text = bs.findAll('div',{'class':'csc-default disturb-container'})[1].getText()

status_raw = re.findall(status_pattern,text)[0]
status = datetime.datetime.strptime(status_raw, 'Stand %d.%m.%Y, %H:%M Uhr').strftime("%Y-%m-%d %H:%M:%S")

cases_raw = re.findall(cases_pattern, text)[0]
cases = int(re.findall(r'[0-9]+', cases_raw)[0])

add_to_database("09761", status, cases, "Stadt Augsburg")
