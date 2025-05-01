"""
Points of Interest Search Tool for Gemini Agent

This module provides functionality to search for points of interest near specified cities.
"""
import os
import csv
import math
from typing import Dict, List, Optional, Union, Tuple

class PointOfInterestTool:
    """Tool for searching points of interest near specified locations."""
    
    def __init__(self, poi_file_path: str = "data/Vienna_Attractions_Geolocated.csv"):
        """
        Initialize the points of interest search tool.
        
        Args:
            poi_file_path: Path to the CSV file containing points of interest
        """
        self.poi_file_path = poi_file_path
        self._pois = None  # Lazy loading
        self._cities = {}  # Cache for city coordinates
        
    @property
    def pois(self) -> List[Dict[str, Union[str, float]]]:
        """Lazy load the points of interest from CSV file."""
        if self._pois is None:
            self._load_pois()
        return self._pois
        
    def _load_pois(self) -> None:
        """Load points of interest from the CSV file."""
        try:
            # if not os.path.exists(self.poi_file_path):
            #     # Create data directory if it doesn't exist
            #     os.makedirs(os.path.dirname(self.poi_file_path), exist_ok=True)
                
            #     # Create a sample POI file if it doesn't exist
            #     with open(self.poi_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            #         writer = csv.writer(csvfile)
            #         writer.writerow(['Number', 'Name', 'Latitude', 'Longitude'])
            #         # Add some sample data
            #         writer.writerow(['1', 'Eiffel Tower', '48.8584', '2.2945'])
            #         writer.writerow(['2', 'Louvre Museum', '48.8606', '2.3376'])
            #         writer.writerow(['3', 'Notre-Dame Cathedral', '48.8530', '2.3499'])
            #         writer.writerow(['4', 'Empire State Building', '40.7484', '-73.9857'])
            #         writer.writerow(['5', 'Central Park', '40.7829', '-73.9654'])
                
            # Load POI data from CSV
            self._pois = []
            with open(self.poi_file_path, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    try:
                        poi = {
                            'number': row['Number'],
                            'name': row['Name'],
                            'latitude': float(row['Latitude']),
                            'longitude': float(row['Longitude'])
                        }
                        self._pois.append(poi)
                    except (ValueError, KeyError) as e:
                        print(f"Error parsing row: {row}. Error: {str(e)}")
                        
            # Pre-populate cities cache with common cities
            self._populate_common_cities()
                        
        except Exception as e:
            print(f"Error loading points of interest: {str(e)}")
            self._pois = []
    
    def _populate_common_cities(self) -> None:
        """Pre-populate the cities cache with common cities."""
        common_cities = {
            "paris": (48.8566, 2.3522),
            "new york": (40.7128, -74.0060),
            "rome": (41.9028, 12.4964),
            "london": (51.5074, -0.1278),
            "tokyo": (35.6762, 139.6503),
            "sydney": (-33.8688, 151.2093),
            "los angeles": (34.0522, -118.2437),
            "berlin": (52.5200, 13.4050),
            "madrid": (40.4168, -3.7038),
            "moscow": (55.7558, 37.6173),
            "beijing": (39.9042, 116.4074),
            "cairo": (30.0444, 31.2357),
            "rio de janeiro": (-22.9068, -43.1729),
            "toronto": (43.6532, -79.3832),
            "dubai": (25.2048, 55.2708),
            "singapore": (1.3521, 103.8198),
            "istanbul": (41.0082, 28.9784),
            "mumbai": (19.0760, 72.8777),
            "chicago": (41.8781, -87.6298),
            "bangkok": (13.7563, 100.5018)
        }
        self._cities = common_cities
    
    def _calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calculate the Haversine distance between two points in kilometers.
        
        Args:
            lat1: Latitude of point 1
            lon1: Longitude of point 1
            lat2: Latitude of point 2
            lon2: Longitude of point 2
            
        Returns:
            Distance in kilometers
        """
        # Radius of the Earth in kilometers
        R = 6371.0
        
        # Convert latitude and longitude from degrees to radians
        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)
        
        # Differences in coordinates
        dlon = lon2_rad - lon1_rad
        dlat = lat2_rad - lat1_rad
        
        # Haversine formula
        a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        # Distance in kilometers
        distance = R * c
        
        return distance
    
    def _locate_city(self, city_name: str) -> Tuple[Optional[float], Optional[float]]:
        """
        Get the coordinates of a city.
        
        Args:
            city_name: The name of the city
            
        Returns:
            Tuple containing (latitude, longitude) or (None, None) if not found
        """
        city_name_lower = city_name.lower()
        
        # Check our cache of common cities first
        if city_name_lower in self._cities:
            return self._cities[city_name_lower]
        
        # For cities not in our cache, we would typically use a geolocation API.
        # However, for this example, we'll just check if the city name matches any POIs
        # and use those coordinates instead.
        for poi in self.pois:
            if city_name_lower in poi['name'].lower():
                lat = poi['latitude']
                lon = poi['longitude']
                # Cache this result for future lookups
                self._cities[city_name_lower] = (lat, lon)
                return (lat, lon)
                
        # City not found
        return (None, None)
    
    def find_nearby_pois(self, city_name: str, radius_km: float = 2.0) -> Dict[str, Union[bool, List[Dict], str, Tuple[float, float]]]:
        """
        Find points of interest near a specified city.
        
        Args:
            city_name: The name of the city to search near
            radius_km: Search radius in kilometers (default: 2.0)
            
        Returns:
            Dict containing search results
        """
        city_name = city_name.strip()
        if not city_name:
            return {
                "found": False,
                "nearby_pois": [],
                "city_coordinates": None,
                "message": "No city name provided."
            }
            
        # Get city coordinates
        lat, lon = self._locate_city(city_name)
        
        if lat is None or lon is None:
            return {
                "found": False,
                "nearby_pois": [],
                "city_coordinates": None,
                "message": f"Could not locate city '{city_name}'. Please try another city."
            }
            
        # Find nearby POIs
        nearby_pois = []
        for poi in self.pois:
            distance = self._calculate_distance(lat, lon, poi['latitude'], poi['longitude'])
            if distance <= radius_km:
                # Add distance to the POI dict
                poi_with_distance = poi.copy()
                poi_with_distance['distance_km'] = round(distance, 2)
                nearby_pois.append(poi_with_distance)
                
        # Sort by distance
        nearby_pois.sort(key=lambda x: x['distance_km'])
        
        # Create result message
        if nearby_pois:
            poi_descriptions = []
            for poi in nearby_pois:
                poi_descriptions.append(f"{poi['name']} ({poi['distance_km']} km away)")
                
            message = f"Found {len(nearby_pois)} points of interest within {radius_km} km of {city_name}:\n"
            message += "\n".join([f"- {desc}" for desc in poi_descriptions])
        else:
            message = f"No points of interest found within {radius_km} km of {city_name}."
            
        return {
            "found": True,
            "nearby_pois": nearby_pois,
            "city_coordinates": (lat, lon),
            "message": message
        }