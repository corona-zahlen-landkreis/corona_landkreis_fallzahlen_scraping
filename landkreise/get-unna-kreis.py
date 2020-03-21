from bs4 import BeautifulSoup

import requests
import datetime
import re

import locale
locale.setlocale(locale.LC_TIME, "de_DE.utf-8")

from database_interface import *

main_url = "https://www.kreis-unna.de/nachrichten/n/?tx_news_pi1%5Bnews%5D=14220&tx_news_pi1%5Bcontroller%5D=News&tx_news_pi1%5Baction%5D=detail&cHash=31b36b644c47f5bc4011e1a3e334e130"

req = requests.get(main_url)
bs = BeautifulSoup(req.text, "html.parser")

cases_pattern = "Gesamt[0-9]+"

text=bs.getText()

status_raw = bs.findAll('time',{'itemprop':'datePublished'})[0].getText()
status= datetime.datetime.strptime(status_raw, '%d.%m.%Y').strftime("%Y-%m-%d")

cases_raw = re.findall(cases_pattern,text)[0]
cases = int(re.findall(r'[0-9]+', cases_raw)[0])

add_to_database(05978, status, cases)
