from bs4 import BeautifulSoup

import requests
import datetime
import re
import helper
import scrape

from database_interface import *

main_url = "https://www.info-corona-lrahdh.de/startseite"

req = requests.get(main_url)
bs = BeautifulSoup(req.text, "html.parser")

status_pattern = re.compile(r'.*Stand: .*')
cases_pattern = re.compile(r'.*Es gibt aktuell.*')


DISTRICT_UID = "08135"

# Aktuelle Informationen zum Coronavirus (Stand: 18.03.2020, 12:00 Uhr)
status_raw = bs.findAll(text=re.compile("Stand"))[0]
status= datetime.datetime.strptime(status_raw, 'Aktuelle Informationen zum Coronavirus (Stand: %d.%m.%Y, %H:%M Uhr)').strftime("%Y-%m-%d %H:%M:%S")


text_match = re.compile("Was gibt’s neues?")
text_position = bs.find(text=text_match)
table = text_position.findNext('table')

data_total=helper.get_table(table)

cases = helper.get_number_only(data_total[1][0])

community = {
    # heidenheim an der brenz
            'Stadt Heidenheim':    { 'uid': '08135019', cases: -1 },
            'Giengen':             { 'uid': '08135016', cases: -1 },
            'Herbrechtingen':      { 'uid': '08135020', cases: -1 },
            'Niederstotzingen':    { 'uid': '08135027', cases: -1 },
            'Dischingen':          { 'uid': '08135010', cases: -1 },
            'Gerstetten':          { 'uid': '08135015', cases: -1 },
            'Hermaringen':         { 'uid': '08135021', cases: -1 },
            'Königsbronn':         { 'uid': '08135025', cases: -1 },
            'Nattheim':            { 'uid': '08135026', cases: -1 },
            'Sontheim':            { 'uid': '08135031', cases: -1 },
            'Steinheim':           { 'uid': '08135032', cases: -1 },
    
}
community_pattern = "%s: [0-9]+"
for key in community.keys():
    community_matches = re.search(community_pattern % key, bs.text)
    if community_matches != None:
        community[key][cases] = int(helper.get_number_only(community_matches.group(0)))
        add_to_database(community[key]['uid'], status, community[key][cases], key, DISTRICT_UID)
    else:
        logger.error('ERROR: Failed to find \'%s\' in %s' %(community_pattern % key, main_url))

if scrape.SCRAPER_DEBUG:
    pprint.pprint(("Communities:", community))
        
add_to_database(DISTRICT_UID, status, cases, "Kreis Heidenheim")
