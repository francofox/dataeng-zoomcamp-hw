#!/bin/sh
python3 pipeline.py --user=root --password=root --host=localhost --port=5432 --dbname=taxis --tblname=green_taxis --csv="`pwd`/green.csv"
python3 pipeline.py --user=root --password=root --host=localhost --port=5432 --dbname=taxis --tblname=zones --csv="`pwd`/zones.csv"

# WINDOWS POWERSHELL:
python pipeline.py --user=root --password=root --host=localhost --port=5432 --dbname=taxis --tblname=green_taxis --csv="$(Get-Location)\green.csv"
python pipeline.py --user=root --password=root --host=localhost --port=5432 --dbname=taxis --tblname=zones --csv="$(Get-Location)\zones.csv"