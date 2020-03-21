import re
import datetime

def extract_case_num(text, prefix):
    cases_raw = text.split(prefix)[1]
    return int(re.findall("[0-9]+", cases_raw)[0])

def extract_status_date(bs, prefix, input_date_format):
    status_raw = bs.findAll(text=re.compile(prefix))[0]
    return datetime.datetime.strptime(status_raw, input_date_format).strftime("%Y-%m-%d %H:%M:%S")