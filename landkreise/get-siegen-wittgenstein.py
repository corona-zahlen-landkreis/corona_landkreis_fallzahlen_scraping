import scrape
import helper

url = "https://www.siegen-wittgenstein.de/Startseite/index.php?La=1&object=tx,2170.2450.1&kat=&kuo=2&sub=0&NavID=2170.60.1"
prefix = "Inzwischen gibt es"

scrape.scrape(url, "05970", lambda bs: helper.extract_case_num(bs.text, prefix), name="Kreis Siegen-Wittgenstein")



