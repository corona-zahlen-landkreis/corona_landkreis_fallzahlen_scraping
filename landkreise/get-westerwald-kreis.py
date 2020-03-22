import scrape
import helper

url = "https://www.westerwaldkreis.de/aktuelles-detailansicht/gesundheitsamt-informiert.html"

regex = "[0-9]+ bestätigte Fälle im Westerwaldkreis."

date_regex="Abschlussmeldung [0-9]+.[0-9]+.[0-9]+"
date_format = "Abschlussmeldung %d.%m.%Y"

case_func = lambda bs: helper.extract_case_num_directregex(bs.text, regex,0)
date_func = lambda bs: helper.extract_status_date_directregex(bs, date_regex, date_format, 0, "%Y-%m-%d")

scrape.scrape(url, "07143", case_func, date_func)



