#!/usr/bin/env python3

import locale
import datetime
import requests

from database_interface import add_to_database

MAIN_URL = ("https://services.arcgis.com/ORpvigFPJUhb8RDF/arcgis/rest/services/corona_DD_sicht2/"
            "FeatureServer/0/query?f=json&where=Fallzahl%20IS%20NOT%20NULL&returnGeometry=false&"
            "spatialRel=esriSpatialRelIntersects&outFields=*&resultOffset=0&resultRecordCount=2000"
            "&cacheHint=true")


def get_dresden():
    """
    Dresdener Daten beziehen.
    """
    locale.setlocale(locale.LC_TIME, "de_DE.utf-8")
    response = requests.get(MAIN_URL)
    if response.status_code != 200:
        raise Exception("No response.")
    jsn = response.json()

    # note special char
    features = jsn['features']
    current_feature = features[len(features)-1]
    status = datetime.datetime.strptime(current_feature['attributes']['Datum'],
                                        '%d.%m.%y').strftime("20%y-%m-%d 12:00")
    cases = int(current_feature['attributes']['Fallzahl'])

    # debugging: print("14612000", status, cases, "Stadt Dresden")
    add_to_database("14612000", status, cases, "Stadt Dresden")


if __name__ == "__main__":
    get_dresden()
