import scrape
import helper

url = "http://www.landkreis-regensburg.de/unser-landkreis/aktuelles/coronavirus/"

prefix = "Zahl der bestätigten Coronavirus-Fälle im Landkreis Regensburg:"

date_regex="Stand: [0-9]+.[0-9]+.[0-9]+, +[0-9]+:[0-9]+ Uhr"

#Stand: 20.03.2020, 15:00 Uhr
date_format = "Stand: %d.%m.%Y, %H:%M Uhr"

case_func = lambda bs: helper.extract_case_num(bs.text, prefix)
date_func = lambda bs: helper.extract_status_date_directregex(bs.text, date_regex, date_format, 0)

scrape.scrape(url, "09362",case_func, date_func, "Kreis Regensburg")



