import helper
import scrape

url = "https://landkreis-cuxhaven.de/Quicknavigation/Startseite/index.php?La=1&object=tx,3189.730.1&kat=&kuo=2&sub=0"


# Stand: 22.03.2020, 12:30 Uhr Aktuelle Zahl der Infektionen: Zahl der Infizierten: 34 ( = plus 2 im Vergleich zu gestern) Zahl der noch Erkrankten: 32 (= plus 4 im Vergleich zu gestern) 
def get_recent_press_msg(bs):
    return bs.find_all("div", class_="liste_text")[1]
    


def get_cases(bs):
    msg = str(get_recent_press_msg(bs))
    return helper.extract_case_num(msg, "Zahl der Infizierten:")

def get_date(bs):
    msg = str(get_recent_press_msg(bs))
    return helper.extract_status_date_directregex(msg, r"Stand: \d\d\.\d\d\.\d{4}, \d\d:\d\d Uhr", "Stand: %d.%m.%Y, %H:%M Uhr", 0)

scrape.scrape(url, "03352011", get_cases, get_date, name="Cuxhaven", options={'cookies': {'ikiss-modal-window-off': '1'}})
