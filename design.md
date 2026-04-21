"""
CS5001
Final Project - Design
Spring 2026
21 Apr 26
Adele Ka
"""
## Project Intent
This project looks at park and crime data in Vancouver. The program reads the data from CSV files, turns each row into objects, studies the data, and prints a report. The main classes are `Park`, `Crimes`, `DataLoader`, and `Analysis`.

## Park Class
The `Park` class stores information about one park. Its job is to hold the park’s name, neighbourhood, size in hectares, latitude, and longitude. The main methods are `__init__` to create the object, `to_dict` to turn it into a dictionary, and `__str__` to show it as a simple string.

## Crime Class
The `Crime` class stores information about one crime. Its job is to hold the crime type, neighbourhood, latitude, and longitude. The main methods are `__init__` to create the object, `to_dict` to turn it into a dictionary, and `__str__` to show it as a simple string.

## Data Loader Class
The `DataLoader` class reads the CSV files and turns the rows into `Park` and `Crimes` objects. Its main job is to clean the data and get it ready for the program to use. Important attributes are the parks file path, crimes file path, the coordinate transformer, and the neighbourhood mapping dictionary. Methods are `load_parks`, `load_crimes`, `parse_parks`, `parse_crimes`, `parse_park_coordinates`, `parse_crime_geometry`, `convert_xy_to_latlon`, and `save_parse_data`.

## Analysis Class
The `Analysis` class looks at the parks and crimes data and finds useful results. Its job is to count things, compare neighbourhoods, and measure how close crimes are to parks. Its main attributes are the list of parks and the list of crimes. Methods are `dataset_summary`, `parks_by_neighbourhood`, `crimes_by_neighbourhood`, `crime_type_counts`, `neighbourhood_with_most_parks`, `neighbourhood_with_most_crime`, `most_common_crime_type`, `park_crime_correlation`, `haversine_distance_meters`, `crime_proximity_to_parks`, and `full_report`.

## Text Report
The `text_report` module prints the final text report for the project. Its main function is `print_report`, which displays the data summary, meaningful insights, and cross-data-set analysis in a clean format. This module is used to present the results in a readable way in the terminal or console.

## Chart
The `chart` module creates visual summaries of the data as PNG image files. It generates charts showing the number of parks by neighbourhood, crime counts by crime type, the relationship between parks and crimes by neighbourhood, and the number of crimes near parks by distance radius. Its main functions are `sorted_counts` and `make_charts`.

## Folium Map
The `folium_map` module creates an interactive HTML map for the project. The map displays Vancouver parks and nearby crimes, and it includes custom search tools that allow the user to search by park or neighbourhood. It also shows park details, crime markers, and radius circles to help visualize how close crimes are to each selected park.

## How the files work together
The project files work together in a sequence. First, `DataLoader` reads the CSV files and creates `Park` and `Crime` objects from the raw data. Next,`Analysis` uses those objects to calculate totals, patterns, and comparisons. Then, `text_report`  prints the written summary, `chart` creates the PNG charts, and `folium_map` builds the interactive HTML map. Together, these files create a complete report of Vancouver parks and the proximity of crimes to each park.