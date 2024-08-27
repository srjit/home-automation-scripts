import requests
import sys

def send_pump_request(pump_name):
    url = "http://10.0.0.192"
    form_data = {
        pump_name: ""
    }

    # Make the POST request
    response = requests.post(url, data=form_data)

    # Print the response (or whatever you want Home Assistant to capture)
    print(f"Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")

    return response

if __name__ == "__main__":
    # Read the pump name from the command line argument
    pump_name = sys.argv[1] if len(sys.argv) > 1 else "Pump1"
    send_pump_request(pump_name)
