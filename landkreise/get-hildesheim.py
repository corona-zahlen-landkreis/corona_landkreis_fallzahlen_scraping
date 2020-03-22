import scrape
import helper
import requests
import re
from bs4 import BeautifulSoup


def is_case_link(link):
    return re.search(r'(Fälle|Fallzahlen|Zahlen)-zum-Coronavirus', link)

presse_url = "https://landkreishildesheim.de/Politik-Verwaltung/Verwaltung/Presse/Pressemitteilungen"

communities = {
    "Alfeld": "032540002002",
    "Algermissen": "032540003003",
    "Bad Salzdetfurth": "032540005005",
    "Bockenem": "032540008008",
    "Diekholzen": "032540011011",
    "Elze": "032540014014",
    "Freden": "032540042042",
    "Giesen": "032540017017",
    "Harsum": "032540020020",
    "Hildesheim": "032540021021",
    "Holle": "032540022022",
    "Nordstemmen": "032540026026",
    "Stadt Sarstedt": "032540028028",
    "Schellerten": "032540029029",
    "Söhlde": "032540032032",
    "Lamspringe": "032540044044",
    "Sibbesse": "032540045045",
    "SG Leinebergland": "032545406",
}



# Feed der Pressemitteilungen nach aktuellstem Fallzahlen Link durchsuchen
presse = requests.get(presse_url)
bs_presse = BeautifulSoup(presse.text, "html.parser")
list_titles = bs_presse.findAll(attrs={'class': re.compile(r"liste-titel")})
link_map = [i.a['href'] for i in list_titles if is_case_link(i.a['href'])] 

prefix_case = "gibt es aktuell"
date_regex = r"\(Stand:[^\)]+\)"
date_format = "(Stand: %A, %d. %B %H:%M Uhr)"

case_func = lambda bs: helper.extract_case_num(bs.text, prefix_case)
date_func = lambda bs: helper.extract_status_date_directregex(bs.text, date_regex, date_format, 0)

url = link_map[0]
community_id = "03254"

scrape.scrape(url, community_id, case_func, date_func, "Hildesheim")

page = requests.get(url)
bs = BeautifulSoup(page.text, "html.parser")    

# Gemeinden auswerten
for com_name in communities.keys():
    case_prefix = com_name + " ("
    if re.search(re.escape(case_prefix), bs.text):
        com_cases = lambda bs: helper.extract_case_num(bs.text, case_prefix)
        scrape.scrape(url, communities[com_name], com_cases, date_func, com_name, community_id)


