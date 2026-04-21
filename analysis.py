"""
CS5001
Final Project - Analysis Class
Spring 2026
21 Apr 26
Adele Ka
"""
from math import radians, sin, cos, sqrt, atan2

class Analysis:
    """Performs analysis on park and crime objects to make summaries and compare the two datasets."""
    
    def __init__(self, parks, crimes):
        """ Initializes the analysis object with the given parks and crimes data.
            Args:
                parks (list): A list of Park objects.
                crimes (list): A list of Crimes objects.
        """
        self.parks = parks
        self.crimes = crimes

    def dataset_summary(self):
        """ Counts the total number of parks and crimes.
            Returns: dict: A dictionary with the total parks count and crimes count.
        """
        return {
            "parks_count": len(self.parks),
            "crimes_count": len(self.crimes)
        }

    def parks_by_neighbourhood(self):
        """ Counts how many parks are in each neighbourhood.
            Returns: dict: A dictionary where the key is the neighbourhood and the value is the number of parks.
        """
        counts = {}
        for park in self.parks:
            counts[park.neighbourhood] = counts.get(park.neighbourhood, 0) + 1
        return counts

    def crimes_by_neighbourhood(self):
        """ Counts how many crimes are in each neighbourhood.
            Returns: dict: A dictionary where the key is the neighbourhood and the value is the number of crimes.
        """
        counts = {}
        for crime in self.crimes:
            counts[crime.neighbourhood] = counts.get(crime.neighbourhood, 0) + 1
        return counts

    def crime_type_counts(self):
        """ Counts how many times each crime type appears.
            Returns: dict: A dictionary where the key is the crime type and the value is the number of crimes.
        """
        counts = {}
        for crime in self.crimes:
            counts[crime.crime_type] = counts.get(crime.crime_type, 0) + 1
        return counts

    def neighbourhood_with_most_parks(self):
        """ Finds the neighbourhood with the most parks.
            Returns: tuple: The neighbourhood name and the park count.
        """
        counts = self.parks_by_neighbourhood()
        if not counts:
            return None, 0
        name = max(counts, key=counts.get)
        return name, counts[name]

    def neighbourhood_with_most_crime(self):
        """ Finds the neighbourhood with the most crime.
            Returns: tuple: The neighbourhood name and the crime count.
        """
        counts = self.crimes_by_neighbourhood()
        if not counts:
            return None, 0
        name = max(counts, key=counts.get)
        return name, counts[name]

    def most_common_crime_type(self):
        """ Finds the crime type that appears the most. 
            Returns: tuple: The crime type and its count.
        """
        counts = self.crime_type_counts()
        if not counts:
            return None, 0
        crime_type = max(counts, key=counts.get)
        return crime_type, counts[crime_type]

    def park_crime_correlation(self):
        """ Calculates the correlation between park count and crime count. This method compares neighbourhood park totals to neighbourhood 
            crime totals to see if they move together.
            Returns: float: The correlation value.
        """
        park_counts = self.parks_by_neighbourhood()
        crime_counts = self.crimes_by_neighbourhood()
        neighbourhoods = sorted(set(park_counts) | set(crime_counts))

        x_values = [] # park counts
        y_values = [] # crime counts
        for neighbourhood in neighbourhoods:
            x_values.append(park_counts.get(neighbourhood, 0))
            y_values.append(crime_counts.get(neighbourhood, 0))

        if len(x_values) < 2: #correlation needs at least 2 data points
            return 0.0

        x_mean = sum(x_values) / len(x_values) # average park count by neighbourhood
        y_mean = sum(y_values) / len(y_values) # average crime count by neighbourhood

        numerator = 0 #push together score
        x_diff_sq = 0
        y_diff_sq = 0

        for x, y in zip(x_values, y_values):
            x_diff = x - x_mean
            y_diff = y - y_mean
            numerator += x_diff * y_diff
            x_diff_sq += x_diff ** 2
            y_diff_sq += y_diff ** 2

        denominator = (x_diff_sq * y_diff_sq) ** 0.5
        if denominator == 0:
            return 0.0
        return numerator / denominator

    def haversine_distance_meters(self, lat1, lon1, lat2, lon2):
        """ Finds the distance between two map points in meters. This method uses latitude and longitude values to calculate
            the distance between two locations.
            Args:
                lat1 (float): Latitude of the first point.
                lon1 (float): Longitude of the first point.
                lat2 (float): Latitude of the second point.
                lon2 (float): Longitude of the second point.
            Returns:
                float: The distance in meters.
        """
        earth_radius = 6371000 # This is the average radius of the Earth in meters

        lat1 = radians(lat1)
        lon1 = radians(lon1)
        lat2 = radians(lat2)
        lon2 = radians(lon2)

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        return earth_radius * c

    def crime_proximity_to_parks(self, radii=(100, 200, 500)):
        """ Counts crimes near parks. This method finds the closest park for each crime and counts how many crimes fall inside each distance radius.
            Args:
                radii (tuple): Distance values in meters.
            Returns:
                dict: A dictionary where the key is the radius
                and the value is the number of nearby crimes.
        """
        results = {radius: 0 for radius in radii}

        for crime in self.crimes:
            closest_distance = None
            for park in self.parks:
                distance = self.haversine_distance_meters(
                    crime.latitude, crime.longitude,
                    park.latitude, park.longitude
                )
                if closest_distance is None or distance < closest_distance:
                    closest_distance = distance

            if closest_distance is not None:
                for radius in radii:
                    if closest_distance <= radius:
                        results[radius] += 1

        return results

    def full_report(self):
        """ Builds the full analysis report. This method groups all summary results into one dictionary.
            Returns: dict: A dictionary with all report sections.
        """
        return {
            "summary_of_data_set": self.dataset_summary(),
            "meaningful_insights": {
                "neighbourhood_with_most_parks": self.neighbourhood_with_most_parks(),
                "neighbourhood_with_most_crime": self.neighbourhood_with_most_crime(),
                "crime_type_counts": self.crime_type_counts(),
                "most_common_crime_type": self.most_common_crime_type()
            },
            "cross_data_set_summary": {
                "park_crime_correlation": self.park_crime_correlation(),
                "crime_proximity_to_parks": self.crime_proximity_to_parks()
            }
        }
