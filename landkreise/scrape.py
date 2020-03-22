from bs4 import BeautifulSoup

import requests
import datetime
import re
import time
import random
import requests
import cachecontrol
from cachecontrol.caches.file_cache import FileCache
import pathlib
import logging

import locale
locale.setlocale(locale.LC_TIME, "de_DE.utf-8")
from database_interface import *

SCRAPER_DEBUG='SCRAPER_DEBUG' in os.environ and os.environ['SCRAPER_DEBUG'] == 'yes'

if SCRAPER_DEBUG:
  logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

USER_AGENTS = [
        # GPLv3: Taken from https://gitlab.com/ntninja/user %s/\([^\/]\+\/ [^:]\+\): \(.\+\)$/\t'\2', #\1/g-agent-switcher/-/blob/master/assets/user-agents.txt
        # conversion regex: %s/\([^\/]\+\/ [^:]\+\): \(.\+\)$/\t'\2', #\1/g %s/\([^\/]\+\/ [^:]\+\): \(.\+\)$/\t'\2', #\1/g
        #Note: Browser version data is semi-regularily updated based on the version data %s/\([^\/]\+\/ [^:]\+\): \(.\+\)$/\t'\2', #\1/g
        #      available through WikiData's SPARQL data service %s/\([^\/]\+\/ [^:]\+\): \(.\+\)$/\t'\2', #\1/g
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0', #Windows / Firefox 74 [Desktop]
	'Mozilla/5.0 (X11; Linux x86_64; rv:74.0) Gecko/20100101 Firefox/74.0', #Linux / Firefox 74 [Desktop]
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.1 Safari/605.1.15', #Mac OS X / Safari 12 [Desktop]
	'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko', #Windows / IE 11 [Desktop]
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17763', #Windows / Edge 44 [Desktop]
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36', #Windows / Chrome 80 [Desktop]
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.8) Gecko/20100101 Firefox/60.8', #Windows / Firefox 60 ESR [Desktop]

	'Mozilla/5.0 (Android 10; Mobile; rv:74.0) Gecko/74.0 Firefox/74.0', #Android Phone / Firefox 74 [Mobile]
	'Mozilla/5.0 (Linux; Android 10; Z832 Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Mobile Safari/537.36', #Android Phone / Chrome 80 [Mobile]
	'Mozilla/5.0 (Android 10; Tablet; rv:74.0) Gecko/74.0 Firefox/74.0', #Android Tablet / Firefox 74 [Mobile]
	'Mozilla/5.0 (Linux; Android 10; SAMSUNG-SM-T377A Build/NMF26X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Mobile Safari/537.36', #Android Tablet / Chrome 80 [Mobile]
	'Mozilla/5.0 (iPhone; CPU OS 10_15_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.1 Mobile/14E304 Safari/605.1.15', #iPhone / Safari 12.1.1 [Mobile]
	'Mozilla/5.0 (iPad; CPU OS 10_15_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.1 Mobile/15E148 Safari/605.1.15', #iPad / Safari 12.1.1 [Mobile]

        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0',
        ]
headers = {
    'User-Agent': USER_AGENTS[random.randrange(0, len(USER_AGENTS), 1)] 
}

RANDOM_CLIENT_HEADERS=headers

def time_stamp():
    return time.strftime("%Y-%m-%d")

# def extract_case_num(text, prefix):
#     cases_raw = text.split(prefix)[1]
#     return int(re.findall("[0-9]+", cases_raw)[0])   

# Options: debug, cookies
def scrape(url, community_id, cases_func, date_func = None, name="", parent_community_id=None, options={'debug':SCRAPER_DEBUG}):
    req = request_url(url,headers=RANDOM_CLIENT_HEADERS, options=options)
    logger.debug("%s(%s): Request to %s with user-agent: %s" % (name, parent_community_id, url, headers['User-Agent']))
    bs = BeautifulSoup(req.text, "html.parser")
    if options.get('debug'):
        logger.debug(repr(bs.text))
    date = time_stamp() if date_func is None else date_func(bs)
    cases = cases_func(bs)
    if options.get('debug'):
        logger.debug(str(cases) + " Fälle am " + date)
    else:
        add_to_database(community_id, date, cases, name, parent_community_id)

def request_cache():
    data_dir = pathlib.Path(__file__).parent.joinpath('data')
    cache_dir = data_dir.joinpath('.webcache').absolute()
    disk_cache = FileCache(cache_dir, forever=True)
    logger.debug(cachecontrol.caches.file_cache.url_to_file_path('https://google.com', disk_cache))
    return cachecontrol.CacheControl(requests.Session(), cache=disk_cache)

def request_url(url,headers=RANDOM_CLIENT_HEADERS,options={}):
    resp = request_cache().get(url, headers=headers, cookies=options.get('cookies'))
    if options.get('forceEncoding') != None:
        logger.debug('Forcing encoding to: %s' % options.get('forceEncoding'))
        resp.encoding = options.get('forceEncoding')
    return resp

