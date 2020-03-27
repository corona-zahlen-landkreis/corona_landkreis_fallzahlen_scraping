import re
import datetime
import locale

# NOTE: these have to be sorted, with the most general regex at the bottom!
date_regexes = {
	"Stand:\d+\.\w+,\d+Uhr" : "Stand:%d.%B,%HUhr",

	"Stand:\d+\.\d+.\d+,\d+\.\d+Uhr" : "Stand:%d.%m.%Y,%H.%MUhr",
	"Stand\d+\.\d+.\d+,\d+\.\d+Uhr" : "Stand%d.%m.%Y,%H.%MUhr",
	
	"Stand:\d+\.\w+\d+;\d+\.\d+Uhr" : "Stand:%d.%B%Y;%H.%MUhr",


	"Stand\d+\.\d+\.\d+-\d+:\d+Uhr":"Stand%d.%m.%Y-%H:%MUhr",
    "Stand\d+.\d+.\d+" : "Stand%d.%m.%Y",
	"\d+\.\d+\.\d+":"%d.%m.%Y"

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

def extract_status_date(bs, prefix):
    locale.setlocale(locale.LC_ALL, "de_DE.utf-8")
    status_raw = bs.findAll(text=re.compile(prefix))[0]
    return get_status(status_raw)

def extract_status_date_directregex(text, regexmatch, match):
    locale.setlocale(locale.LC_ALL, "de_DE.utf-8")
    status_raw = re.findall(regexmatch,text)[match]
    return get_status(status_raw)

def clear_text_of_ambigous_chars(text):
    return text.replace("\xa0", " ").replace("\r","\n")

def get_status(text,occurrence=0):
    text = clear_text_of_ambigous_chars(text)
    text = remove_chars_from_text(text,["\n"," "])
    #print(text)

    has_hour=False
    current_find=""
    for regex in date_regexes:
        # try to match against the current regex
        try:
            current_find = re.findall(regex, text,re.UNICODE)[occurrence]
            if "%H" in date_regexes.get(regex): has_hour=True
            if(current_find): break;
        except IndexError:
            pass
        
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
