from bs4 import BeautifulSoup

import requests
import datetime

import helper
import scrape
from database_interface import *

main_url = "https://www.ostalbkreis.de/sixcms/detail.php?_topnav=36&_sub1=31788&_sub2=32062&_sub3=292448&id=292450"

req = scrape.request_url(main_url)

bs = BeautifulSoup(req.text, "html.parser")

table = bs.findAll(lambda tag: tag.name=='table' and tag['border']=="1")[1]

row = table.findAll(lambda tag: tag.name=='tr')[1].find_all('td')


cases = row[0].getText()
status_raw = row[4].getText()

status= helper.get_status(status_raw)


add_to_database("08136", status, cases, "Ostalbkreis")
