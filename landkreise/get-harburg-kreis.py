from bs4 import BeautifulSoup

import requests
import datetime
import re
import locale

locale.setlocale(locale.LC_TIME, "de_DE.utf-8")
import helper
import scrape

from database_interface import *

main_url = "https://www.landkreis-harburg.de/corona"

req = scrape.request_url(main_url)

bs = BeautifulSoup(req.text, "html.parser")

text_match = re.compile("Zahl erfasster Coronafälle im Landkreis Harburg")
text_position = bs.find(text=text_match)
table = text_position.findNext('table')

data = helper.get_table(table)

# remove table head
data.pop(0)

for row in data:
    status = helper.get_status(row[0])
    cases = int(row[1])
    add_to_database("03353", status, cases, "Kreis Harburg")

