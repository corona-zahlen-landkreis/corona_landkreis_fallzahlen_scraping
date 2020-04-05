from bs4 import BeautifulSoup

import requests
import datetime
import re

import locale
locale.setlocale(locale.LC_TIME, "de_DE.utf-8")

import scrape
from helper import *
from database_interface import *

main_url = "https://www.offenbach.de/leben-in-of/gesundheit/dir-6/corona/coronavirus_meldungen.php"

req = scrape.request_url(main_url)
bs = BeautifulSoup(req.text, "html.parser")

text = bs.getText()
# f = open("debug.txt", "w")
# f.write(text)
# f.close()

# result:
# Infektionen in Offenbach (Quelle: Stadtgesundheitsamt):
#
#
#
# Fälle gesamt
# schwer erkrankt
# genesen
# Todesfall
#
#
# 34
# 3
# 9
# 1

pattern_of = re.compile(".*Infektionen in Offenbach \\(Quelle: Stadtgesundheitsamt\\):\n+Fälle gesamt\n" +
                        "+schwer erkrankt\n+genesen\n+Todesf\\wlle?\n+(\\d+)\n+(\\d+)\n+(\\d+)\n+(\\d+)\n+.*\n" +
                        "Stand: (\\d+\\.\\W\\w+\\W\\d{4}).*", re.MULTILINE)

m = pattern_of.search(text)
# print("Faelle gesamt: ", m.group(1))
# print("schwer erkrankt: ", m.group(2))
# print("genesen: ", m.group(3))
# print("Todesfall: ", m.group(4))
# print("Stand: ", m.group(5))

cases = int(m.group(1))
status = get_status(m.group(5))

# print("cases: ", cases)
# print("status: ", status)

add_to_database("06413000", status, cases, "Stadt Offenbach")
