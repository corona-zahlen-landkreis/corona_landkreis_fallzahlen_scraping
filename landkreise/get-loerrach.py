from bs4 import BeautifulSoup

import requests
import datetime
import re
import helper
import scrape


main_url = "https://www.loerrach-landkreis.de/corona"


date_func = lambda bs: helper.get_status(re.findall("Stand.*?Uhr",bs.text)[0])
cases_func = lambda bs: helper.extract_case_num(bs.text, "Aktuell bestätigte COVID19-Fälle:")
scrape.scrape(main_url, "08336", cases_func, date_func, name="Lörrach", options={'cookies': {"skipEntranceUrl":"1"}})

