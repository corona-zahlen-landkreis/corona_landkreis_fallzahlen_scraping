import re
import datetime
import locale

# NOTE: these have to be sorted, with the most general regex at the bottom!
date_regexes = {
# Stand:14.01.,16:02Uhr
	"Stand:\d+\.\d+\.,\d+:\d+Uhr":"Stand:%d.%m.,%H:%MUhr",
# Stand14.01.,16:02Uhr
        "Stand\d+\.\d+\.,\d+:\d+Uhr":"Stand%d.%m.,%H:%MUhr",
# Stand:14.Januar2020,16Uhr
        "Stand:\d+\.\w+\d+,\d+Uhr" : "Stand:%d.%B%Y,%HUhr",
#Stand1.April2020,16:30Uhr
        "Stand\d+\.\w+\d+,\d+:\d+Uhr" : "Stand%d.%B%Y,%H:%MUhr",

# Stand:14.01.2020,16.20Uhr
	"Stand:\d+\.\d+.\d+,\d+\.\d+Uhr" : "Stand:%d.%m.%Y,%H.%MUhr",
# Stand:14.01.2020,16:20Uhr
        "Stand:\d+\.\d+.\d+,\d+:\d+Uhr" : "Stand:%d.%m.%Y,%H:%MUhr",

# Stand14.01.2020,16.20Uhr
	"Stand\d+\.\d+.\d+,\d+\.\d+Uhr" : "Stand%d.%m.%Y,%H.%MUhr",
# Stand14.01.2020,16:20Uhr
        "Stand\d+\.\d+.\d+,\d+:\d+Uhr" : "Stand%d.%m.%Y,%H:%MUhr",

# Stand:14.Januar,14Uhr
        "Stand:\d+\.\w+,\d+Uhr" : "Stand:%d.%B,%HUhr",
# Stand14.Januar,14Uhr
	"Stand\d+\.\w+,\d+Uhr" : "Stand%d.%B,%HUhr",


# Stand:14.Januar2020;16.20Uhr
	"Stand:\d+\.\w+\d+;\d+\.\d+Uhr" : "Stand:%d.%B%Y;%H.%MUhr",

# mitStandvonFreitag,14.Januar,16.20Uhr
	"mitStandvon\w+,\d+\.\w+,\d+\.\d+Uhr":"mitStandvon%A,%d.%B,%H.%MUhr",

# Stand14.01.2020-16:02Uhr
	"Stand\d+\.\d+\.\d+-\d+:\d+Uhr":"Stand%d.%m.%Y-%H:%MUhr",
# Stand14.01.2020
        "Stand\d+.\d+.\d+" : "Stand%d.%m.%Y",
# Stand:Freitag,14.Januar2020
        "Stand:\w+,\d+\.\w+\d+": "Stand:%A,%d.%B%Y",
# 14.01.2020
	"\d+\.\d+\.\d+":"%d.%m.%Y",
# 14.Januar2020
	"\d+\.\w+\d+":"%d.%B%Y",
# 14. Januar
	"\d+\.\w+":"%d.%B"

    }

def check_and_replace_year(date_string):
    # TODO this is not particular safe, for example if we switched the dateformat to military style.
    if re.match("1900", date_string):
        return date_string.replace("1900", datetime.date.today().strftime("%Y"))
    else:
        return date_string

def extract_case_num(text, prefix):
    cases_raw = text.split(prefix)[1]
    return get_number_only(cases_raw)

def extract_case_num_directregex(text, regex, match):
    cases_raw = re.findall(regex,text)[match]
    return get_number_only(cases_raw)

def extract_status_date(bs, prefix, input_date_format, output_date_format="%Y-%m-%d %H:%M:%S"):
    locale.setlocale(locale.LC_ALL, "de_DE.utf-8")
    status_raw = bs.findAll(text=re.compile(prefix))[0]
    date_string = datetime.datetime.strptime(status_raw, input_date_format).strftime(output_date_format)
    return check_and_replace_year(date_string)

def extract_status_date_directregex(text, regexmatch, input_date_format, match, output_date_format="%Y-%m-%d %H:%M:%S"):
    locale.setlocale(locale.LC_ALL, "de_DE.utf-8")
    status_raw = re.findall(regexmatch,text)[match]
    date_string = datetime.datetime.strptime(status_raw, input_date_format).strftime(output_date_format)
    return check_and_replace_year(date_string)

def clear_text_of_ambigous_chars(text):
    return text.replace("\xa0", " ").replace("\r","\n")

def get_status(text,occurrence=0):
    text = clear_text_of_ambigous_chars(text)
    text = remove_chars_from_text(text,["\n"," "])
    
    äprint(text)

    has_hour=False
    current_find=""
    date=None
    for regex in date_regexes:
        # try to match against the current regex
        try:
            current_find = re.findall(regex, text,re.UNICODE)[occurrence]
            if "%H" in date_regexes.get(regex): has_hour=True
            if(current_find): 
                #if not current_find:
                #    # try dateparser
                #    # NOTE: dateparser is still not very good and requires to remove brackets etc!
                #    from dateparser.search import search_dates
                #    text = remove_chars_from_text(text,["(",")"])
                #    result = search_dates(text, languages=["de"])


                if has_hour:
                    date_format = "%Y-%m-%d %H:%M:%S"
                else:
                    date_format = "%Y-%m-%d"
                # check if there is an hour (if not, do not output any)
                date = datetime.datetime.strptime(current_find,date_regexes.get(regex)).strftime(date_format)   
                break;
        except (IndexError,ValueError) as e:
            pass
        

    if not date:
        raise InvalidDateException(text)
    date = check_and_replace_year(date)       # check if there is a year
    
    return date
       
def remove_chars_from_text(text,what_to_remove):
    for entry in what_to_remove:
        text=text.replace(entry,"")
    return text

def get_number_only(text):
    return int(re.findall("[0-9]+", text)[0])

def get_table(table):
    data = []
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele]) # Get rid of empty values
    return data


class InvalidDateException(Exception):
    def __init__(self, message, text=None):
        super().__init__(message)
        print(text)
