import scrape
import helper

url = "https://www.siegen-wittgenstein.de/Startseite/Informationen-zum-Coronavirus.php?object=tx,2170.14&ModID=7&FID=2170.2450.1&NavID=2170.60"
prefix = "insgesamt"

scrape.scrape(url, "05970", lambda bs: helper.extract_case_num(bs.text, prefix), name="Kreis Siegen-Wittgenstein")



