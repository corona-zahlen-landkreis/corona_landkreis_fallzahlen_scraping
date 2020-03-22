from bs4 import BeautifulSoup

import requests
import datetime
import re
import helper
import scrape

# import locale
# locale.setlocale(locale.LC_TIME, "de_DE.utf-8")

# from database_interface import *

main_url = "https://www.loerrach-landkreis.de/de/Service-Verwaltung/Fachbereiche/Gesundheit/Sachgebiete/Sachgebiet/Corona"


date_func = lambda bs: helper.extract_status_date_directregex(bs.text, r"\(Stand \d\d. [^0-9]+ \d{4}, \d\d:\d\d Uhr\)", "(Stand %d. %B %Y, %H:%M Uhr)", 0)
cases_func = lambda bs: helper.extract_case_num(bs.text, "Aktuell bestätigte COVID19-Fälle:")
scrape.scrape(main_url, "08336", cases_func, date_func, name="Lörrach", options={'cookies': {"skipEntranceUrl":"1"}})

# session = requests.Session()

# req = session.post(main_url, cookies={"skipEntranceUrl":"1"})

# #req=session.get(main_url)
# bs = BeautifulSoup(req.text, "html.parser")


#cases_pattern = "Aktuell bestätigte COVID19-Fälle: [0-9]+"

#(Stand 20. März 2020, 16:15 Uhr)

# status_raw = re.findall("Stand .* Uhr",bs.findAll(text=re.compile("Stand "))[0])[0]
# status= datetime.datetime.strptime(status_raw, 'Stand %d. %B %Y, %H:%M Uhr').strftime("%Y-%m-%d %H:%M:%S")



# cases_raw = bs.find(text=re.compile(cases_pattern))
# cases = int(re.findall(r'[0-9]+', cases_raw)[1])

# print(cases)
# print(status)
# add_to_database("08336", status, cases)
