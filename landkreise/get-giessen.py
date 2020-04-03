from bs4 import BeautifulSoup

import scrape
import helper
from database_interface import *

url = "https://www.lkgi.de/gesundheit-und-soziales/3060-gesundheitsamt-informiert-br-ueber-coronavirus"

req = scrape.request_url(url)
bs = BeautifulSoup(req.text, 'html.parser')

table = bs.find('table')

data = helper.get_table(table)
data.pop(0)

for row in data:
  status = helper.get_status(row[0])
  cases = int(row[1])
  add_to_database("06531", status, cases, name="Kreis Gießen")

