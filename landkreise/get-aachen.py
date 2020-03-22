from bs4 import BeautifulSoup

import requests
import datetime
import re

import locale
locale.setlocale(locale.LC_TIME, "de_DE.utf-8")

from database_interface import *

main_url = "http://www.aachen.de/DE/stadt_buerger/notfall_informationen/corona/aktuelles/index.html"

req = requests.get(main_url)
bs = BeautifulSoup(req.text, "html.parser")

# note special char
cases_aachen_pattern = "davon [0-9]+ in der Stadt Aachen"
cases_staedteregion_pattern = "Aktuell [0-9]+ bestätigte Coronafälle in der StädteRegion Aachen"

text=bs.getText()


status_raw = re.findall("zum Corona-Virus; .*? Uhr",text)[0]
status= datetime.datetime.strptime(status_raw, 'zum Corona-Virus; %A, %d.%m., %H.%M Uhr').strftime("2020-%m-%d %H:%M")

cases_aachen_raw = re.findall(cases_aachen_pattern,text)[0]
cases_aachen = int(re.findall(r'[0-9]+', cases_aachen_raw)[0])

cases_staedteregion_raw  = re.findall(cases_staedteregion_pattern,text)[0]
cases_staedteregion = int(re.findall(r'[0-9]+', cases_staedteregion_raw)[0])

add_to_database("05334002", status, cases_aachen, "Stadt Aachen")
add_to_database("05334", status, cases_staedteregion, "Staedregion Aachen")
