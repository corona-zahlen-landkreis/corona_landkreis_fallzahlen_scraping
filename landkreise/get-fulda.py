import re
import scrape

def cases_func(bs):
    cases_raw = bs.text.split("gibt es bisher")[1]
    return int(re.findall("[0-9]+", cases_raw)[0])

main_url = "https://www.landkreis-fulda.de/buergerservice/gesundheit/aktuelles#c11139"

scrape.scrape(main_url, "06631", cases_func)
