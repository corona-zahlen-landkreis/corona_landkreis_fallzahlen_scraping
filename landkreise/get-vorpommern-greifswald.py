from bs4 import BeautifulSoup

import requests
import datetime
import re
import locale


locale.setlocale(locale.LC_TIME, "de_DE.utf-8")
import helper
import scrape

from database_interface import *

def cleanOverview(overview):
    return overview.replace('\n\n', '\n').replace('+\n','').replace('+','')
    
def cleanLine(line):
    line=line.replace('Fälle','').strip()
    return line

main_url = "https://www.kreis-vg.de/'/index.php?object=tx%7C3079.14723.1%27"

req = scrape.request_url(main_url)

bs = BeautifulSoup(req.text, "html.parser")

cases_overview = cleanOverview(bs.findAll(text="Lagebericht und Entwicklung im Landkreis Vorpommern-Greifswald")[0].parent.parent.find('div', {'class':'toggler-container'}).getText())

for line in cases_overview.splitlines():
    line = cleanLine(line)
    status,cases=line.split(" ")
    status = datetime.datetime.strptime(status, '%d.%m.%Y').strftime("%Y-%m-%d")
    cases = int(cases)
    add_to_database("13075", status, cases, "Kreis Vorpommern-Greifswald")

