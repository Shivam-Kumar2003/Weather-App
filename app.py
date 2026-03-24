from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # ✅ Enable CORS

# 🔑 Add your OpenWeather API key here
API_KEY = "82af14c11ba7c036cdac90d7101bd397"


# ✅ Home route (serves index.html)
@app.route("/")
def home():
    return render_template("index.html")


# ✅ Weather by city
@app.route("/weather", methods=["GET"])
def get_weather():
    city = request.args.get("city")

    if not city:
        return jsonify({"error": "Please provide a city name"}), 400

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()

        if data.get("cod") != 200:
            return jsonify({"error": "City not found"}), 404

        weather_data = {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"]
        }

        return jsonify(weather_data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ✅ Weather by coordinates (auto-location)
@app.route("/weather-by-coords", methods=["GET"])
def get_weather_by_coords():
    lat = request.args.get("lat")
    lon = request.args.get("lon")

    if not lat or not lon:
        return jsonify({"error": "Latitude and Longitude required"}), 400

    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()

        if data.get("cod") != 200:
            return jsonify({"error": "Location not found"}), 404

        weather_data = {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"]
        }

        return jsonify(weather_data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ✅ Run server
if __name__ == "__main__":
    app.run(debug=True)