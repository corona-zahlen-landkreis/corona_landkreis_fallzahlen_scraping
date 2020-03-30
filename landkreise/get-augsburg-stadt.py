from bs4 import BeautifulSoup

import requests
import datetime
import re

import scrape
from helper import *
from database_interface import *

main_url = "https://www.augsburg.de/umwelt-soziales/gesundheit/coronavirus"

req = scrape.request_url(main_url)
bs = BeautifulSoup(req.text, "html.parser")

#(Stand 22.3.2020, 09:30 Uhr)
status_pattern = "Stand.*?Uhr"
cases_pattern = "bisher [0-9]+ COVID"

text = remove_chars_from_text(bs.getText(),["\n"])
text = clear_text_of_ambigous_chars(text)

status_raw = re.findall(status_pattern,text)[0]
status = get_status(status_raw)

cases_raw = re.findall(cases_pattern, text)[0]
cases = int(re.findall(r'[0-9]+', cases_raw)[0])

add_to_database("09761", status, cases, "Stadt Augsburg")
