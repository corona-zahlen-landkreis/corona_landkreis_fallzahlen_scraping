from bs4 import BeautifulSoup

import requests
import datetime
import re

import locale
locale.setlocale(locale.LC_TIME, "de_DE.utf-8")

import scrape
import helper
from database_interface import *

main_url = "https://www.rhein-neckar-kreis.de/,Lde/start/landratsamt/coronavirus+-+faq.html"

req = scrape.request_url(main_url)
bs = BeautifulSoup(req.text, "html.parser")

text_loc = bs.find('h3',text="Aktuelle Fallzahlen aus dem Rhein-Neckar-Kreis")
#,{'class':'basecontent-line-break-text'})
text = text_loc.findNext('div').getText()
text = text.replace("\n", " ")

cases_rheinneckarkreis_pattern = "Rhein-Neckar-Kreis beträgt die Zahl der positiv getesteten Personen [0-9]+"
cases_heidelberg_pattern = "im Stadtgebiet Heidelberg [0-9]+"

cases_rheinneckarkreis_raw = re.findall(cases_rheinneckarkreis_pattern,text)[0]
cases_rheinneckarkreis = int(re.findall(r'[0-9]+', cases_rheinneckarkreis_raw)[0])

cases_heidelberg_raw = re.findall(cases_heidelberg_pattern,text)[0]
cases_heidelberg = int(re.findall(r'[0-9]+', cases_heidelberg_raw)[0])




status_raw = re.findall("Stand: .* 2020", text)[0]
status= datetime.datetime.strptime(status_raw, 'Stand: %d. %B %Y').strftime("%Y-%m-%d")

#print(cases_heidelberg_pattern)
#print(cases_rheinneckarkreis)
#print(status)

add_to_database("08226", status, cases_rheinneckarkreis, "Rhein-Neckar-Kreis")
add_to_database("08221000", status, cases_heidelberg, "Heidelberg")

