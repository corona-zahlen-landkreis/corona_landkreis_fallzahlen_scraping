from bs4 import BeautifulSoup
import re

import scrape
from helper import *
from database_interface import *

url = "https://www.landkreis-ansbach.de/Quicknavigation/Startseite/Aktuelle-Informationen-zum-Coronavirus.php?object=tx,1503.10.1&ModID=7&FID=2238.2854.1&NavID=2150.1"

regex_total = "insgesamt \d+"
regex_kreis = "\d+ der mit dem .*? Landkreis"

date_regex="\(Stand: .*?\)"

req = scrape.request_url(url)

bs = BeautifulSoup(req.text, "html.parser")

text=bs.getText()
text=clear_text_of_ambigous_chars(text)

status_raw = re.findall(date_regex,text)[0]
status= get_status(status_raw)


cases_kreis_raw = re.findall(regex_kreis,text)[0]
cases_kreis = get_number_only(cases_kreis_raw)

cases_total_raw = re.findall(regex_total,text)[0]
cases_total = get_number_only(cases_total_raw)

cases_stadt = cases_total-cases_kreis
add_to_database("09571", status, cases_kreis, "Kreis Ansbach")
add_to_database("09561000", status, cases_stadt, "Stadt Ansbach")



