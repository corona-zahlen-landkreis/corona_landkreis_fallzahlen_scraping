from bs4 import BeautifulSoup
import re
import scrape
import helper
from database_interface import *

main_url = "https://www.minden-luebbecke.de/Startseite/Informationen-zum-Coronavirus/index.php?La=1&object=tx,2832.3066.1&kat=&kuo=2&sub=0"


req = scrape.request_url(main_url)
bs = BeautifulSoup(req.text, 'html.parser')

table = bs.find('table')
data = helper.get_table(table)

data_line = data[2]

cases = data_line[0]
healed= data_line[1]
deaths = data_line[2]

status_raw = re.findall("\(\d+\.\d+\., \d+ Uhr\)",bs.text)[0].replace("(","").replace(")","")
status = helper.get_status(status_raw)

add_to_database("05770", status, cases, name="Minden-Luebbecke")

