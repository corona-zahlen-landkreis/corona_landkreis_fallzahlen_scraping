from bs4 import BeautifulSoup

import scrape
import helper

main_url = "https://www.kreis-tuebingen.de/corona.html"

prefix_case = "Aktuelle Fallzahlen: "
community_id = "08416"

case_func = lambda bs: helper.extract_case_num(bs.text, prefix_case)
date_func = lambda bs: helper.extract_status_date_directregex(bs.text, date_regex, date_format, 0)

date_regex = r"\([ ]*Stand ([0-9\.]+)\)"
date_format = "%d.%m.%Y"

req = scrape.request_url(main_url)
bs = BeautifulSoup(req.text, "html.parser")

scrape.scrape(main_url, community_id, case_func, date_func, "Kreis Tuebingen")
