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

table = bs.find('table')

data = helper.get_table(bs.find('table'))

# remove table head
data.pop(0)

for row in data:
    status = datetime.datetime.strptime(row[0], '%d.%m. %Y').strftime("%Y-%m-%d")
    cases = int(row[1])
    add_to_database("03353", status, cases, "Kreis Harburg")

