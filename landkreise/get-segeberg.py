import scrape
import helper


# (Labordiagnostisch bestätigt, Stand 21.03.2020)

url = "https://www.segeberg.de/Quicknavigation/Startseite"
prefix = "COVID-19-FÄLLE IM KREIS SEGEBERG:"
prefix_date = "bestätigt, Stand"
date_format = "(Labordiagnostisch bestätigt, Stand %d.%m.%Y)"
case_func = lambda bs: helper.extract_case_num(bs.text, prefix)
date_func = lambda bs: helper.extract_status_date(bs, prefix_date, date_format, "%Y-%m-%d")

scrape.scrape(url, "01060", case_func, date_func, "Kreis Segeberg")



