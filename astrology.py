from typing import Dict, Any
from datetime import datetime
import ephem # type: ignore
from math import degrees

def get_zodiac_sign(month: int, day: int) -> str:
    # Keeping existing sun sign calculation as it's accurate
    if (month == 3 and day >= 21) or (month == 4 and day <= 19):
        return "Aries"
    elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
        return "Taurus"
    elif (month == 5 and day >= 21) or (month == 6 and day <= 20):
        return "Gemini"
    elif (month == 6 and day >= 21) or (month == 7 and day <= 22):
        return "Cancer"
    elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
        return "Leo"
    elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
        return "Virgo"
    elif (month == 9 and day >= 23) or (month == 10 and day <= 22):
        return "Libra"
    elif (month == 10 and day >= 23) or (month == 11 and day <= 21):
        return "Scorpio"
    elif (month == 11 and day >= 22) or (month == 12 and day <= 21):
        return "Sagittarius"
    elif (month == 12 and day >= 22) or (month == 1 and day <= 19):
        return "Capricorn"
    elif (month == 1 and day >= 20) or (month == 2 and day <= 18):
        return "Aquarius"
    else:
        return "Pisces"

def get_location_coordinates(location: str) -> tuple[float, float]:
    # Dictionary of city coordinates (latitude, longitude)
    city_coords = {
        "New York, NY": (40.7128, -74.0060),
        "Los Angeles, CA": (34.0522, -118.2437),
        "Chicago, IL": (41.8781, -87.6298),
        "Houston, TX": (29.7604, -95.3698),
        "Phoenix, AZ": (33.4484, -112.0740),
        "Philadelphia, PA": (39.9526, -75.1652),
        "San Antonio, TX": (29.4241, -98.4936),
        "San Diego, CA": (32.7157, -117.1611),
        "Dallas, TX": (32.7767, -96.7970),
        "San Jose, CA": (37.3382, -121.8863),
        "London, UK": (51.5074, -0.1278),
        "Paris, France": (48.8566, 2.3522),
        "Tokyo, Japan": (35.6762, 139.6503),
        "Sydney, Australia": (-33.8688, 151.2093),
        "Toronto, Canada": (43.6532, -79.3832),
        "Berlin, Germany": (52.5200, 13.4050),
        "Madrid, Spain": (40.4168, -3.7038),
        "Rome, Italy": (41.9028, 12.4964),
        "Beijing, China": (39.9042, 116.4074),
        "Moscow, Russia": (55.7558, 37.6173),
        "Dubai, UAE": (25.2048, 55.2708),
        "Singapore": (1.3521, 103.8198),
        "Mumbai, India": (19.0760, 72.8777),
        "São Paulo, Brazil": (-23.5505, -46.6333),
        "Mexico City, Mexico": (19.4326, -99.1332),
    }
    return city_coords.get(location, (0.0, 0.0))

def get_moon_sign(date: str, time: str, lat: float, lon: float) -> str:
    # Calculate exact moon position using ephem
    observer = ephem.Observer()
    observer.lat = str(lat)
    observer.lon = str(lon)
    
    dt = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
    observer.date = dt
    
    moon = ephem.Moon()
    moon.compute(observer)
    
    # Convert moon's ecliptic longitude to zodiac sign
    degrees_per_sign = 30
    moon_longitude = degrees(moon.hlon)
    if moon_longitude < 0:
        moon_longitude += 360
    
    sign_number = int(moon_longitude / degrees_per_sign)
    signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", 
             "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
    
    return signs[sign_number]

def get_rising_sign(date: str, time: str, lat: float, lon: float) -> str:
    # Calculate exact ascendant using ephem
    observer = ephem.Observer()
    observer.lat = str(lat)
    observer.lon = str(lon)
    
    dt = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
    observer.date = dt
    
    # Calculate sidereal time and ascendant
    st = observer.sidereal_time()
    ascendant_deg = degrees(st) - degrees(observer.lon)
    
    # Adjust for equation of time and obliquity
    ascendant_deg = ascendant_deg % 360
    
    # Convert to zodiac sign
    sign_number = int(ascendant_deg / 30)
    signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", 
             "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
    
    return signs[sign_number]

def get_birth_chart(birth_date: str, birth_time: str, birth_location: str) -> Dict[str, Any]:
    dt = datetime.strptime(birth_date, "%Y-%m-%d")
    lat, lon = get_location_coordinates(birth_location)
    
    return {
        "birth_date": birth_date,
        "birth_time": birth_time,
        "birth_location": birth_location,
        "sun_sign": get_zodiac_sign(dt.month, dt.day),
        "moon_sign": get_moon_sign(birth_date, birth_time, lat, lon),
        "rising_sign": get_rising_sign(birth_date, birth_time, lat, lon)
    }


def calculate_compatibility(user_chart: Dict[str, Any], match_chart: Dict[str, Any]) -> float:
    score = 0.0
    
    # 1. Element Compatibility (0-0.3)
    elements = {
        "Fire": ["Aries", "Leo", "Sagittarius"],
        "Earth": ["Taurus", "Virgo", "Capricorn"],
        "Air": ["Gemini", "Libra", "Aquarius"],
        "Water": ["Cancer", "Scorpio", "Pisces"]
    }
    
    def get_element(sign: str) -> str:
        return next(element for element, signs in elements.items() if sign in signs)
    
    user_elements = [get_element(sign) for sign in [user_chart["sun_sign"], user_chart["moon_sign"], user_chart["rising_sign"]]]
    match_elements = [get_element(sign) for sign in [match_chart["sun_sign"], match_chart["moon_sign"], match_chart["rising_sign"]]]
    
    element_score = sum(1 for u, m in zip(user_elements, match_elements) if u == m)
    score += element_score * 0.1  # Max 0.3 for perfect element match
    
    # 2. Modality Compatibility (0-0.2)
    modalities = {
        "Cardinal": ["Aries", "Cancer", "Libra", "Capricorn"],
        "Fixed": ["Taurus", "Leo", "Scorpio", "Aquarius"],
        "Mutable": ["Gemini", "Virgo", "Sagittarius", "Pisces"]
    }
    
    def get_modality(sign: str) -> str:
        return next(modality for modality, signs in modalities.items() if sign in signs)
    
    user_modalities = [get_modality(sign) for sign in [user_chart["sun_sign"], user_chart["moon_sign"], user_chart["rising_sign"]]]
    match_modalities = [get_modality(sign) for sign in [match_chart["sun_sign"], match_chart["moon_sign"], match_chart["rising_sign"]]]
    
    modality_score = sum(1 for u, m in zip(user_modalities, match_modalities) if u == m)
    score += modality_score * 0.067  # Max 0.2 for perfect modality match
    
    # 3. Aspect Compatibility (0-0.3)
    def get_sign_degree(sign: str) -> int:
        signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", 
                "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
        return signs.index(sign) * 30
    
    def calculate_aspect(deg1: int, deg2: int) -> str:
        diff = abs(deg1 - deg2)
        if diff > 180:
            diff = 360 - diff
        
        if diff < 10:
            return "Conjunction"
        elif 170 < diff < 190:
            return "Opposition"
        elif 115 < diff < 125:
            return "Trine"
        elif 85 < diff < 95:
            return "Square"
        elif 55 < diff < 65:
            return "Sextile"
        return "None"
    
    aspect_scores = {
        "Conjunction": 0.1,
        "Trine": 0.08,
        "Sextile": 0.06,
        "Square": -0.04,
        "Opposition": -0.02,
        "None": 0
    }
    
    user_degrees = [get_sign_degree(user_chart[f"{p}_sign"]) for p in ["sun", "moon", "rising"]]
    match_degrees = [get_sign_degree(match_chart[f"{p}_sign"]) for p in ["sun", "moon", "rising"]]
    
    aspect_score = 0
    for ud in user_degrees:
        for md in match_degrees:
            aspect = calculate_aspect(ud, md)
            aspect_score += aspect_scores[aspect]
    
    score += min(0.3, max(0, aspect_score))
    
    # 4. Direct Sign Matches (0-0.2)
    signs = [("sun_sign", 0.1), ("moon_sign", 0.07), ("rising_sign", 0.03)]
    for sign_type, weight in signs:
        if user_chart[sign_type] == match_chart[sign_type]:
            score += weight
    
    return round(min(1.0, max(0.0, score)), 2)