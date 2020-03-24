from bs4 import BeautifulSoup

import requests
import datetime
import re

from database_interface import *
import helper
import scrape

DISTRICT_UID = "09184"

main_url = "https://www.landkreis-muenchen.de/themen/verbraucherschutz-gesundheit/gesundheit/fallzahlen-nach-gemeinden/"

req = scrape.request_url(main_url)
bs = BeautifulSoup(req.text, "html.parser")

status_pattern = "\(Stand: .*?\)"
cases_pattern = "[0-9]+ bestätigte Erkrankungsfälle"

full_text = helper.clear_text_of_ambigous_chars(bs.getText())

text = bs.findAll(text=re.compile(status_pattern))[0]
status_raw = re.findall(status_pattern,text)[0]
status = datetime.datetime.strptime(status_raw, '(Stand: %d.%m.%Y, %H:%M Uhr)').strftime("%Y-%m-%d")

cases_raw = re.findall(cases_pattern, full_text)[0]
cases = int(re.findall(r'[0-9]+', cases_raw)[0])

add_to_database("09184", status, cases, "Kreis München")


table = bs.find('table', {'class':'contenttable'})

data = dict(helper.get_table(table))

community = {
            'Aschheim': { 'uid': '09184112', cases: -1 },
            'Aying': { 'uid': '09184137', cases: -1 },
            'Baierbrunn':{ 'uid': '09184113', cases: -1 },
            'Brunnthal': { 'uid': '09184114', cases: -1 },
            'Garching b. München': { 'uid': '09184119', cases: -1 },
            'Gräfelfing': { 'uid': '09184120', cases: -1 },
            'Grasbrunn':{ 'uid': '09184121', cases: -1 },
            'Grünwald':{ 'uid': '09184122', cases: -1 },
            'Haar':{ 'uid': '09184123', cases: -1 },
            'Höhenkirchen-Siegertsbrunn':{ 'uid': '09184127', cases: -1 },
            'Hohenbrunn':{ 'uid': '09184129', cases: -1 },
            'Ismaning':{ 'uid': '09184130', cases: -1 },
            'Kirchheim b. München':{ 'uid': '09184131', cases: -1 },
            'Neubiberg':{ 'uid': '09184146', cases: -1 },
            'Neuried':{ 'uid': '09184132', cases: -1 },
            'Oberhaching':{ 'uid': '09184134', cases: -1 },
            'Oberschleißheim':{ 'uid': '09184135', cases: -1 },
            'Ottobrunn':{ 'uid': '09184136', cases: -1 },
            'Planegg':{ 'uid': '09184138', cases: -1 },
            'Pullach im Isartal':{ 'uid': '09184139', cases: -1 },
            'Putzbrunn':{ 'uid': '09184140', cases: -1 },
            'Sauerlach':{ 'uid': '09184141', cases: -1 },
            'Schäftlarn':{ 'uid': '09184142', cases: -1 },
            'Straßlach-Dingharting':{ 'uid': '09184144', cases: -1 },
            'Taufkirchen':{ 'uid': '09184145', cases: -1 },
            'Unterföhring':{ 'uid': '09184147', cases: -1 },
            'Unterhaching':{ 'uid': '09184148', cases: -1 },
            'Unterschleißheim':{ 'uid': '09184149', cases: -1 },
            
}


for key in community.keys():
    cases = int(data.get(key))
    if cases != None:
        community[key][cases] = cases
        add_to_database(community[key]['uid'], status, community[key][cases], key, DISTRICT_UID)
    else:
        logger.error('ERROR: Failed to find \'%s\' in %s' % key, main_url)

if scrape.SCRAPER_DEBUG:
    pprint.pprint(("Communities:", community))
        
