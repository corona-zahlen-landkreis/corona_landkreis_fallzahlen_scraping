from bs4 import BeautifulSoup

import requests
import datetime
import re
import locale

locale.setlocale(locale.LC_TIME, "de_DE.utf-8")
import helper

from database_interface import *

main_url = "https://www.landkreis-leer.de/Leben-Lernen/Coronavirus"

req=requests.get(main_url)
bs = BeautifulSoup(req.text, "html.parser")


table = bs.find('table',{"data-bordercolor":"#949292"})

data = helper.get_table(table)

status_raw = re.findall("\(Stand .*? Uhr",bs.text)[0]
status= datetime.datetime.strptime(status_raw, '(Stand %d. %B, %H.%M Uhr').strftime("2020-%m-%d %H:%M")

cases_total = int(data[13][1])

# todo hier wird auch noch die gemeindeebene untersützt

add_to_database("03457", status, cases_total, "Kreis Leer")

