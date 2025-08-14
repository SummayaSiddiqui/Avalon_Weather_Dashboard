import requests
import pandas as pd

def get_historical_rainfall(latitude=47.5, longitude=-53.0, start_date="2025-07-01", end_date="2025-08-14"):
    url = f"https://archive-api.open-meteo.com/v1/archive?latitude={latitude}&longitude={longitude}&start_date={start_date}&end_date={end_date}&hourly=precipitation"
    response = requests.get(url)
    data = response.json()

    if 'hourly' not in data:
        print("Error: 'hourly' data not found. Response was:")
        print(data)
        return None

    times = data['hourly']['time']
    rainfall = data['hourly']['precipitation']
    
    df = pd.DataFrame({'time': pd.to_datetime(times), 'rainfall_mm': rainfall})
    df_daily = df.resample('D', on='time').sum().reset_index()
    return df_daily

# Test the function
if __name__ == "__main__":
    df = get_historical_rainfall()
    print(df.head())
