from bs4 import BeautifulSoup

import requests
import datetime
import re

import locale
locale.setlocale(locale.LC_TIME, "de_DE.utf-8")

from database_interface import *

DISTRICT_UID = "03454"

main_url = "https://www.emsland.de/buerger-behoerde/aktuell/coronavirus/fallzahlen-den-emslaendischen-kommunen.html"

req = requests.get(main_url)
bs = BeautifulSoup(req.text, "html.parser")

cases_pattern = "Gesamtzahl\n[0-9]+"

text=bs.getText()
# note the special space!
status_raw = re.findall("Stand .* Uhr",text)[0]
status= datetime.datetime.strptime(status_raw, 'Stand %d.%m.%Y, %H Uhr').strftime("%Y-%m-%d %H:%M")

cases_raw = re.findall(cases_pattern,text)[0]
cases = int(re.findall(r'[0-9]+', cases_raw)[0])

add_to_database(DISTRICT_UID, status, cases)

communities = {
    'Emsbüren': {'uid': '034540010010', 'cases': -1},
    'Geeste': {'uid': '034540014014', 'cases': -1},
    'Haren': {'uid': '034540018018', 'cases': -1},
    'Haselünne': {'uid': '034540019019', 'cases': -1},
    'Lingen': {'uid': '034540032032', 'cases': -1},
    'Meppen': {'uid': '034540035035', 'cases': -1},
    'Papenburg': {'uid': '034540041041', 'cases': -1},
    'Rhede': {'uid': '034540044044', 'cases': -1},
    'Salzbergen': {'uid': '034540045045', 'cases': -1},
    'Twist': {'uid': '034540054054', 'cases': -1},
    'Dersum': {'uid': '034545401007', 'cases': -1},
    'Dörpen': {'uid': '034545401008', 'cases': -1},
    'Heede': {'uid': '034545401020', 'cases': -1},
    'Kluse': {'uid': '034545401025', 'cases': -1},
    'Lehe': {'uid': '034545401030', 'cases': -1},
    'Neubörger': {'uid': '034545401037', 'cases': -1},
    'Neulehe': {'uid': '034545401038', 'cases': -1},
    'Walchum': {'uid': '034545401056', 'cases': -1},
    'Wippingen': {'uid': '034545401060', 'cases': -1},
    'Andervenne': {'uid': '034545402001', 'cases': -1},
    'Beesten': {'uid': '034545402003', 'cases': -1},
    'Freren': {'uid': '034545402012', 'cases': -1},
    'Messingen': {'uid': '034545402036', 'cases': -1},
    'Thuine': {'uid': '034545402053', 'cases': -1},
    'Dohren': {'uid': '034545403009', 'cases': -1},
    'Herzlake': {'uid': '034545403021', 'cases': -1},
    'Lähden': {'uid': '034545403026', 'cases': -1},
    'Fresenburg': {'uid': '034545404013', 'cases': -1},
    'Lathen': {'uid': '034545404029', 'cases': -1},
    'Niederlangen': {'uid': '034545404039', 'cases': -1},
    'Oberlangen': {'uid': '034545404040', 'cases': -1},
    'Renkenberge': {'uid': '034545404043', 'cases': -1},
    'Sustrum': {'uid': '034545404052', 'cases': -1},
    'Bawinkel': {'uid': '034545405002', 'cases': -1},
    'Gersten': {'uid': '034545405015', 'cases': -1},
    'Handrup': {'uid': '034545405017', 'cases': -1},
    'Langen': {'uid': '034545405028', 'cases': -1},
    'Lengerich': {'uid': '034545405031', 'cases': -1},
    'Wettrup': {'uid': '034545405059', 'cases': -1},
    'Bockhorst': {'uid': '034545406004', 'cases': -1},
    'Breddenberg': {'uid': '034545406006', 'cases': -1},
    'Esterwegen': {'uid': '034545406011', 'cases': -1},
    'Hilkenbrook': {'uid': '034545406022', 'cases': -1},
    'Surwold': {'uid': '034545406051', 'cases': -1},
    'Börger': {'uid': '034545407005', 'cases': -1},
    'Groß Berßen': {'uid': '034545407016', 'cases': -1},
    'Hüven': {'uid': '034545407023', 'cases': -1},
    'Klein Berßen': {'uid': '034545407024', 'cases': -1},
    'Sögel': {'uid': '034545407047', 'cases': -1},
    'Spahnharrenstätte': {'uid': '034545407048', 'cases': -1},
    'Stavern': {'uid': '034545407050', 'cases': -1},
    'Werpeloh': {'uid': '034545407058', 'cases': -1},
    'Lünne': {'uid': '034545408034', 'cases': -1},
    'Schapen': {'uid': '034545408046', 'cases': -1},
    'Spelle': {'uid': '034545408049', 'cases': -1},
    'Lahn': {'uid': '034545409027', 'cases': -1},
    'Lorup': {'uid': '034545409033', 'cases': -1},
    'Rastdorf': {'uid': '034545409042', 'cases': -1},
    'Vrees': {'uid': '034545409055', 'cases': -1},
    'Werlte, Stadt': {'uid': '034545409057', 'cases': -1}
}

community_pattern = ".*%s.*"
for key in communities.keys():
    textbox = bs.find(class_="content__textbox")
    community_cases = textbox.findAll(text=re.compile(community_pattern % key))
    if 0 < len(community_cases):
        cases = community_cases[0].findNext('td').get_text()
        communities[key]['cases'] = int(cases)
        add_to_database(communities[key]['uid'], status, communities[key]['cases'], key, DISTRICT_UID)
