from bs4 import BeautifulSoup

import requests
import datetime
import re
import locale

from database_interface import *

DISTRICT_UID = "05566"

locale.setlocale(locale.LC_ALL, 'de_DE.utf-8')
main_url = "https://www.kreis-steinfurt.de/kv_steinfurt/Aktuelles/Slider/Informationen%20Coronavirus"

req = requests.get(main_url)
bs = BeautifulSoup(req.text, "html.parser")

date_raw = bs.findAll(text=re.compile("Pressemitteilung von"))[0]
date = datetime.datetime.strptime(date_raw, 'Pressemitteilung von %A, %d. %B %Y\nKreis Steinfurt')

time_raw = bs.findAll(text=re.compile("Im Kreis Steinfurt sind mit Stand von\n" + date.strftime("%A, %d. %B")))[0]
time = datetime.datetime.strptime(time_raw.split("Uhr")[0],
                                  ("Kreis Steinfurt. Im Kreis Steinfurt sind mit Stand von\n" +
                                   date.strftime("%A, %d. %B") + ", %H.%M ")).time()

datetime_raw = datetime.datetime.combine(date, time)
status = datetime_raw.strftime("%Y-%m-%d %H:%M:%S")

cases_raw = bs.findAll(text=re.compile("Uhr, [0-9]+ Menschen nachweislich mit dem"))[0]
cases = int(re.findall(r'[0-9]+', cases_raw)[3])

add_to_database(DISTRICT_UID, status, cases, "Kreis Steinfurt")

communities = {
    'Altenberge': {'uid': '055660004004', 'cases': -1},
    'Emsdetten': {'uid': '055660008008', 'cases': -1},
    'Greven': {'uid': '055660012012', 'cases': -1},
    'Hopsten': {'uid': '055660020020', 'cases': -1},
    'Hörstel': {'uid': '055660016016', 'cases': -1},
    'Horstmar': {'uid': '055660024024', 'cases': -1},
    'Ibbenbüren': {'uid': '055660028028', 'cases': -1},
    'Ladbergen': {'uid': '055660032032', 'cases': -1},
    'Laer': {'uid': '055660036036', 'cases': -1},
    'Lengerich': {'uid': '055660040040', 'cases': -1},
    'Lienen': {'uid': '055660044044', 'cases': -1},
    'Lotte': {'uid': '055660048048', 'cases': -1},
    'Metelen': {'uid': '055660052052', 'cases': -1},
    'Mettingen': {'uid': '055660056056', 'cases': -1},
    'Neuenkirchen': {'uid': '055660060060', 'cases': -1},
    'Nordwalde': {'uid': '055660064064', 'cases': -1},
    'Ochtrup': {'uid': '055660068068', 'cases': -1},
    'Recke': {'uid': '055660072072', 'cases': -1},
    'Rheine': {'uid': '055660076076', 'cases': -1},
    'Saerbeck': {'uid': '055660080080', 'cases': -1},
    'Steinfurt': {'uid': '055660084084', 'cases': -1},
    'Tecklenburg': {'uid': '055660088088', 'cases': -1},
    'Westerkappeln': {'uid': '055660092092', 'cases': -1},
    'Wettringen': {'uid': '055660096096', 'cases': -1}
}

community_pattern = "In %s: ([0-9]+).*"
for key in communities.keys():
    community_cases = bs.findAll(text=re.compile(community_pattern % key))
    if 0 < len(community_cases):
        cases = re.search(community_pattern % key, community_cases[0]).group(1)
        communities[key]['cases'] = int(cases)
        add_to_database(communities[key]['uid'], status, communities[key]['cases'], key, DISTRICT_UID)
