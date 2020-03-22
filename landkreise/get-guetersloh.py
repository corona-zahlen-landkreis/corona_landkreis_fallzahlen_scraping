#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup

import requests
import datetime
import re

import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')

# for some german month names, e.g. März
import locale
locale.setlocale(locale.LC_ALL, "de_DE.utf-8")

from database_interface import *

main_url = "https://www.kreis-guetersloh.de/aktuelles/corona/"

req = requests.get(main_url)
bs = BeautifulSoup(req.text, "html.parser")

cases_pattern = "insgesamt [0-9]+ laborbest"

# I don't know, why I need to do this on my osx
text=bs.getText()
#.decode("UTF-8").encode("UTF-8")

# Im Kreis Gütersloh gibt es aktuell, das heißt zum Stand: 17. März, 14:00 Uhr, insgesamt 91 laborbestätigte Coronainfektionen.

information_raw = re.findall("Im Kreis Gütersloh gibt es aktuell, das heißt zum Stand: .*? Uhr, insgesamt [0-9]+ laborbestätigte Coronainfektionen.", text)

for one_info in information_raw:
    status_raw = re.findall("zum Stand: .*? Uhr", one_info)[0]
    try:
        statusDate = datetime.datetime.strptime(status_raw, 'zum Stand: %d. %B, %H:%M Uhr')
    except ValueError as ve:
        statusDate = datetime.datetime.strptime(status_raw, 'zum Stand: %d. %B, %H.%M Uhr')
    status = statusDate.replace(year = 2020).strftime("%Y-%m-%d %H:%M")    
    cases_raw = re.findall("insgesamt [0-9]+ laborbest", one_info)[0]
    cases = int(re.findall(r'[0-9]+', cases_raw)[0])
    add_to_database("05754", status, cases, "Kreis Gütersloh")
