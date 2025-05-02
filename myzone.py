import streamlit as st
from opencage.geocoder import OpenCageGeocode

API_KEY = "3dc65113cf8e4f10a2802af5cb630947"
geocoder = OpenCageGeocode(API_KEY)

def geocode_address(address):
    results = geocoder.geocode(address)
    if results and len(results) > 0:
        lat = results[0]['geometry']['lat']
        lon = results[0]['geometry']['lng']
        formatted = results[0]['formatted']
        return formatted, lat, lon
    else:
        return None, None, None

# App title
st.title("IcaeWelfareZones Classifier")
st.markdown("Enter an Edmonton address to find its Welfare Zone.")

# Address input
address = st.text_input("Address")

# Initialize geocoder
#geolocator = Nominatim(user_agent="icae-welfare-zones")

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

# Main logic
if address:
    try:
        location = geocode_address(address)
        if location:
            lat = location.latitude
            lon = location.longitude
            zone, bounds = classify_zone(lat, lon)
            
            st.success("Zone Classification Result:")
            st.write(f"**Location:** {location.address}")
            st.write(f"**Bounds:** {bounds}")
            st.write(f"**Welfare Zone:** {zone}")
        else:
            st.error("Could not resolve address. Please try a more specific location.")
    except Exception as e:
        st.error(f"An error occurred: {e}")
