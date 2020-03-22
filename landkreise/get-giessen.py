import scrape
import helper

url = "https://www.lkgi.de/gesundheit-und-soziales/3060-gesundheitsamt-informiert-br-ueber-coronavirus"
#  (Stand 21. März) 
date_regex = r"wurden \(Stand \d\d\. [^0-9]+\) insgesamt"
date_func = lambda bs: helper.extract_status_date_directregex(bs.text, date_regex, "wurden (Stand %d. %B) insgesamt", 0)

case_regex = r"insgesamt \d+ Fälle des Coronavirus" 
case_func = lambda bs: helper.extract_case_num_directregex(bs.text, case_regex, 0)

scrape.scrape(url, "06531", case_func, date_func, name="Gießen")
