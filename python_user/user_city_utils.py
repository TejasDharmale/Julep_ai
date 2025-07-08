import json
import os

USER_CITY_DATA_PATH = os.path.join(os.path.dirname(__file__), 'user_city_data.json')

def load_user_city_data():
    if not os.path.exists(USER_CITY_DATA_PATH):
        return {}
    with open(USER_CITY_DATA_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def add_user_city_data(city, data):
    city = city.lower().strip()
    all_data = load_user_city_data()
    all_data[city] = data
    with open(USER_CITY_DATA_PATH, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2) 