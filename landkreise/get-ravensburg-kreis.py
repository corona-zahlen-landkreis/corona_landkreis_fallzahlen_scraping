from bs4 import BeautifulSoup

import scrape
import helper

main_url = "https://www.rv.de/Politik+_+Verwaltung/aktuelles+zum+coronavirus"

prefix_case = "gibt es bei uns"
community_id = "08436"

case_func = lambda bs: helper.extract_case_num(bs.text, prefix_case)
date_func = lambda bs: helper.extract_status_date_directregex(req.text, date_regex, date_format, 0, date_format)

date_regex = r"\<meta name=\"date\" content=\"([^\"]+)\"\>"
date_format = "%Y-%m-%d"

req = scrape.request_url(main_url)

scrape.scrape(main_url, community_id, case_func, date_func, "Kreis Ravensburg")
