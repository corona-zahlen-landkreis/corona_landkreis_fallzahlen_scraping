from bs4 import BeautifulSoup

import requests
import datetime
import re

import locale
locale.setlocale(locale.LC_TIME, "de_DE.utf-8")

from database_interface import *

main_url = "https://www.rhein-neckar-kreis.de/,Lde/start/landratsamt/coronavirus+-+faq.html"

req = requests.get(main_url)
bs = BeautifulSoup(req.text, "html.parser")

text = bs.findAll('p',{'class':'basecontent-line-break-text'})[1].getText()

cases_rheinneckarkreis_pattern = "[0-9]+ im Rhein"
cases_heidelberg_pattern = "[0-9]+ im Stadtgebiet Heidelberg"

cases_rheinneckarkreis_raw = re.findall(cases_rheinneckarkreis_pattern,text)[0]
cases_rheinneckarkreis = int(re.findall(r'[0-9]+', cases_rheinneckarkreis_raw)[0])

cases_heidelberg_raw = re.findall(cases_heidelberg_pattern,text)[0]
cases_heidelberg = int(re.findall(r'[0-9]+', cases_heidelberg_raw)[0])




status_raw = re.findall("Stand: .* 2020", text)[0]
status= datetime.datetime.strptime(status_raw, 'Stand: %d. %B %Y').strftime("%Y-%m-%d")

#print(cases_heidelberg_pattern)
#print(cases_rheinneckarkreis)
#print(status)

add_to_database("Rhein-Neckar-Kreis", status, cases_rheinneckarkreis)
add_to_database("Stadt Heidelberg", status, cases_heidelberg)

