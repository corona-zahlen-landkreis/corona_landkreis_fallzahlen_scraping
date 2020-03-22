import scrape
import helper
import requests
import re
from bs4 import BeautifulSoup


def is_case_link(link):
    return re.search(r'(Fälle|Fallzahlen|Zahlen)-zum-Coronavirus', link)

presse_url = "https://landkreishildesheim.de/Politik-Verwaltung/Verwaltung/Presse/Pressemitteilungen"



# Feed der Pressemitteilungen nach aktuellstem Fallzahlen Link durchsuchen
presse = requests.get(presse_url)
bs_presse = BeautifulSoup(presse.text, "html.parser")
list_titles = bs_presse.findAll(attrs={'class': re.compile(r"liste-titel")})
link_map = [i.a['href'] for i in list_titles if is_case_link(i.a['href'])] 

url = link_map[0]
prefix_case = "gibt es aktuell"
date_regex = r"\(Stand:[^\)]+\)"
date_format = "(Stand: %A, %d. %B %H:%M Uhr)"

case_func = lambda bs: helper.extract_case_num(bs.text, prefix_case)
date_func = lambda bs: helper.extract_status_date_directregex(bs, date_regex, date_format, 0)

scrape.scrape(url, "03254", case_func, date_func)

