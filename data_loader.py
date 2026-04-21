"""
CS5001
Final Project - Data Loader Class
Spring 2026
21 Apr 26
Adele Ka
"""
import csv
import re
from pathlib import Path
from pyproj import Transformer
from park import Park
from crime import Crime


class DataLoader:
    """ Loads the parks and crimes files, cleans the rows, turns them into Park and Crimes objects, and saves the cleaned data into new CSV files."""

    def __init__(self, parks_path="parks.csv", crimes_path="Export.csv"):
        """ Inititalizes the Dataloader with file paths and coordinate converter
            Args:
                parks_path (str): The file path for the parks CSV file.
                crimes_path (str): The file path for the crimes CSV file.
        """
        self.parks_path = Path(parks_path)
        self.crimes_path = Path(crimes_path)
        self.transformer = Transformer.from_crs("epsg:26910", "epsg:4326", always_xy=True)
        self.neighbourhood_mapping = {}

    def load_parks(self):
        """ Reads the parks CSV, parses each row, and stores valid parks in a list.
            Returns: list: A list of parks  
        """
        parks = []
        try:
            with open(self.parks_path, "r", encoding="utf-8-sig") as file:
                reader = csv.DictReader(file, delimiter=";")
                for row in reader:
                    try:
                        park = self.parse_parks(row)
                    except Exception as e:
                        print(f"Skipping bad park row: {e}")
                        continue
                    if park is not None:
                        parks.append(park)
                        self.neighbourhood_mapping[park.neighbourhood.lower()] = park.neighbourhood
        except FileNotFoundError:
            print(f"Error: Could not find parks file: {self.parks_path}")
        except Exception as e:
            print(f"Error reading parks file: {e}")
            
        return parks

    def load_crimes(self):
        """ Reads the crimes CSV, parses each row, cleans column name and stores valid crimes in a list.
            Returns: list: A list of crimes
        """
        crimes = []
        try:
            with open(self.crimes_path, "r", encoding="utf-8-sig") as file:
                reader = csv.DictReader(file)

                reader.fieldnames = [
                    name.strip().replace(":", "").replace(" ", "_").replace("/", "_").lower()
                    for name in reader.fieldnames
                ]

                for row in reader:
                    try:
                        crime = self.parse_crimes(row)
                        if crime is not None:
                            crimes.append(crime)
                    except Exception as e:
                        print(f"Skipping bad crime row: {e}")
        
        except FileNotFoundError:
            print(f"Error: Could not find crimes file: {self.crimes_path}")
        except Exception as e:
            print(f"Error reading crimes file: {e}")
        
        return crimes
    
    def parse_parks(self, row):
        """ Takes a row from parks CSV, extracts and cleans the data and makes a Park Object.
            Args: One row from the parks CSV file.
            Returns: A Park object if the row is valid, otherwise None.
        """
        try:
            name = row["Name"].strip()
            neighbourhood = row["NeighbourhoodName"].strip()
            hectare = float(row["Hectare"]) if row["Hectare"].strip() else 0.0
            latitude, longitude = self.parse_park_coordinates(row["GoogleMapDest"])

            if not name or not neighbourhood or latitude is None or longitude is None:
                return None
            
            return Park(name, neighbourhood, hectare, latitude, longitude)

        except KeyError as e:
            print(f"Missing park column: {e}")
            return None
        except ValueError as e:
            print(f"Bad park number: {e}")
            return None
        except Exception as e:
            print(f"Could not parse park row: {e}")
            return None
     

    def parse_crimes(self, row):
        """ Takes a row from crimes CSV, extracts and cleans the data, converts coordinates, and makes a Crime Object.
            Args: One row from the crimes CSV file.
            Returns: A Crime object if the row is valid, otherwise None.
        """
        try:
            crime_type = row["crime_type"].strip()
            neighbourhood = row["neighbourhood"].strip()
            if neighbourhood == "Central Business District":
                neighbourhood = "Downtown"

            geometry = row["geometry"].strip()
            x, y = self.parse_crime_geometry(geometry)
            if x is None or y is None:
                return None

            latitude, longitude = self.convert_xy_to_latlon(x, y)
            neighbourhood = self.neighbourhood_mapping.get(neighbourhood.lower(), neighbourhood)
            
            return Crime(crime_type, neighbourhood, latitude, longitude)
        
        except KeyError as e:
            print(f"Missing crime column: {e}")
            return None
        except ValueError as e:
            print(f"Bad crime value: {e}")
            return None
        except Exception as e:
            print(f"Could not parse crime row: {e}")
            return None

    def save_parse_data(self, parks, crimes, output_folder="."):
        """ Saves cleaned park and crime data into new CSV files.
            Args:
                parks (list): A list of Park objects.
                crimes (list): A list of Crime objects.
                output_folder (str): The folder where the parsed data will be saved.
        """
        try:   
            parks_file = Path(output_folder) / "parks_parsed.csv"
            crimes_file = Path(output_folder) / "crimes_parsed.csv"

            with open(parks_file, "w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["name", "neighbourhood", "hectare", "latitude", "longitude"])
                for park in parks:
                    writer.writerow([
                        park.name,
                        park.neighbourhood,
                        park.hectare,
                        park.latitude,
                        park.longitude
                    ])

            with open(crimes_file, "w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["crime_type", "neighbourhood", "latitude", "longitude"])
                for crime in crimes:
                    writer.writerow([
                        crime.crime_type,
                        crime.neighbourhood,
                        crime.latitude,
                        crime.longitude
                    ])
        except Exception as e:
            print(f"Error saving parsed {e}")

    def parse_park_coordinates(self, coordinate_text):
        """ Reads latitude and longitude from the park coordinate text.
            Args: coordinate_text (str): The coordinate text from the parks file.
            Returns: tuple: A pair of values in the form (latitude, longitude).
        """
        matches = re.findall(r"-?\d+\.\d+", coordinate_text.strip())
        if len(matches) >= 2:
            return float(matches[0]), float(matches[1])
        return None, None

    def parse_crime_geometry(self, geometry_text):
        """ Reads x and y from the crime geometry text.
            Args: geometry_text (str): The geometry text from the crimes file.
            Returns: tuple: A pair of values in the form (x, y).
        """
        match = re.search(r"X\s*:?\s*([\d\.]+),\s*Y\s*:?\s*([\d\.]+)", geometry_text.strip())
        if match:
            return float(match.group(1)), float(match.group(2))
        return None, None

    def convert_xy_to_latlon(self, x, y):
        """ Converts x and y coordinates to latitude and longitude using the pyproj library.
            Args:
                x (float): The x coordinate from the crime file.
                y (float): The y coordinate from the crime file.
            Returns:tuple: A pair of values in the form (latitude, longitude).
        """
        longitude, latitude = self.transformer.transform(x, y)
        return latitude, longitude
