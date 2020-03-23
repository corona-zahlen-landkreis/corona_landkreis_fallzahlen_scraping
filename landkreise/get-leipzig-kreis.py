import helper
import scrape

url = "https://www.landkreisleipzig.de/corona_virus.html"


# Aktuell gibt es 39 bestätigte Infektionsfälle im Landkreis Leipzig. 

def get_recent_press_msg(bs):
    return bs.find_all("div", class_="clearfix article-body-section")[0]

def get_cases(bs):
    msg = str(get_recent_press_msg(bs))
    return helper.extract_case_num(msg, "Aktuell gibt es ")

scrape.scrape(url, "14729", get_cases, name="Kreis Leipzig")
