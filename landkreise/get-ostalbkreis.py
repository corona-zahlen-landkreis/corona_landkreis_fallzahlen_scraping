from bs4 import BeautifulSoup

import requests
import datetime

from database_interface import *

main_url = "https://www.ostalbkreis.de/sixcms/detail.php?_topnav=36&_sub1=31788&_sub2=32062&_sub3=292448&id=292450"

req = requests.get(main_url)

bs = BeautifulSoup(req.text, "html.parser")

table = bs.find(lambda tag: tag.name=='table' and tag['border']=="1") 

row = table.findAll(lambda tag: tag.name=='tr')[1].find_all('td')


cases = row[0].getText()
status_raw = row[1].getText()

#'18.03.2020, 14:30 Uhr' does not match format '%Y-%m-%d %H:%M:%S.%f'
status= datetime.datetime.strptime(status_raw, '%d.%m.%Y').strftime("%Y-%m-%d")


add_to_database("Ostalbkreis", status, cases)
