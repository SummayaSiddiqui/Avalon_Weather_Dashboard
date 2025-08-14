import requests
import pandas as pd

def get_historical_rainfall(start_date, end_date, latitude=47.56, longitude=-52.71):
    """
    Fetch historical daily rainfall from Open-Meteo
    """
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
        "daily": "rain_sum",
        "timezone": "America/St_Johns"
    }
    response = requests.get(url, params=params)
    data = response.json()

    daily_rain = data.get('daily', {})
    times = daily_rain.get('time', [])
    rain_mm = daily_rain.get('rain_sum', [])

    df = pd.DataFrame({
        'time': pd.to_datetime(times),
        'rainfall_mm': rain_mm
    })
    return df

def get_coordinates(city_name):
    """
    Convert city name to latitude, longitude, province/state, and country using OpenStreetMap Nominatim
    (results forced to English)
    """
    try:
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            "q": city_name,
            "format": "json",
            "limit": 1,
            "addressdetails": 1,
            "accept-language": "en"  # Force results in English
        }
        headers = {
            "User-Agent": "AvalonRainfallDashboard/1.0"
        }
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()

        data = response.json()
        if data:
            lat = float(data[0]['lat'])
            lon = float(data[0]['lon'])
            address = data[0].get('address', {})

            province = (
                address.get('state') or
                address.get('province') or
                address.get('region') or
                ''
            )
            country = address.get('country', '')

            return lat, lon, province, country
        else:
            return None, None, None, None

    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None, None, None, None
    except ValueError:
        print("Invalid response format")
        return None, None, None, None

