import requests
import os

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
GOOGLE_PLACES_URL = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json'
GOOGLE_DETAILS_URL = 'https://maps.googleapis.com/maps/api/place/details/json'

def get_place_id(restaurant_name, city, country):
    """Get the Google Place ID for a restaurant given its name and location."""
    params = {
        'input': f'{restaurant_name}, {city}, {country}',
        'inputtype': 'textquery',
        'fields': 'place_id',
        'key': GOOGLE_API_KEY
    }
    response = requests.get(GOOGLE_PLACES_URL, params=params)
    data = response.json()
    candidates = data.get('candidates', [])
    if candidates:
        return candidates[0].get('place_id')
    return None

def get_google_reviews(restaurant_name, city, country):
    """Fetch Google reviews for a restaurant using the Places API."""
    place_id = get_place_id(restaurant_name, city, country)
    if not place_id:
        return []
    params = {
        'place_id': place_id,
        'fields': 'name,rating,reviews,user_ratings_total',
        'key': GOOGLE_API_KEY
    }
    response = requests.get(GOOGLE_DETAILS_URL, params=params)
    data = response.json()
    result = data.get('result', {})
    reviews = result.get('reviews', [])
    # Return top 3 reviews with rating and text
    return [{
        'author_name': r.get('author_name'),
        'rating': r.get('rating'),
        'text': r.get('text'),
        'relative_time_description': r.get('relative_time_description')
    } for r in reviews[:3]] 