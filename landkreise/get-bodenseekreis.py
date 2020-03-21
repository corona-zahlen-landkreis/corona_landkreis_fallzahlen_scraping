from bs4 import BeautifulSoup

import requests
import datetime
import re

from database_interface import *

main_url = "https://www.bodenseekreis.de/de/soziales-gesundheit/gesundheit/infektionsschutz/infektionskrankheiten/corona-virus/"

req = requests.get(main_url)
bs = BeautifulSoup(req.text, "html.parser")

# todo no status date, check if datapoint is present in database 
status_raw = bs.findAll(text=re.compile("Stand:"))[0]
status= datetime.datetime.strptime(status_raw, 'Stand: %d.%m.%Y, %H:%M Uhr').strftime("%Y-%m-%d %H:%M:%S")

cases_raw=bs.findAll(text=re.compile("labordiagnostisch bestätigte Infektionen"))
cases = int(re.findall(r'[0-9]+', cases_raw)[2])


#add_to_database("Bodenseekreis", status, cases)
