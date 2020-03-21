from bs4 import BeautifulSoup

import requests
import datetime
import re
import time

from database_interface import *

def time_stamp():
    return time.strftime("%Y-%m-%d %H:%M:%S")

def scrape(url, community_id, cases_func, date_func = None):
    req = requests.get(url)
    bs = BeautifulSoup(req.text, "html.parser")
    date = time_stamp() if date_func is None else date_func(bs)
    cases = cases_func(bs)
    add_to_database(community_id, date, cases)


