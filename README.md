# Web-crawler for Corona case numbers in germany (county or sub-county level)

**67** Landkreise/Stadtkreis/Kreisfreihe Städte  are currently supported. 

**6** of those also have sub-county (Stadt/Gemeinde) level support.

**WE NEED YOUR HELP 🙌**

## Inspiration
RKI's and state's data is most of the times multiple days old
The official data at the RKI and the federal states are sometimes several days old. What could be more obvious than to retrieve this data directly from the websites of the administrative districts (county)? There they are "directly at the source" and most up-to-date.

In addition, there is a crowdsource website on which current case numbers per county (including source) can be given. (currently in the works)

## Want to participate? No problem!

Search the website with press releases from your district (or neighboring districts) and try to find the following URLs:
 * Check, if we already collect the data and there is a district in landkreise/get-<mydistrict>.py!
 * If not: Where are the newest corona-case numbers for your district?
   * For which words do we have to search? (we also take RegEx :-) )
 * Is there a list (RSS-Feed?) of press releases including corona messages? (in case the URL is changing all the time?)
 * Optional: With which URL/search words do we get the case numbers at sub-county level? (might be in the press releases of the district)

## How to start the included API service

[See API README](api/README.md)
Website where people can choose a district, enter the current case number (including status date) and source. (and a backend which forwards these requests with the possibility to access these data and include it in the data set.)

## How to use the web-crawler - scraper

Scraper that also generates community level output:
```
./run.sh
# or to update a single district / community
# run any of the get-<location>.py files
python3 landkreise/get-soest.py
```

Newer abstracted scraper (depend on scraper.py):
```
# SCRAPER debug mode/logging can be enabled as follows
SCRAPER_DEBUG=yes python3 landkreise/get-fulda.py
``` 

The result data is saved in `landkreise/data/` as CSV files.
Each CSV file is named by it's official Id.
The `districtId` and `communitId` Ids can be looked up in [sources.csv](https://github.com/corona-zahlen-landkreis/corona_landkreis_fallzahlen_scraping/blob/895afda1da29f1f00c2845617effdcd0011a469a/sources.csv) OR in JSON [location.json](api/db/raw-data/locations.json) (Replacement for sources.csv in master). The district/community unique Ids are the official identifier from https://de.wikipedia.org/wiki/Amtlicher_Gemeindeschl%C3%BCssel.

districts data:

```landkreise/data/0<districtId>.csv```

community data (aggregates to distrcit - hopefully):
```landkreise/data/0<districtId>/<communityId>.csv```

### Requirements:
  * Python3
    * requests (often included)
    * CacheControl[filecache] (persistent cache does not work yet)
      * lockfile
    * beautiful soup 4
    * running all scrapers tqdm

pip3 line:
```
pip3 install requests bs4 cachecontrol[filecache] lockfile tqdm
```

Debian/Ubuntu packages:
```
  sudo apt-get install python3 python3-bs4 python3-cachecontrol python3-lockfile python3-tqdm
```

  * Makefile for Docker container also exists

### Writing / Mainting a scraper

Newer abstracted scraper:
```
# For all scrapers that are migrted to use scraper.py:
#   request will be cached automatically
#   user-agents will rotate
#   debug mode
#
# SCRAPER debug mode/logging can be enabled as follows
SCRAPER_DEBUG=yes python3 landkreise/get-fulda.py
```

New scrapers should use scraper.py and use request_url to load URLs.
This should cache the website responses and reduce data-transfers.
Also the user-agent should rotate at least for every scraper start.

# unparsable Landkreise
It would be nice, if you would check these for new data and open a PR!


| name | website   | id |
|---|---| --- |
|Kreis Vorpommern-Greifswald  | https://www.kreis-vg.de/'/index.php?object=tx%7C3079.14723.1%27   | 13075 |
|   |   | |
|   |   | |

For more, see the project tab!

