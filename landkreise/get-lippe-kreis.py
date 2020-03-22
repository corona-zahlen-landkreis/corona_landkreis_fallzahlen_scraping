from bs4 import BeautifulSoup

import requests
import datetime
import re

import locale
locale.setlocale(locale.LC_TIME, "de_DE.utf-8")

from database_interface import *

main_url = "https://www.kreis-lippe.de/?object=tx|2001.7113.1&ModID=255&FID=2001.7113.1&La=1"

req = requests.get(main_url)
bs = BeautifulSoup(req.text, "html.parser")

cases_pattern = "Im Kreis Lippe gibt es insgesamt [0-9]+ bestätigte Coronafälle"

text=bs.getText()

status_raw = re.findall("Stand .*?\)",text)[0]
status= datetime.datetime.strptime(status_raw, 'Stand %d.%m.%Y)').strftime("%Y-%m-%d")

cases_raw = re.findall(cases_pattern,text)[0]
cases = int(re.findall(r'[0-9]+', cases_raw)[0])

add_to_database("05766", status, cases, "Kreis Lippe")
