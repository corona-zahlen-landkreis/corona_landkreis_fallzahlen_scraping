from bs4 import BeautifulSoup
from bs4.diagnose import diagnose
DEBUG = False

import requests
import datetime
import re
if DEBUG:
    import pprint

from database_interface import *

DISTRICT_UID = "05974"


def debug_print(arg):
  if DEBUG:
    print(arg)

main_url = "https://www.presse-service.de/rss.aspx?v=2&p=551"

req = requests.get(main_url)
req.encoding = 'utf8'
bs = BeautifulSoup(req.text, "html.parser")
news_list = bs.findAll("item")
for item in news_list:
    status_pattern = "(.*) Das Referat .*"
    cases_pattern = "([0-9]+) .* Corona-Fälle"

    cases_raw = re.search(cases_pattern, item.title.text)
    if cases_raw == None:
        continue
    cases = int(cases_raw.group(1))
    print("\n")
    debug_print('%s' % item.title.text)
    debug_print('%s' % item.guid.text)
    debug_print('%s' % item.pubdate.text)
    status = datetime.datetime.strptime(item.pubdate.text, '%a, %d %b %Y %H:%M:%S %Z').replace(tzinfo=datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S %Z")
    print('Parsed time: %s' % status)
    if DEBUG == False:
       add_to_database(DISTRICT_UID, status, cases, "Kreis Soest")
    
    # Fetch and output communities for Kreis Soest
    # using guid as link does not work?
    community_url = item.guid.text
    subreq = requests.get(community_url)
    subreq.encoding = 'utf8'
    subbs = BeautifulSoup(subreq.text, "html.parser")
    search_message = 'p[class="ps_meldungstext"]'
    message = subbs.select(search_message)
    if len(message) == 0:
        print('ERROR: did not find \'%s\' for URL: %s' % (search_message, community_url))
        continue
    message = message[0].p.text

#59740004004	5974004	Anröchte
#59740008008	5974008	Bad Sassendorf
#59740012012	5974012	Ense
#59740016016	5974016	Erwitte, Stadt
#59740020020	5974020	Geseke, Stadt
#59740024024	5974024	Lippetal
#59740028028	5974028	Lippstadt, Stadt
#59740032032	5974032	Möhnesee
#59740036036	5974036	Rüthen, Stadt
#59740040040	5974040	Soest, Stadt
#59740044044	5974044	Warstein, Stadt
#59740048048	5974048	Welver
#59740052052	5974052	Werl, Stadt
#59740056056	5974056	Wickede (Ruhr)

    community = {
                'Anröchte': { 'uid': '059740004004', cases: -1 },
#                'Ense': { 'uid': '059740012012', cases: -1},
                'Bad Sassendorf': { 'uid': '059740008008', cases: -1},
                'Erwitte': { 'uid': '059740016016', cases: -1},
                'Geseke': { 'uid': '059740020020', cases: -1},
                'Lippetal': { 'uid': '059740024024', cases: -1},
                'Lippstadt': { 'uid': '059740028028', cases: -1},
                'Möhnesee': { 'uid': '059740032032', cases: -1},
                'Rüthen': { 'uid': '059740036036', cases: -1},
                'Soest': { 'uid': '059740040040', cases: -1},
                'Warstein': { 'uid': '059740044044', cases: -1},
                'Welver': { 'uid': '059740048048', cases: -1},
                'Werl': { 'uid': '059740052052', cases: -1},
#                'Wickede (Ruhr)': { 'uid': '059740056056', cases: -1}
    }
    community_pattern = "Kommunen im Kreis Soest:.*%s ([0-9]+)"
    for key in community.keys():
        community_matches = re.search(community_pattern % key, message)
        if community_matches != None:
            community[key][cases] = int(community_matches.group(1))
            if DEBUG == False:
                add_to_database(community[key]['uid'], status, community[key][cases], key, DISTRICT_UID)
        else:
            print('ERROR: Failed to find \'%s\' in %s' %(community_pattern % key, community_url))

    if DEBUG:
        pprint.pprint(("Communities:", community))

