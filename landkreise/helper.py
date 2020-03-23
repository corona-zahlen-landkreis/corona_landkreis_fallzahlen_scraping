import re
import datetime
import locale


def check_and_replace_year(date_string):
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
