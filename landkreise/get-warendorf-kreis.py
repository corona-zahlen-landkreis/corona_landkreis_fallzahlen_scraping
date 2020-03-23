import scrape
import helper

url = "https://www.kreis-warendorf.de/aktuelles/startseite/"
#  (Stand 21.03) 
date_regex = r"\(Stand: [0-9]+.[0-9]+.\)"
date_func = lambda bs: helper.extract_status_date_directregex(bs.text, date_regex, "(Stand: %d.%m.)", 0, "2020-%m-%d")

case_regex = r"zählen wir \d+ Infizierte im Kreis" 
case_func = lambda bs: helper.extract_case_num_directregex(bs.text, case_regex, 0)

scrape.scrape(url, "05570", case_func, date_func, name="Kreis Warendorf")
