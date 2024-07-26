from ninja import Router
import requests
import os

router = Router()

weather_api_key = os.getenv('WEATHER_API_KEY')

@router.get("/key", tags=["weather"])
def get_weather_data(request):
    url = "https://api.weatherapi.com/v1/forecast.json"
    params = {
        "key": weather_api_key,
        "q": "Strangnas",
        "days": 3,
        "lang": "sv"
    }
    response = requests.get(url, params=params)

    return response.json()
