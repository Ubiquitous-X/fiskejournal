import requests
import os
from core.task_functions.utils import encode_image, send_notification
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

def get_fish_species(image_path):
    """Identifiera fiskart med hjälp av OpenAI API"""
    openai_api_key = os.getenv('OPENAI_API_KEY')
    base64_image = encode_image(image_path)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai_api_key}"
    }

    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Vilken art är denna fisk? Svara bara med ett enda ord, det svenska namnet och "
                                "utelämna den avslutande punkten. Om du inte kan identifiera någon fisk svarar du 'Ej "
                                "bestämd'."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    response_dict = response.json()

    try:
        content = response_dict['choices'][0]['message']['content']
        return content.strip()
    except (KeyError, IndexError):
        logger.error(f"Fel vid anrop till OpenAI API: {response_dict}")
        send_notification(f'OpenAI kunde ej nås', 'error', delay=1)
        return "Ej bestämd"


def get_location_name(lat, lon):
    """Hämta platsnamn från koordinater via Geonames API"""
    geonames_username = os.getenv('GEONAMES_USERNAME')
    geo_url = (f"http://api.geonames.org/findNearbyJSON?lat={lat}&lng={lon}&username={geonames_username}&featureCode=LK"
               f"&featureCode=BAY&featureCode=STM")
    response = requests.get(geo_url)

    if response.status_code == 200:
        data = response.json()
        if 'geonames' in data:
            for item in data['geonames']:
                if item['fcode'] in ['LK', 'BAY', 'STM']:
                    return item.get('name', 'Okänd')
        return "Okänd"
    else:
        logger.error(f"Geonames API-fel. Statuskod: {response.status_code} - {response.text}")
        send_notification(f'GeoNames kunde ej nås', 'error', delay=1)
        return "Okänd"


def get_current_weather_data(lat, lon):
    """Hämta aktuell väderdata från WeatherAPI"""
    weather_api_key = os.getenv('WEATHER_API_KEY')
    weather_url = (f"http://api.weatherapi.com/v1/forecast.json?"
                   f"key={weather_api_key}&q={lat},{lon}&days=1&lang=sv")
    response = requests.get(weather_url)
    data = response.json()

    if response.status_code == 200:
        # Hämta relevanta data från svaret
        current_weather = data['current']
        forecast_weather = data['forecast']['forecastday'][0]['astro']

        air_temperature = current_weather['temp_c']
        weather = current_weather['condition']['text']
        wind_speed = round(current_weather['wind_kph'] / 3.6, 1)  # Konvertera km/h till m/s och avrunda till 1 decimal
        wind_dir = current_weather['wind_dir']
        moon_phase = forecast_weather['moon_phase']  # Månfasen i text
        moon_illumination = int(forecast_weather['moon_illumination'])  # Månbelysning i procent
        uv_index = current_weather['uv']
        air_pressure = current_weather['pressure_mb']
        air_humidity = current_weather['humidity']
        weather_icon_url = "https:" + current_weather['condition']['icon']  # Ikon för väderförhållanden

        # Översätt månfaserna
        moon_phase_translations = {
            "New Moon": "Nymåne",
            "Waxing Crescent": "Tilltagande skära",
            "First Quarter": "Första kvarteret",
            "Waxing Gibbous": "Tilltagande halvmåne",
            "Full Moon": "Fullmåne",
            "Waning Gibbous": "Avtagande halvmåne",
            "Last Quarter": "Sista kvarteret",
            "Waning Crescent": "Avtagande skära"
        }

        # Justera månfaser baserat på månbelysning
        if 97 <= moon_illumination <= 100:
            moon_phase_sv = "Fullmåne"
        elif 0 <= moon_illumination <= 3:
            moon_phase_sv = "Nymåne"
        else:
            moon_phase_sv = moon_phase_translations.get(moon_phase, moon_phase)

        # Översätt vindriktningen
        wind_dir_translations = {
            'E': 'Ö',
            'W': 'V'
        }
        wind_dir_sv = ''.join([wind_dir_translations.get(char, char) for char in wind_dir])

        return (weather, air_temperature, air_pressure, wind_speed, wind_dir_sv, uv_index,
                moon_phase_sv, moon_illumination, air_humidity, weather_icon_url)
    else:
        logger.error(
            f"Misslyckades med att hämta vädret: {data.get('error', {}).get('message', 'Ej specificerat meddelande')}")
        send_notification(f'Weatherapi kunde ej nås', 'error', delay=1)
        return None, None, None, None, None, None, None, None, None, None
