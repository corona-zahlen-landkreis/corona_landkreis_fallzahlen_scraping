from bs4 import BeautifulSoup

import requests
import datetime
import re
import helper
import scrape


main_url = "https://www.loerrach-landkreis.de/de/Service-Verwaltung/Fachbereiche/Gesundheit/Sachgebiete/Sachgebiet/Corona"


date_func = lambda bs: helper.extract_status_date_directregex(bs.text, r"\(Stand \d\d. [^0-9]+ \d{4}, \d\d:\d\d Uhr\)", "(Stand %d. %B %Y, %H:%M Uhr)", 0)
cases_func = lambda bs: helper.extract_case_num(bs.text, "Aktuell bestätigte COVID19-Fälle:")
scrape.scrape(main_url, "08336", cases_func, date_func, name="Lörrach", options={'cookies': {"skipEntranceUrl":"1"}})

