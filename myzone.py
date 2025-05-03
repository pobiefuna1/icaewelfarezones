import streamlit as st
from opencage.geocoder import OpenCageGeocode
import re

from math import radians, cos, sin, asin, sqrt



# Distance calculator
def haversine_distance(lat1, lon1, lat2, lon2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    km = 6371 * c
    return km

# Command handler
def handle_command(command):
    cmd = command[1:].strip().lower()  # remove '?' and normalize
    if cmd == "zones":
        st.markdown("### ICAE Welfare Zones:")
        st.markdown("""
        - **Oguta Lake Zone – North West**: North of Yellowhead Trail and West of 97 Street  
        - **Nkwu Zone – North East**: North of Yellowhead Trail and East of 97 Street  
        - **Omambala Zone – West**: Between Yellowhead & Whitemud and West of 170 Street  
        - **Ogene Zone – Central**: Between Yellowhead & Whitemud and between 170 Street & 75 Street  
        - **Ogbunike Cave Zone – East**: Between Yellowhead & Whitemud and East of 75 Street  
        - **Ichaka Zone – South West**: South of Whitemud Drive and West of Gateway Boulevard  
        - **Orji Zone – South East**: South of Whitemud Drive and East of Gateway Boulevard
        """)
        return True
    return False
    
    
# Mobile-friendly layout and title
st.set_page_config(layout="centered")
st.image("icae_logo.png", width=120)

# Set your OpenCage API key
API_KEY = "3dc65113cf8e4f10a2802af5cb630947"
geocoder = OpenCageGeocode(API_KEY)
EDMONTON_LAT = 53.5461
EDMONTON_LON = -113.4938

# Within 150 Km radius 
OUTER_LIMITS = 150


# App title
st.title("ICAE Welfare Zones")
st.markdown("Enter an Edmonton address to find its Welfare Zone.")

# Address input
address = st.text_input("Address")

# Address cleaner
def clean_address(raw):
    replacements = {
        r'\bSt\b': 'Street',
        r'\bStr\b': 'Street',
        r'\bRd\b': 'Road',
        r'\bAve\b': 'Avenue',
        r'\bBlvd\b': 'Boulevard',
        r'\bDr\b': 'Drive',
        r'\bCt\b': 'Court',
        r'\bCres\b': 'Crescent',
        r'\bPl\b': 'Place',
        r'\bTer\b': 'Terrace',
        r'\bNW\b': 'NW',
        r'\bSW\b': 'SW',
        r'\bNE\b': 'NE',
        r'\bSE\b': 'SE'
    }
    for pattern, replacement in replacements.items():
        raw = re.sub(pattern, replacement, raw, flags=re.IGNORECASE)
    return raw.strip()

# Function to classify zone based on lat/lon
def classify_zone(lat, lon):
    if lat > 53.585 and lon < -113.49:
        return "Oguta Lake Zone – North West", "North of Yellowhead Trail and West of 97 Street"
    elif lat > 53.585 and lon >= -113.49:
        return "Nkwu Zone – North East", "North of Yellowhead Trail and East of 97 Street"
    elif 53.485 < lat <= 53.585 and lon < -113.59:
        return "Omambala Zone – West", "Between Yellowhead & Whitemud and West of 170 Street"
    elif 53.485 < lat <= 53.585 and -113.59 <= lon <= -113.43:
        return "Ogene Zone – Central", "Between Yellowhead & Whitemud and between 170 Street & 75 Street"
    elif 53.485 < lat <= 53.585 and lon > -113.43:
        return "Ogbunike Cave Zone – East", "Between Yellowhead & Whitemud and East of 75 Street"
    elif lat <= 53.485 and lon < -113.47:
        return "Ichaka Zone – South West", "South of Whitemud Drive and West of Gateway Boulevard"
    elif lat <= 53.485 and lon >= -113.47:
        return "Orji Zone – South East", "South of Whitemud Drive and East of Gateway Boulevard"
    else:
        return "Unknown Zone", "Could not classify by current boundaries"

# Geocode function using OpenCage
def geocode_address(address):
    results = geocoder.geocode(address)
    if results and len(results) > 0:
        lat = results[0]['geometry']['lat']
        lon = results[0]['geometry']['lng']
        formatted = results[0]['formatted']
        return formatted, lat, lon
    else:
        return None, None, None

# Main logic
if address:
    if address.startswith("?"):
        if not handle_command(address):
            st.warning("Unknown command. Try `?zones`.")
    else:
        try:
            formatted_address, lat, lon = geocode_address(clean_address(address))
            if formatted_address:
                # Check outer bounds (if applicable)
                distance = geodesic((lat, lon), EDMONTON_CENTER).km
                if distance > OUTER_LIMITS:
                    st.warning("Location is outside the Edmonton area.")
                zone, bounds = classify_zone(lat, lon)
                st.success(f"🏠 Welfare Zone: **{zone}**")
                st.write(f"**Location:** {formatted_address}")
                st.write(f"**Bounds:** {bounds}")
            else:
                st.error("Could not resolve address. Please try a more specific location.")
        except Exception as e:
            st.error(f"An error occurred: {e}")

# Footer
st.markdown(
    "<div style='text-align: center; font-size: 0.8em; color: gray;'>"
    "© 2025 Peter Obiefuna, Arizen Corporation"
    "</div>",
    unsafe_allow_html=True
)
