# recommendation_utils.py

import random
import json
import os

# Load city data from JSON file
with open(os.path.join(os.path.dirname(__file__), 'city_data.json'), 'r', encoding='utf-8') as f:
    city_data = json.load(f)

USER_CITY_DATA_PATH = os.path.join(os.path.dirname(__file__), 'user_city_data.json')

def load_user_city_data():
    try:
        with open(USER_CITY_DATA_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}

def save_user_city_data(data):
    with open(USER_CITY_DATA_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def get_recommendations(city, is_outdoor):
    user_data = load_user_city_data()
    if city in user_data:
        info = user_data[city]
        display_city = info['display']
        dishes = info['cuisine'][:3]
        restaurants = [r for r in info['restaurants'] if r['outdoor'] == is_outdoor]
        if not restaurants:
            restaurants = info['restaurants']
        return {
            "dishes": dishes,
            "restaurants": restaurants[:3],
            "display_city": display_city
        }
    info = city_data[city]
    display_city = info['display']
    dishes = random.sample(info['cuisine'], min(3, len(info['cuisine'])))
    restaurants = [r for r in info['restaurants'] if r['outdoor'] == is_outdoor]
    if not restaurants:
        restaurants = info['restaurants']
    return {
        "dishes": dishes,
        "restaurants": random.sample(restaurants, min(3, len(restaurants))),
        "display_city": display_city
    }

def add_user_city(city, display, country, cuisine, restaurants):
    data = load_user_city_data()
    data[city] = {
        "display": display,
        "country": country,
        "cuisine": cuisine,
        "restaurants": restaurants
    }
    save_user_city_data(data)
