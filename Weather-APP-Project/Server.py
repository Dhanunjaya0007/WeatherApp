# ════════════════════════════════════════════════
#  WeatherGlass — server.py
#  Works on Windows, Mac and Linux
#  Run via: start.bat (Windows) or ./start.sh (Mac/Linux)
#  Then open: http://localhost:5000
# ════════════════════════════════════════════════

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import webbrowser
import threading
import sys
import os

# ── App Setup ──────────────────────────────────
app = Flask(__name__, static_folder=".")
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
#  WEATHER ENDPOINT
#  Called by browser: /weather?city=Visakhapatnam
# ══════════════════════════════════════════════

@app.route("/weather")
def get_weather():

    city = request.args.get("city", "").strip()

    if not city:
        return jsonify({
            "error"  : True,
            "message": "Please enter a city name."
        }), 400

    try:
        params = {
            "q"     : city,
            "appid" : API_KEY,
            "units" : "metric",
        }

        response = requests.get(BASE_URL, params=params, timeout=8)
        data     = response.json()

        # Print raw data in terminal for learning
        print("\n" + "─" * 50)
        print(f"  City     : {city}")
        print(f"  Status   : {data.get('cod')}")
        print(f"  Response : {data}")
        print("─" * 50 + "\n")

        if str(data.get("cod")) != "200":
            return jsonify({
                "error"  : True,
                "message": data.get("message", "City not found.")
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
        return jsonify({
            "error"  : True,
            "message": "No internet connection."
        }), 503

    except requests.exceptions.Timeout:
        return jsonify({
            "error"  : True,
            "message": "Request timed out. Try again."
        }), 504

    except Exception as e:
        print(f"  Error: {e}")
        return jsonify({
            "error"  : True,
            "message": "Server error. Check terminal."
        }), 500


# ══════════════════════════════════════════════
#  AUTO OPEN BROWSER
# ══════════════════════════════════════════════

def open_browser():
    import time
    time.sleep(1.5)
    webbrowser.open("http://localhost:5000")


# ══════════════════════════════════════════════
#  START SERVER
# ══════════════════════════════════════════════

if __name__ == "__main__":

    # Detect OS
    platform = sys.platform
    if platform == "win32":
        os_name = "Windows"
    elif platform == "darwin":
        os_name = "Mac"
    else:
        os_name = "Linux"

    print("\n" + "═" * 45)
    print(f"  WeatherGlass — Running on {os_name}")
    print("  Open → http://localhost:5000")
    print("  Press CTRL+C to stop")
    print("═" * 45 + "\n")

    # Auto open browser in background
    threading.Thread(target=open_browser, daemon=True).start()

    # Start Flask on all network interfaces
    # 0.0.0.0 means it works on localhost AND
    # also on your local network (other devices)
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True,
        use_reloader=False
    )