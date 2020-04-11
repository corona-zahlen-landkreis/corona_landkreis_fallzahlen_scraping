from bs4 import BeautifulSoup

import datetime
import scrape
import locale
import json

locale.setlocale(locale.LC_TIME, "de_DE.utf-8")

from database_interface import *

main_url = "https://webgis.lk-ni.de/arcgis/rest/services/opengov/Corona_StatusQuo/MapServer/0/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=Tagesdatum%20desc"

req = scrape.request_url(main_url)
bs = BeautifulSoup(req.text, "html.parser")
text = bs.get_text()

#get json object
json_data = json.loads(text)

cases = json_data["features"][0]["attributes"]["Faelle_bestaetigt"]
unix_timestamp = int(json_data["features"][0]["attributes"]["Tagesdatum"])
unix_timestamp /= 1000

#convert unix to date
status = datetime.datetime.fromtimestamp(unix_timestamp).strftime("%Y-%m-%d")

add_to_database("03256", status, cases, "Landkreis Nienburg/Weser")