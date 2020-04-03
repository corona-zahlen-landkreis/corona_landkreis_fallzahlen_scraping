#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup

import requests
import datetime
import re

#import sys
#reload(sys) # only on some installations ;-)
#sys.setdefaultencoding('utf-8') # only on some installations ;-)

import scrape
import helper
# for some german month names, e.g. März
import locale
locale.setlocale(locale.LC_ALL, "de_DE.utf-8")

from database_interface import *

# all pages are on this site
site_url = "https://www.kreis-guetersloh.de"

# index page of press release from district assocation
main_url = site_url + "/aktuelles/corona/pressemitteilungen-coronavirus/"
teaser_pattern = "<a.*?Aktuelle Situation im Kreis Gütersloh.*?</a>"
link_pattern = "href=\"(.*?)\""

# pattern to scrap information on press release pages
meta_description_pattern = "<meta name=\"description\" content=\"([\s\S]*?)\"/>"
cases_pattern = "insgesamt ([0-9]+) laborbestätigte"
recover_pattern = "Davon gelten ([0-9]+) Personen als genesen"
table_pattern = "<tbody>[\s\S]*?Anzahl von heute[\s\S]*?</tbody>"
row_pattern = "<tr>([\s\S]*?)</tr>"
col_pattern = "<td><p class=\"paragraph\">([\s\S]*?)</p></td>"

community = {
    'Borgholzhausen': { 'uid': '05754004' },
    'Gütersloh': { 'uid': '05754008' },
    'Halle': { 'uid': '05754012' },
    'Harsewinkel': { 'uid': '05754016' },
    'Herzebrock-Clarholz': { 'uid': '05754020' },
    'Langenberg': { 'uid': '05754024' },
    'Rheda-Wiedenbrück': { 'uid': '05754028' },
    'Rietberg': { 'uid': '05754032' },
    'Schloß Holte-Stukenbrock': { 'uid': '05754036' },
    'Steinhagen': { 'uid': '05754040' },
    'Verl': { 'uid': '05754044' },
    'Versmold': { 'uid': '05754048' },
    'Werther': { 'uid': '05754052' }
}

def getPage(url, parsed):
    req = scrape.request_url(url)
    text = req.text
    if parsed:
        text = BeautifulSoup(text, "html.parser")
    #text=text.decode("UTF-8").encode("UTF-8") # only on some installations ;-)
    return text
    

def getStatusDate(string):
    status_raw = re.findall("zum Stand .*? Uhr", string)

    if len(status_raw) == 1:
        statusDate = helper.get_status(status_raw[0].replace("zum Stand ",""))
        return statusDate

def findNumber(pattern, string):
    number_raw = re.findall(pattern, string)
    if len(number_raw) == 1:
        return int(number_raw[0])

overviewPage = getPage(main_url, False)

teaser_raw = re.findall(teaser_pattern, overviewPage)

for one_teaser in teaser_raw:
    one_page_url = re.findall(link_pattern, one_teaser)
    if len(one_page_url) == 1:
        url = site_url + one_page_url[0]
        one_page = getPage(url, False)
        one_meta_description = re.findall(meta_description_pattern, one_page)
        if len(one_meta_description) == 1:
            statusDate = getStatusDate(one_meta_description[0])

            if statusDate != None:
                status = statusDate

                cases = findNumber(cases_pattern, one_meta_description[0])
                recovered = findNumber(recover_pattern, one_meta_description[0])
                if cases != None:
                    add_to_database("05754", status, cases, "Kreis Gütersloh")

                table_raw = re.findall(table_pattern, one_page)
                if len(table_raw) == 1:
                    rows = re.findall(row_pattern, table_raw[0])
                    for row in rows:
                        cols = re.findall(col_pattern, row)
                        if len(cols) == 3:
                            city = cols[0]
                            today = cols[1]
                            yesterday = cols[2]
                            if city in community and today != None:
                                    add_to_database(community[city]['uid'], status, today, "Kreis Gütersloh, Stadt " + city, "05754")

        else:
            print("do not have exactly one meta description: " + str(len(one_meta_description)))    
    else:
        print("do not have exactly one 'href': " + str(len(one_page_url)))
