import scrape
import helper


url = "https://www.landkreis-stade.de/portal/meldungen/coronavirus-aktuelle-lage-informationen-und-hinweise-des-gesundheitsamtes-landkreis-stade-901004416-20350.html?rubrik=901000006"

regex = "[0-9]+ COVID-"

date_regex="Stand .*?:[0-9]+"
date_format = "Stand %d. %B %H:%M"

# todo healed

case_func = lambda bs: helper.extract_case_num_directregex(bs.text, regex, 0)
date_func = lambda bs: helper.extract_status_date_directregex(bs.text, date_regex, date_format, 0, "2020-%m-%d %H:%M:%S")

scrape.scrape(url, "03359", case_func, date_func)



