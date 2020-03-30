from datetime import date, timedelta
from bs4 import BeautifulSoup
import re

import scrape
import helper
from database_interface import *


url = "https://www.landkreis-stade.de/portal/meldungen/coronavirus-aktuelle-lage-informationen-und-hinweise-des-gesundheitsamtes-landkreis-stade-901004416-20350.html?rubrik=901000006"

regex = "[0-9]+ positiv getestete"

req = scrape.request_url(url)
bs = BeautifulSoup(req.text, "html.parser")
text=bs.getText()


# status is always yesterday 18:00
status=(date.today() + timedelta(days=-1)).strftime('%Y-%m-%d 18:00:00')


# todo healed

cases = helper.get_number_only(re.findall(regex,text)[0])

add_to_database("03359", status, cases, "Kreis Stade")



