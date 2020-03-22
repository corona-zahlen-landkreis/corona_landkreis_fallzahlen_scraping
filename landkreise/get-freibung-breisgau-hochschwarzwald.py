from bs4 import BeautifulSoup

import requests
import datetime
import re

from database_interface import *

main_url = "https://www.breisgau-hochschwarzwald.de/pb/Breisgau-Hochschwarzwald/Start/Service+_+Verwaltung/Corona-Virus.html"

req=requests.get(main_url)
bs = BeautifulSoup(req.text, "html.parser")


data = []
table = bs.find('table', attrs={'id':'grid_1980892'})
table_body = table.find('tbody')

rows = table_body.find_all('tr')
for row in rows:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    data.append([ele for ele in cols if ele]) # Get rid of empty values
    

status_raw = data[1][0]    
#21.03., 08:30 Uhr
status= datetime.datetime.strptime(status_raw, '%d.%m., %H:%M Uhr').strftime("2020-%m-%d %H:%M:%S")

cases_freiburg = data[1][2]
cases_breisgau_hochschwarzwald = data[1][3]

add_to_database("08311", status, cases_freiburg, "Freiburg im Breisgau")
add_to_database("08315", status, cases_breisgau_hochschwarzwald, "Breisgau-Hochschwarzwald")

