from geopy.geocoders import Nominatim
#from app import location
import logging
logging.basicConfig(filename='geoloc.log', level=logging.INFO, format='%(asctime)s - %(message)s')


geolocator = Nominatim(user_agent="streamlit_app")

def details(location):
    location_info = geolocator.geocode(location)
    lat = location_info.latitude
    lon = location_info.longitude
    return lat,lon

