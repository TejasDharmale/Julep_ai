import requests

def get_weather(city, api_key):
    url = "http://api.weatherapi.com/v1/current.json"
    params = {'key': api_key, 'q': city}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return {
            'city': data['location']['name'],
            'country': data['location']['country'],
            'description': data['current']['condition']['text'].lower(),
            'temperature': data['current']['temp_c']
        }
    except Exception as e:
        print("❌ Weather API error:", e)
        return None