import requests
import json
import argparse

def get_air_pollution_data(api_key, lat, lon):
    url = "http://api.openweathermap.org/data/2.5/air_pollution"
    params = {
        'lat': lat,
        'lon': lon,
        'appid': api_key
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        # Extract main AQI and components if available
        if data and "list" in data and len(data["list"]) > 0:
            aqi = data["list"][0]["main"]["aqi"]
            components = data["list"][0]["components"]
            if aqi == 1:
                components['quality_desc'] = "Good"
            elif aqi == 2:
                components['quality_desc'] = "Fair"
            elif aqi == 3:
                components['quality_desc'] = "Moderate"
            elif aqi == 4:
                components['quality_desc'] = "Poor"
            elif aqi == 5:
                components['quality_desc'] = "Very Poor"
            else:
                components['quality_desc'] = "Unknown"
                
            # Return AQI and components as part of the JSON object
            return {"aqi": aqi, **components}
        else:
            return {"error": "Invalid response format"}
        
    except requests.exceptions.RequestException as e:
        print(json.dumps({"error": f"An error occurred: {e}"}))
        return None

if __name__ == "__main__":

    lat = '47.81728686344417'
    long = '-122.28992478745111'
    api_key = 'OpenWeatherMap API Key'
    air_pollution_data = get_air_pollution_data(api_key, lat, long)

    if air_pollution_data:
        print(json.dumps(air_pollution_data))
    else:
        print(json.dumps({"error": "Unable to retrieve data"}))
