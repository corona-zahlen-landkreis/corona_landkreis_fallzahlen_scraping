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
    return int(re.findall("[0-9]+", cases_raw)[0])

def extract_status_date(bs, prefix, input_date_format):
    locale.setlocale(locale.LC_ALL, "de_DE.utf-8")
    status_raw = bs.findAll(text=re.compile(prefix))[0]
    date_string = datetime.datetime.strptime(status_raw, input_date_format).strftime("%Y-%m-%d %H:%M:%S")
    return check_and_replace_year(date_string)

def extract_status_date_directregex(bs, regexmatch, input_date_format, match):
    locale.setlocale(locale.LC_ALL, "de_DE.utf-8")
    status_raw = re.findall(regexmatch,bs.getText())[match]
    date_string = datetime.datetime.strptime(status_raw, input_date_format).strftime("%Y-%m-%d %H:%M:%S")
    return check_and_replace_year(date_string)

