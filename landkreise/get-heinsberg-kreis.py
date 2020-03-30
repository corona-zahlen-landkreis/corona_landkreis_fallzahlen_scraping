import re
import requests
from bs4 import BeautifulSoup

import scrape
import helper

main_url = "https://www.kreis-heinsberg.de/aktuelles/aktuelles/?pid=5142"
community_id = "05370"

case_regex = r"(Infektionen liegen bei|gibt es im Kreis Heinsberg)[^0-9]*([0-9]+)"
date_regex = r"Kreis Heinsberg[\. ]*\(([0-9\.]+)\)"
date_format = '%d.%m.%Y'

req = requests.get(main_url)
req.encoding = 'iso-8859-1'
bs = BeautifulSoup(req.content, "html.parser")


def case_func(bs):
    cases_raw = re.findall(case_regex, bs.text)[0][1]
    return helper.get_number_only(cases_raw)


def date_func(bs):
    return helper.extract_status_date_directregex(bs.text, date_regex, date_format, 0)


scrape.scrape(main_url, community_id, case_func, date_func, "Kreis Heinsberg")
