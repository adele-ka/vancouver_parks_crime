"""
CS5001
Final Project - Read Me!
Spring 2026
21 Apr 26
Adele Ka
"""
# VANCOUVER PARKS AND CRIME ANALYSIS

This project reads parks data from the City of Vancouver open data portal and crime data from the Vancouver Police Department open data portal. It converts the raw data into Python objects, analyzes the data, and produces a text report, charts, and an interactive map.

The program will:
- Load the parks and crime files.
- Clean and convert the data.
- Analyze parks, crime types, and proximity patterns.
- Print a report to the screen.
- Generate PNG charts.
- Create an HTML Folium map.

## HOW TO RUN

1. Make sure all project files are in the same folder.
2. Open a terminal in that folder.
3. Run the main file:

```bash
python main.py

## DATASETS
parks.csv 
- Source: City of Vancouver Open Data
- Download link: https://opendata.vancouver.ca/explore/dataset/parks/information/?dataChart=eyJxdWVyaWVzIjpbeyJjaGFydHMiOlt7InR5cGUiOiJjb2x1bW4iLCJmdW5jIjoiU1VNIiwieUF4aXMiOiJoZWN0YXJlIiwic2NpZW50aWZpY0Rpc3BsYXkiOnRydWUsImNvbG9yIjoiIzAyNzlCMSJ9XSwieEF4aXMiOiJuZWlnaGJvdXJob29kbmFtZSIsIm1heHBvaW50cyI6NTAsInNvcnQiOiIiLCJzZXJpZXNCcmVha2Rvd25UaW1lc2NhbGUiOiIiLCJjb25maWciOnsiZGF0YXNldCI6InBhcmtzIiwib3B0aW9ucyI6e319fV0sInRpbWVzY2FsZSI6IiIsImRpc3BsYXlMZWdlbmQiOnRydWUsImFsaWduTW9udGgiOnRydWV9

export.csv
- Source: Vancouver Police Department GeoDASH
    Search All Neighbourhoods and select all occurance. Predefined date range "Previous Week"
- Download link: https://geodash.vpd.ca/Html5Viewer/?disclaimer=on&viewer=VPDPublicRefresh_gvh&x=129&y=34

## LIBRARIES
pyproj - pip install pyproj or pip3 install pyproj
matplotlib  — install with  pip install matplotlib 
folium  — install with  pip install folium 

## LIMITATIONS
- It only works with the current CSV file formats.
- If the data format changes, the program may need to be updated.
- Some bad rows may be skipped if the data is missing or not formatted correctly.
- The report is printed in text form only.
- The analysis is basic and only looks at counts, crime types, correlation, and distance to parks.

## FILE SUMMARY
park.py  — stores park data in a class.
crime.py  — stores crime data in a class.
data_loader.py  — loads and cleans the CSV files.
analysis.py  — analyzes the cleaned data.
text_report.py  — runs the program and prints the report.
chart.py  — generates PNG charts.
folium_map.py  — generates the interactive HTML map.
main.py  — runs the full project workflow.

## AI Usage
Perplexity to generate and debug complicated code specifically in `analysis.py`, `chart.py`, `folium_map.py`

##Github Links
Project Link: https://github.com/adele-ka/vancouver_parks_crime/
Project Page: https://adele-ka.github.io/vancouver_parks_crime/
