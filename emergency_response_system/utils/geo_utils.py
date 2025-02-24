import requests
import streamlit as st
from config import OPENCAGE_API_KEY

def get_lat_lon(location_name):
    """Get latitude and longitude from location name using OpenCage API"""
    if not location_name:
        return None, None

    try:
        url = f'https://api.opencagedata.com/geocode/v1/json?q={location_name}&key={OPENCAGE_API_KEY}'
        response = requests.get(url)
        data = response.json()

        if data['status']['code'] == 200 and data['results']:
            lat = data['results'][0]['geometry']['lat']
            lon = data['results'][0]['geometry']['lng']
            return lat, lon
        else:
            st.warning(f"Could not find coordinates for {location_name}")
    except Exception as e:
        st.error(f"Error getting location coordinates: {e}")

    return None, None
