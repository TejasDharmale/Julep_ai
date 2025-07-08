from flask import Flask, render_template, request
import requests
import random
import json
import os
from dotenv import load_dotenv

# Handlers (your custom modules)
from handlers.weather_api import get_weather
from handlers.recommendation_utils import get_recommendations
from handlers.llama_utils import get_llama_city_dishes  # ✅ correctly imported
from handlers.julep_utils import get_julep_recommendations
from handlers.format_utils import format_restaurants
from handlers.google_reviews import get_google_reviews

# Load environment variables
load_dotenv("secret_key.env")

# Load city data
try:
    with open('handlers/city_data.json', 'r', encoding='utf-8') as f:
        city_data = json.load(f)
except FileNotFoundError:
    print("❌ handlers/city_data.json file not found.")
    city_data = {}

# Initialize Flask app
app = Flask(__name__, template_folder='../templates', static_folder='../static')

# API keys
API_KEY = os.getenv('API_KEY')
JULEP_API_KEY = os.getenv('JULEP_API_KEY')
allowed_envs = ('production', 'dev', 'local_multi_tenant', 'local')
env = os.getenv('JULEP_ENVIRONMENT', 'production')
if env not in allowed_envs:
    env = 'production'

# Debug prints
print("✅ WEATHER_API_KEY Loaded:", API_KEY is not None)
print("✅ JULEP_API_KEY Loaded:", JULEP_API_KEY is not None)

# Initialize Julep client (optional)
try:
    from julep import Julep
    if JULEP_API_KEY:
        client = Julep(api_key=JULEP_API_KEY, environment=env)
        agent = client.agents.create(name="Test Agent", model="claude-3.5-haiku", about="A test agent")
        print(f"✅ Julep agent created: {agent.id}")
except ImportError:
    print("⚠️ Julep not installed. Skipping Julep setup.")
except Exception as e:
    print("❌ Julep agent creation failed:", e)

from python_user.user_city_utils import load_user_city_data, add_user_city_data

def normalize_city_name(name):
    return name.lower().strip()

def is_unsatisfactory(data):
    # Helper to check if dishes or restaurants are missing/placeholder/empty
    if not data:
        return True
    dishes = data.get('dishes', [])
    restaurants = data.get('restaurants', [])
    if not dishes or dishes == ["Dish 1", "Dish 2", "Dish 3"]:
        return True
    if restaurants is not None and len(restaurants) == 0:
        return True
    return False

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_city_data = load_user_city_data()
        user_input = request.form.get('city')
        normalized_city = normalize_city_name(user_input)
        weather = get_weather(normalized_city, API_KEY)
        if weather:
            is_outdoor = not ("rain" in weather['description'] or weather['temperature'] < 10)
            city_display = user_input.title() if user_input else ""
            recommendations = None
            # Try static/user data first
            if normalized_city in city_data or get_recommendations(normalized_city, is_outdoor):
                recommendations = get_recommendations(normalized_city, is_outdoor)
                recommendations['display_city'] = city_display
            elif normalized_city in user_city_data:
                # Use user-provided city data
                recommendations = user_city_data[normalized_city]
                recommendations['display_city'] = city_display
            else:
                # City not found, show add city form
                if request.form.get('add_city') == '1':
                    # Save new city
                    display = request.form.get('display')
                    country = request.form.get('country')
                    # Dishes with meal type
                    dishes = []
                    for meal in ['breakfast', 'lunch', 'dinner']:
                        dish = request.form.get(f'dish_{meal}')
                        if dish:
                            dishes.append({'name': dish, 'meal': meal})
                    # Top-rated restaurants
                    restaurants = []
                    for i in range(1, 4):
                        r_name = request.form.get(f'restaurant_name_{i}')
                        r_rating = request.form.get(f'restaurant_rating_{i}')
                        if r_name and r_rating:
                            restaurants.append({'name': r_name, 'rating': float(r_rating)})
                    user_data = {
                        'display_city': display,
                        'country': country,
                        'dishes': dishes,
                        'restaurants': restaurants
                    }
                    add_user_city_data(normalized_city, user_data)
                    return render_template('index.html', error=f"✅ {display} added! Please search again.")
                # Show add city form
                return render_template('add_city.html', city=normalized_city, user_input=user_input)
            # If unsatisfactory, try Julep API
            if is_unsatisfactory(recommendations):
                julep_data = get_julep_recommendations(city_display, normalized_city, client=globals().get('client'), agent=globals().get('agent'))
                if julep_data.get('dishes'):
                    recommendations['dishes'] = julep_data['dishes']
                if julep_data.get('restaurants'):
                    recommendations['restaurants'] = julep_data['restaurants']
            # Format restaurants for template
            if is_outdoor:
                recommendations['restaurants'] = format_restaurants(recommendations['restaurants'])
                # Add Google reviews to each restaurant
                for i, r in enumerate(recommendations['restaurants']):
                    if isinstance(r, dict) and 'name' in r:
                        r['google_reviews'] = get_google_reviews(r['name'], normalized_city, recommendations.get('country', ''))
                    elif isinstance(r, str):
                        r_dict = {'name': r, 'google_reviews': get_google_reviews(r, normalized_city, recommendations.get('country', ''))}
                        recommendations['restaurants'][i] = r_dict
            else:
                recommendations['restaurants'] = []
            weather['city'] = recommendations['display_city']
            # If indoor, show Try at Home
            try_at_home = None
            if not is_outdoor and recommendations['dishes']:
                try_at_home = recommendations['dishes'][0]
            return render_template(
                'recommendation.html',
                weather=weather,
                is_outdoor=is_outdoor,
                recommendations=recommendations,
                try_at_home=try_at_home
            )
        else:
            return render_template('index.html', error="❌ Weather data unavailable. Please check your API key or try again.")
    return render_template('index.html')

if __name__ == '__main__':
    print("✅ Flask app starting...")
    app.run(debug=True)
