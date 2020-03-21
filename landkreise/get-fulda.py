import scrape
import helper

main_url = "https://www.landkreis-fulda.de/buergerservice/gesundheit/aktuelles#c11139"
prefix = "gibt es bisher"

scrape.scrape(main_url, "06631", lambda bs: helper.extract_case_num(bs.text, prefix))
