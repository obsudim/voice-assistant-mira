import requests

from app_config import city


api_key = '0438d1abded3dbebdfd81bd217b0f271'

def is_valid_city():
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        requests.get(url)
    except:
        return False
    return True


def get_weather():
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    weather_data = response.json()
    temp = weather_data['main']['temp']
    feels_like = weather_data['main']['feels_like']
    desc = weather_data['weather'][0]['description']
    return temp, feels_like, desc
