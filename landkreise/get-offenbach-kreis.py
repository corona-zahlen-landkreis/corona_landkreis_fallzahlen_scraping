from bs4 import BeautifulSoup

import requests
import datetime
import re

import locale
locale.setlocale(locale.LC_TIME, "de_DE.utf-8")

import scrape
from helper import *
from database_interface import *

main_url = "https://www.kreis-offenbach.de/Themen/Gesundheit-Verbraucher-schutz/akut/Corona"

req = scrape.request_url(main_url)
bs = BeautifulSoup(req.text, "html.parser")

text = bs.getText()
f = open("debug.txt", "w")
f.write(text)
f.close()

# result:
# SARS-CoV-2 im Kreis
# Bestätigte Infektionen:
# 232
# davon wieder gesund:
# 78
# davon Todesfälle:
# 6
# (Stand 4. April 2020)


pattern = re.compile(".*Bestätigte Infektionen:\n+(\\d+)\n+davon wieder gesund:\n+(\\d+)\n" +
                     "davon Todesfälle:\n(\\d+)\n+\\(Stand (\\d+\\.\\W\\w+\\W\\d{4})\\).*", re.MULTILINE)

m = pattern.search(text)
# print("Infektionen: ", m.group(1))
# print("genesen: ", m.group(2))
# print("Todesfall: ", m.group(3))
# print("Stand: ", m.group(4))

cases = int(m.group(1))
status = get_status(m.group(4))

# print("cases: ", cases)
# print("status: ", status)

add_to_database("06438000", status, cases, "Kreis Offenbach")
