# ════════════════════════════════════════════════
#  WeatherGlass — server.py (Fixed & Permanent)
#  
#  DO NOT run index.html directly.
#  ALWAYS start via: start.bat  (double click)
#  OR manually: python server.py
#  THEN open: http://localhost:5000
# ════════════════════════════════════════════════

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import os
import webbrowser
import threading

# ── App setup ──────────────────────────────────
app = Flask(__name__, static_folder=".")

# Allow requests from ALL origins permanently
CORS(app, resources={r"/*": {"origins": "*"}})

# ── API Config ─────────────────────────────────
API_KEY  = "0a41944406513a88a127aaa1074607d1"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


# ══════════════════════════════════════════════
#  SERVE FRONTEND FILES
# ══════════════════════════════════════════════

@app.route("/")
def index():
    return send_from_directory(".", "index.html")

@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory(".", filename)


# ══════════════════════════════════════════════
#  WEATHER API ENDPOINT
# ══════════════════════════════════════════════

@app.route("/weather")
def get_weather():

    city = request.args.get("city", "").strip()

    if not city:
        return jsonify({"error": True, "message": "Please enter a city name."}), 400

    try:
        params = {
            "q"     : city,
            "appid" : API_KEY,
            "units" : "metric",
        }

        response = requests.get(BASE_URL, params=params, timeout=8)
        data     = response.json()

        print("\n" + "─" * 50)
        print(f"  City      : {city}")
        print(f"  Status    : {data.get('cod')}")
        print(f"  Response  : {data}")
        print("─" * 50 + "\n")

        if str(data.get("cod")) != "200":
            return jsonify({
                "error"  : True,
                "message": data.get("message", "City not found. Check spelling.")
            }), 404

        return jsonify({
            "error"       : False,
            "city"        : data["name"],
            "country"     : data["sys"]["country"],
            "temp"        : round(data["main"]["temp"]),
            "feels_like"  : round(data["main"]["feels_like"]),
            "humidity"    : data["main"]["humidity"],
            "wind_speed"  : round(data["wind"]["speed"], 1),
            "description" : data["weather"][0]["description"],
            "weather_id"  : data["weather"][0]["id"],
            "weather_main": data["weather"][0]["main"],
        })

    except requests.exceptions.ConnectionError:
        return jsonify({"error": True, "message": "Cannot reach OpenWeatherMap. Check internet."}), 503

    except requests.exceptions.Timeout:
        return jsonify({"error": True, "message": "Request timed out. Try again."}), 504

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": True, "message": "Server error. Check terminal."}), 500


# ══════════════════════════════════════════════
#  START SERVER
# ══════════════════════════════════════════════

def open_browser():
    import time
    time.sleep(1.5)
    webbrowser.open("http://localhost:5000")

if __name__ == "__main__":
    print("\n" + "═" * 45)
    print("  WeatherGlass backend running")
    print("  Open → http://localhost:5000")
    print("  Press CTRL+C to stop the server")
    print("═" * 45 + "\n")

    threading.Thread(target=open_browser, daemon=True).start()

    app.run(debug=True, port=5000, use_reloader=False)