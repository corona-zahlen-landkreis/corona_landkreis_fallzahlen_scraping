# Web-crawler für Corona-Fallzahlen (Landkreise oder sogar Gemeinden)

## Inspiration
Die offiziellen Daten beim RKI und den Bundesländern sind zum Teil mehrere Tag alt. Was gibt es naheliegenderes, als diese Daten direkt von den Webseiten der Landkreise abzufragen? Dort sind sie "direkt an der Quelle" und am aktuellsten.

Dazu kommt eine Crowdsource-Webseite, auf der aktuelle Fallzahlen pro Landkreis (inkl Quelle) angegeben werden können

## Mitmachen? kein Problem

Sucht die Webseite mit Pressemitteilungen eures Kreises (oder Nachbarkreise) und versucht folgende URLs herauszufinden:
 * Prüft, ob wir die Daten schon einsammel und es einen Kreis ein get-<meinKreis>.py unter landkreise gibt!
 * Falls nicht: Wo stehen für den Kreis, die neusten Corona-Fallzahlen?
   * Nach welchen Worten muss man suchen? (RegEx nehmen wir auch :-) )
 * Gibt es eine Liste (RSS-Feed?) von Pressemittelungen incl. Corona Meldungen? (falls sich die URL jedes Mal ändert?)
 * Optional: Welche URL / Suchwörter liefern die Fallzahlen für die Gemeinden? (Kann auch in den Pressemitteilungen des Kreises oder ähnliches stehen)

## How to start the included API service

[See API README](api/README.md)
Website wo Leute einen Landkreis auswählen können, die aktuelle Fallzahl (inkl Stand) angeben können und Quelle. (Dazu Backend, dass diese Anfragen weiterleitet, mit Möglichkeit, diese anzunehmen, und so die Daten zu übernehmen.)

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
The `districtId` and `communitId` values are declared in `sources.csv` (TODO source?).

districts data:

```landkreise/data/0<districtId>.csv```

community data (aggregates to distrcit - hopefully):
```landkreise/data/0<districtId>/<communityId>.csv```

### Requirements:
* Python3
* Dependencies from `requirements.txt` which can be install as follows:

  - by using pip:
  ```
  pip3 install -r requirements.txt
  ```

  - by using Debian/Ubuntu packages:
  ```
  sudo apt install python3 python3-bs4 python3-cachecontrol python3-lockfile python3-tqdm
  ```

Alternatively, you can use the Dockerfile to build a Docker container which has everything already installed.

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

