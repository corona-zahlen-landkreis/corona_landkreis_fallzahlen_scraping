import scrape
import helper


url = "https://www.regionalverband-saarbruecken.de/corona/"

regex = "gibt es derzeit [0-9]+"

date_regex="Stand: .*? Uhr"
date_format = "Stand: %d. %B, %H Uhr"

case_func = lambda bs: helper.extract_case_num_directregex(bs.text, regex, 0)
date_func = lambda bs: helper.extract_status_date_directregex(bs.text, date_regex, date_format, 0, "2020-%m-%d %H:%M:%S")

scrape.scrape(url, "10041", case_func, date_func, "Saarbrücken Regionalverband")



