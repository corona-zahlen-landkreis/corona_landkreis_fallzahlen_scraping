import re
import datetime

def extract_case_num(text, prefix):
    cases_raw = text.split(prefix)[1]
    return int(re.findall("[0-9]+", cases_raw)[0])

def extract_case_num_directregex(text, regex, match):
    cases_raw = re.findall(regex,text)[match]
    return int(re.findall("[0-9]+", cases_raw)[0])

def extract_status_date(bs, prefix, input_date_format, output_date_format="%Y-%m-%d %H:%M:%S"):
    status_raw = bs.findAll(text=re.compile(prefix))[0]
    return datetime.datetime.strptime(status_raw, input_date_format).strftime(output_date_format)

def extract_status_date_directregex(bs, regexmatch, input_date_format, match, output_date_format="%Y-%m-%d %H:%M:%S"):
    status_raw = re.findall(regexmatch,bs.getText())[match]
    return datetime.datetime.strptime(status_raw, input_date_format).strftime(output_date_format)
