#!/bin/sh
if type -p python3; then
  # for systems that have only python3 as default
  python() {
    python3 "$@"
  }
else
	echo "WARNING: scripts & libraries require python3!"
fi
python get-nienburg-kreis.py
python get-offenbach.py
python get-offenbach-kreis.py
python get-bodenseekreis.py
python get-ravensburg-kreis.py
python get-tuebingen-kreis.py
python get-warendorf-kreis.py
python get-harburg-kreis.py
python get-ostalbkreis.py
python get-heidenheim.py
python get-albdonaukreis-stadtkreisulm.py
python get-badenbaden-rastatt.py
python get-zollernalbkreis.py
python get-schwaebischhall.py
python get-loerrach.py
python get-freibung-breisgau-hochschwarzwald.py
python get-freudenstadt.py
python get-augsburg-stadt.py
python get-heilbronn.py
python get-rheinneckarkreis-heidelberg.py
python get-muenchen-stadt.py
python get-muenchen-kreis.py
python get-pforzheim-enzkreis.py
python get-reutlingen-kreis.py
python get-recklinghausen-kreis.py
python get-wesel-kreis.py
python get-unna-kreis.py
python get-borken-kreis.py
python get-lippe-kreis.py
python get-erzgebirgskreis.py
python get-emsland-kreis.py
python get-pinneberg-kreis.py
python get-kleve-kreis.py
python get-paderborn-kreis.py
python get-mittelsachsen-kreis.py
python get-neuulm-kreis.py
python get-bayreuth-kreis.py
python get-goerlitz-kreis.py
python get-burgenland-kreis.py
python get-aachen.py
python get-soest.py
python get-westerwald-kreis.py
python get-saarbrücken-regionalverband.py
python get-siegen-wittgenstein.py
python get-ansbach-kreis-stadt.py
python get-kassel-stadt-kreis.py
python get-leer-kreis.py
python get-guetersloh.py
python get-stade-kreis.py
python get-goeppingen.py
python get-hildesheim.py
python get-segeberg.py
python get-mindenluebbecke-kreis.py
python get-giessen.py
python get-steinfurt.py
python get-dresden.py
python get-hamburg.py
python get-leipzig-kreis.py
