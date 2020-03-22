
import re
import scrape
import helper


def find_cases_in_table(bs):
    table = bs.findAll('tbody')[0]
    row = table.findAll('tr')[3]
    cell = re.findall(r'\d+', str(row.findAll('strong')[0]))[0]
    return int(cell)

main_url = "https://www.minden-luebbecke.de/Startseite/Informationen-zum-Coronavirus/index.php?La=1&object=tx,2832.3003.1&kat=&kuo=2&sub=0"

# Aktuelle Fallzahlen (Stand 22.3.2020, 11 Uhr)
date_func = lambda bs: helper.extract_status_date(bs, "Aktuelle Fallzahlen \(", "Aktuelle Fallzahlen (Stand %d.%m.%Y, %H Uhr)")  
scrape.scrape(main_url, "05770", find_cases_in_table, date_func, name="Minden-Luebbecke")

