from geopy.geocoders import Nominatim

def getLatLong(city):
    geolocator = Nominatim(user_agent="MyApp")
    location = geolocator.geocode(city)
    return location

