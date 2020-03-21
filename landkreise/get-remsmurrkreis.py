from bs4 import BeautifulSoup

import requests
import datetime
import re

import locale
locale.setlocale(locale.LC_TIME, "de_DE.utf-8")

from database_interface import *

main_url = "https://www.rems-murr-kreis.de/jugend-gesundheit-soziales/gesundheit/coronavirus-aktuelle-informationen/"

req = requests.get(main_url)
bs = BeautifulSoup(req.text, "html.parser")

cases_pattern = "Bestätige Infektionen mit Coronavirus im Rems-Murr-Kreis: [0-9]+"

text=bs.getText()

# status month without leading zero
status_raw = re.findall("\([0-9]+.[0-9]+.[0-9]+, [0-9]+:[0-9]+ Uhr\)", text)[0]
status= datetime.datetime.strptime(status_raw, '(%d.%_m.%Y, %H:%M Uhr)').strftime("%Y-%m-%d %H:%M:%S")

print(status)

cases_raw = re.findall(cases_pattern,text)[0]
cases = int(re.findall(r'[0-9]+', cases_raw)[0])


#add_to_database("Rems-Murr-Kreis", status, cases)
