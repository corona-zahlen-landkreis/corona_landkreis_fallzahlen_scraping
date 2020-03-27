from bs4 import BeautifulSoup

import requests
import datetime
import re
import locale

import scrape
import helper
from database_interface import *


locale.setlocale(locale.LC_TIME, "de_DE.utf-8")

main_url = "https://www.baden-baden.de/buergerservice/news/corona-aktuell_9635/"


#Baden-Baden. Im Zuständigkeitsbereich des Gesundheitsamtes in Rastatt, zu dem neben Baden-Baden auch der Landkreis Rastatt gehört, sind aktuell insgesamt 88 Personen mit dem Corona-Virus infiziert. Davon sind 19 Fälle aus Baden-Baden. (Stand 19. März, 12 Uhr)

req = scrape.request_url(main_url)
bs = BeautifulSoup(req.text, "html.parser")
text = bs.find(text=re.compile(r"Baden-Baden\..*?Rastatt.*?Stand"))


status_pattern = "Stand .* Uhr"
cases_total_pattern = "Zusammen sind das .* Personen"
cases_badenbaden_pattern = "In Baden-Baden sind inzwischen.*infiziert"


status_raw=re.findall(status_pattern,text)[0]

#Stand 19. März, 12 Uhr
status=helper.get_status(status_raw)


cases_total = int(re.findall(r'[0-9]+', re.findall(cases_total_pattern, text)[0])[0])
cases_badenbaden = int(re.findall(r'[0-9]+', re.findall(cases_badenbaden_pattern, text)[0])[0])

cases_rastatt = cases_total-cases_badenbaden

#cases_raw=re.findall(text=re.compile("Alb-Donau-Kreis \("))[0]
#cases = int(re.findall(r'[0-9]+', cases_raw)[2])


add_to_database("08211", status, cases_badenbaden, "Baden-Baden")
add_to_database("08216", status, cases_rastatt, "Rastatt")

