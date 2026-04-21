"""
CS5001
Final Project - Crime Class
Spring 2026
21 Apr 26
Adele Ka
"""
class Crime:
    """Stores one crime record
        
        Attributes:
        crime_type (str): The type of crime.
        neighbourhood (str): The neighbourhood where the crime happened.
        latitude (float): The latitude of the crime location.
        longitude (float): The longitude of the crime location.

        Methods:
        __init__: Creates a Crime object.
        to_dict: Returns the crime data as a dictionary.
        __str__: Returns the crime as a simple string.
   
    """
    def __init__(self, crime_type: str, neighbourhood: str, latitude: float, longitude: float,  address='Address not available') -> None:
        """ Initializes a Crime object with the given crime type, neighbourhood, latitude, and longitude. 
            Args:
                crime_type (str): The type of crime.
                neighbourhood (str): The neighbourhood where the crime occurred.
                latitude (float): The latitude of the crime location.
                longitude (float): The longitude of the crime location.
                address (str): The address of the crime location (if available).
        """
        self.crime_type = crime_type
        self.neighbourhood = neighbourhood
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        self.address = address

    def to_dict(self) -> dict:
        """ Converts a Crime object into a dictionary.
            Returns: dict
        """
        return {
            "crime_type": self.crime_type,
            "neighbourhood": self.neighbourhood,
            "latitude": self.latitude,
            "longitude": self.longitude,
            'address': self.address,
        }

    def __str__(self) -> str:
        """ Returns a string representation of the Crime object of a crime in neighbourhood.
            Returns: str
        """
        return f"{self.crime_type} in {self.neighbourhood}"