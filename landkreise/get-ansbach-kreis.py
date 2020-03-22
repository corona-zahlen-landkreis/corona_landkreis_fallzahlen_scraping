import scrape
import helper


url = "https://www.landkreis-ansbach.de/Quicknavigation/Startseite/Aktuelle-Informationen-zum-Coronavirus.php?object=tx,1503.10.1&ModID=7&FID=2238.2854.1&NavID=2150.1"

regex = "und damit insgesamt [0-9]+"

date_regex="Stand: .*?\)"
date_format = "Stand: %d.%m.%Y)"

case_func = lambda bs: helper.extract_case_num_directregex(bs.text, regex, 0)
date_func = lambda bs: helper.extract_status_date_directregex(bs, date_regex, date_format, 0, "%Y-%m-%d")

scrape.scrape(url, "09571", case_func, date_func)



