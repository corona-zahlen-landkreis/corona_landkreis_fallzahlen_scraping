from bs4 import BeautifulSoup

import scrape
import helper
import requests
import datetime
import re

import locale
import logging
import urllib.parse
from helper import ParsingError,parse_dateheader

locale.setlocale(locale.LC_TIME, "de_DE.utf-8")

logger = logging.getLogger(__name__)

from database_interface import *

def generate_urls():
    corona_pattern = 'Corona'
    main_url = "https://www.kreis-paderborn.de/kreis_paderborn/aktuelles/pressemitteilungen/2018/"
    req = scrape.request_url(main_url)
    bs = BeautifulSoup(req.text, "html.parser")

    links = bs.find_all('a')
    urls = [urllib.parse.urljoin(main_url, link['href']) for link in links if corona_pattern in link.text]
    return urls

urls=generate_urls()
logger.info('Found %s press releases' % len(urls))
logger.debug('URLs: %s' % "\n".join(urls))

date_regex = "Stand: .*? Uhr"
date_formats = 'Stand: %A, %d.%m.%Y -  %H:%M Uhr', \
               'Stand: %d.%m., %H.%M Uhr', \
               'Stand: %d. %B, %H:%M Uhr', \
               'Stand: %d. %B, %H.%M Uhr', \
               'Stand: %d.%m., Zeit %H Uhr', \
               'Stand: %d.%m., %H Uhr'
#date_convert = helper.genfunc_dateformats_parser(datetime.datetime.now(), *date_formats)

#HEAD#cases_pattern = "sind insgesamt [0-9]+"
community_matcher = [
        { 'cid': '05774'       , 'name': 'Kreis Paderborn'         , 'regex': '[0-9]+\s+bestätigte'        , 'parent': None   },
        { 'cid': '057740004004', 'name': 'Altenbeken'              , 'regex': 'Altenbeken[:\s]+[0-9]+'     , 'parent': '05774'},
        { 'cid': '057740008008', 'name': 'Bad Lippspringe, Stadt'  , 'regex': 'Lippspringe[:\s]+[0-9]+'    , 'parent': '05774'},
	{ 'cid': '057740012012', 'name': 'Borchen'                 , 'regex': 'Borchen[:\s]+[0-9]+'        , 'parent': '05774'},
	{ 'cid': '057740016016', 'name': 'Büren, Stadt'            , 'regex': 'Büren[:\s]+[0-9]+'          , 'parent': '05774'},
	{ 'cid': '057740020020', 'name': 'Delbrück, Stadt'         , 'regex': 'Delbrück[:\s]+[0-9]+'       , 'parent': '05774'},
	{ 'cid': '057740024024', 'name': 'Hövelhof, Sennegemeinde' , 'regex': 'Hövelhof[:\s]+[0-9]+'       , 'parent': '05774'},
	{ 'cid': '057740028028', 'name': 'Lichtenau, Stadt'        , 'regex': 'Lichtenau[:\s]+[0-9]+'      , 'parent': '05774'},
	{ 'cid': '057740032032', 'name': 'Paderborn, Stadt'        , 'regex': 'Paderborn[:\s]+[0-9]+'      , 'parent': '05774'},
	{ 'cid': '057740036036', 'name': 'Salzkotten, Stadt'       , 'regex': 'Salzkotten[:\s]+[0-9]+'     , 'parent': '05774'},
	{ 'cid': '057740040040', 'name': 'Bad Wünnenberg, Stadt'   , 'regex': 'Bad Wünnenberg[:\s]+[0-9]+' , 'parent': '05774'}
]
#Bad Lippspringe: 1,
#Bad Wünnenberg: 14,
#Borchen: 1,
#Büren: 4,
#Delbrück: 15,
#Hövelhof: 9,
#Lichtenau: 1,
#Paderborn 50 und
#Salzkotten: 8

#    for date_format in date_formats:
#        try:
#            helper.extract_status_date_directregex(bs.text, date_regex, date_format, 0, "%Y-%m-%d")
#        except e:
#            logger.debug(e)
#            pass
known_broken_urls=["https://www.kreis-paderborn.de/kreis_paderborn/wirtschaft/Corona-Unterstuetzung-Unternehmen/Corona-Unterstuetzung-Unternehmen.php"]
for url in urls:
    for community in community_matcher:
        try:
            case_func = lambda bs: helper.extract_case_num_directregex(bs.text, community['regex'],0,url)
            date_func = lambda bs, default: helper.extract_status_date_directregex(bs.text, date_regex, helper.genfunc_dateformats_parser(default, *date_formats), 0, "%Y-%m-%d", url)
            scrape.scrape(url, community['cid'], case_func, date_func, community['name'], community['parent'])
        except ParsingError as e:
            if url not in known_broken_urls:
                logger.error(e)
