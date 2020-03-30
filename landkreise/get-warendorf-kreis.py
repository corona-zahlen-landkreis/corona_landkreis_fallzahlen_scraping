from bs4 import BeautifulSoup
import re

import scrape
import helper
from database_interface import * 

url = "https://www.kreis-warendorf.de/aktuelles/startseite/"

date_regex = r"\(Stand: .*?\)"


req = scrape.request_url(url)
bs = BeautifulSoup(req.text,"html.parser")

text=bs.getText()



status = helper.get_status(re.findall(date_regex,text)[0].replace("(","").replace(")",""))

case_regex = r"zählen wir \d+ Infizierte im Kreis" 

cases = helper.extract_case_num_directregex(text, case_regex, 0)

add_to_database("05570", status, cases, "Kreis Warendorf")
