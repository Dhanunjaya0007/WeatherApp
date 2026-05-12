# ════════════════════════════════════════════════
#  WeatherGlass — Python Flask Backend
#  server.py
#
#  HOW TO RUN:
#  1. pip install flask flask-cors requests
#  2. python server.py
#  3. Open http://localhost:5000 in your browser
# ════════════════════════════════════════════════

try:
    from flask import Flask, request, jsonify, send_from_directory
    import requests
except ImportError as e:
    print(f"Error: {e}")
    print("Please install dependencies: pip install flask flask-cors requests")
    exit(1)

try:
    from flask_cors import CORS
except ImportError:
    print("Warning: flask-cors not installed. CORS may not work properly.")
    CORS = None

import os

app = Flask(__name__, static_folder=".")
CORS(app)  # Allow frontend JS to call this backend

# ── YOUR API KEY ──────────────────────────────────
API_KEY  = "0a41944406513a88a127aaa1074607d1"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
# ─────────────────────────────────────────────────


# ── SERVE FRONTEND FILES ──────────────────────────
@app.route("/")
def index():
    """Serve the main HTML file."""
    return send_from_directory(".", "index.html")

@app.route("/<path:filename>")
def static_files(filename):
    """Serve CSS / JS files."""
    return send_from_directory(".", filename)


# ── WEATHER API ENDPOINT ──────────────────────────
@app.route("/weather")
def get_weather():
    """
    Proxy endpoint — frontend calls this instead of
    hitting OpenWeatherMap directly (keeps API key safe).

    Query param:  ?city=Visakhapatnam
    Returns:      JSON weather data
    """
    city = request.args.get("city", "").strip()

    # ── Validate input ──
    if not city:
        return jsonify({
            "error": True,
            "message": "City name is required."
        }), 400

    # ── Call OpenWeatherMap ──
    params = {
        "q"     : city,
        "appid" : API_KEY,
        "units" : "metric",   # Celsius — change to 'imperial' for Fahrenheit
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=8)
        data     = response.json()

        # ── Log the raw response (for your learning / debugging) ──
        print("\n──────────────────────────────────")
        print(f"City queried : {city}")
        print(f"Status code  : {data.get('cod')}")
        print(f"Response     : {data}")
        print("──────────────────────────────────\n")

        # ── OpenWeatherMap returns cod=200 on success ──
        if str(data.get("cod")) != "200":
            return jsonify({
                "error"  : True,
                "message": data.get("message", "City not found.")
            }), 404

        # ── Return clean payload to frontend ──
        return jsonify({
            "error"      : False,
            "city"       : data["name"],
            "country"    : data["sys"]["country"],
            "temp"       : round(data["main"]["temp"]),
            "feels_like" : round(data["main"]["feels_like"]),
            "humidity"   : data["main"]["humidity"],
            "wind_speed" : round(data["wind"]["speed"], 1),
            "description": data["weather"][0]["description"],
            "weather_id" : data["weather"][0]["id"],
            "weather_main": data["weather"][0]["main"],
            "raw"        : data,   # full raw data — useful for your learning
        })

    except requests.exceptions.ConnectionError:
        return jsonify({
            "error"  : True,
            "message": "Cannot reach OpenWeatherMap. Check your internet."
        }), 503

    except requests.exceptions.Timeout:
        return jsonify({
            "error"  : True,
            "message": "Request timed out. Try again."
        }), 504

    except Exception as e:
        print(f"Unexpected error: {e}")
        return jsonify({
            "error"  : True,
            "message": "An unexpected server error occurred."
        }), 500


# ── START SERVER ──────────────────────────────────
if __name__ == "__main__":
    print("═══════════════════════════════════════")
    print("  WeatherGlass backend running")
    print("  Open → http://localhost:5000")
    print("═══════════════════════════════════════")
    app.run(debug=True, port=5000)