"""
CS5001
Milestone 1 - Parks Class
Spring 2026
21 Apr 26
Adele Ka
"""
class Park:
    """Stores one park record
    
        Attributes:
        name (str): The name of the park.
        neighbourhood (str): The neighbourhood where the park is located.
        hectare (float): The size of the park in hectares.
        latitude (float): The latitude of the park location.
        longitude (float): The longitude of the park location.

        Methods:
        __init__: Creates a Park object.
        to_dict: Returns the park data as a dictionary.
        __str__: Returns the park as a simple string.   

    """
    
    def __init__(self, name, neighbourhood, hectare, latitude, longitude,
                 street_number='', street_name='', ew_street='', ns_street='',
                 facilities='N', washrooms='N', special_features='N', advisories='N'):
        """ Initializes a Park object with the given name, neighbourhood, hectare, latitude, and longitude.
            Args:
                name (str): The name of the park.
                neighbourhood (str): The neighbourhood where the park is located.
                hectare (float): The size of the park in hectares.
                latitude (float): The latitude of the park location.
                longitude (float): The longitude of the park location.
                street_number (str): The street number of the park location (if available).
                ew_street (str): The east-west street of the park location (if available).
                ns_street (str): The north-south street of the park location (if available).
                facilities (str): 'Y' if the park has facilities, 'N' otherwise.
                washrooms (str): 'Y' if the park has washrooms, 'N' otherwise.
                special_features (str): 'Y' if the park has special features, 'N' otherwise.
                advisories (str): 'Y' if the park has advisories, 'N' otherwise.
        """
        self.name = name
        self.neighbourhood = neighbourhood
        self.hectare = float(hectare)
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        self.street_number = str(street_number).strip()
        self.street_name = str(street_name).strip()
        self.ew_street = str(ew_street).strip()
        self.ns_street = str(ns_street).strip()
        self.facilities = str(facilities).strip().upper()
        self.washrooms = str(washrooms).strip().upper()
        self.special_features = str(special_features).strip().upper()
        self.advisories = str(advisories).strip().upper()

    def address(self):
        """Builds the park street address from the stored street number and street name.

        Returns: str: The formatted street address for the park. If one part is missing, the method returns the part that is available.
        """
        return f"{self.street_number} {self.street_name}".strip()

    def amenities(self):
        """Builds a list of available park amenities based on Y/N attribute flags.

        Returns: list: A list of amenity names available at the park. If no amenities are marked as available, the method returns ['None listed'].
        """
        items = []
        if self.facilities == 'Y':
            items.append('Facilities')
        if self.washrooms == 'Y':
            items.append('Washrooms')
        if self.special_features == 'Y':
            items.append('Special features')
        if self.advisories == 'Y':
            items.append('Advisories')
        return items if items else ['None listed']

    def to_dict(self):
        """Converts the main park data fields into a dictionary.
        
        Returns: dict: A dictionary containing the park name, neighbourhood, hectare, latitude, and longitude values.  
        """
        return {
            'name': self.name,
            'neighbourhood': self.neighbourhood,
            'hectare': self.hectare,
            'latitude': self.latitude,
            'longitude': self.longitude,
        }

    def __str__(self):
        """Returns a simple string representation of the park.

        Returns:str: The park name followed by its neighbourhood in parentheses.
        """
        return f"{self.name} ({self.neighbourhood})"