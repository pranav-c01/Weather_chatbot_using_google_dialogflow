from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Webhook endpoint
@app.route('/webhook', methods=['POST'])
def webhook():
    # Get the JSON data from the request
    data = request.get_json()

    # Extract the city from the user's query
    city = data['queryResult']['parameters']['geo-city']

    # Call the OpenWeatherMap API to retrieve weather information
    weather_data = get_weather_data(city)

    # Process the weather data and generate a response
    response = process_weather_data(weather_data)

    # Return the response to Dialogflow
    return jsonify({'fulfillmentText': response})

# Function to call the OpenWeatherMap API and retrieve weather data
def get_weather_data(city):
    api_key = '8eb02a17de815cf1b5f416c56f1d0606'  # Replace with your OWM API key
    base_url = 'http://api.openweathermap.org/data/2.5/weather'
    params = {'q': city, 'appid': api_key, 'units': 'metric'}

    response = requests.get(base_url, params=params)
    data = response.json()

    return data

# Function to process the weather data and generate a response
def process_weather_data(data):
    if data['cod'] == '404':
        # City not found
        response = "Sorry, I couldn't find any weather information for that city."
    else:
        # Extract relevant weather information
        description = data['weather'][0]['description']
        temperature = data['main']['temp']
        humidity = data['main']['humidity']

        # Generate the response
        response = f"The weather in {data['name']} is {description}. "
        response += f"The temperature is {temperature}°C and the humidity is {humidity}%."

    return response

if __name__ == '__main__':
    app.run()