import requests
import re
import json


def parse_event(event):
    # Define a regex pattern to extract sensor values
    pattern = r"Sns1:\s(\d+)\smV, Sns2:\s(\d+)\smV, Sns3:\s(\d+)\smV, Sns4:\s(\d+)\smV"
    match = re.search(pattern, event)
    
    if match:
        return {
            "Sns1": int(match.group(1)),
            "Sns2": int(match.group(2)),
            "Sns3": int(match.group(3)),
            "Sns4": int(match.group(4))
        }
    return None


def calculate_averages(data_list):
    averages = {}
    total_count = len(data_list)
    
    if total_count == 0:
        return averages
    
    # Sum up the values for each sensor
    for data in data_list:
        for key, value in data.items():
            if key not in averages:
                averages[key] = 0
            averages[key] += value
    
    # Calculate the average for each sensor
    for key in averages:
        averages[key] = round(averages[key] / total_count)
    
    return averages    


def get_local_web_service_data():
    # Define the URL of the local web service
    url = "http://10.0.0.192/events"
    averages = {'Sns1': -1, 'Sns2': -1, 'Sns3': -1, 'Sns4': -1}
    
    try:
        # Headers
        headers = {
            'Content-Type': 'text/event-stream',
            'Cache-Control': 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0',
            'Pragma': 'no-cache',
            'Connection': 'Keep-Alive',
            'Transfer-Encoding': 'chunked'
        }

        # Make the GET request with headers and a timeout
        response = requests.get(url, headers=headers, timeout=10, stream=True)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Initialize event counter
            event_count = 0
            data_list = []
            
            # Process each chunk of the response as it arrives
            for chunk in response.iter_content(chunk_size=None):
                if chunk:
                    # Decode and print the chunk
                    data = parse_event(chunk.decode('utf-8'))
                    if data:
                        data_list.append(data)
                        event_count += 1
                    
                    # Stop after receiving 5 events
                    if event_count >= 15:
                        break
            
            averages = calculate_averages(data_list)
            print(json.dumps(averages))
        else:
            print(json.dumps({"error": "Failed to fetch data"}))
    
    except requests.exceptions.RequestException as e:
        # Handle any exceptions that occur during the request
        print(json.dumps({"error": str(e)}))

if __name__ == "__main__":
    get_local_web_service_data()