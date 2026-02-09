from flask import Flask, Response
import requests
import time
import os

app = Flask(__name__)

LAT = os.getenv("LATITUDE", "41.39")
LON = os.getenv("LONGITUDE", "2.17")

URL = (
    f"https://api.open-meteo.com/v1/forecast?"
    f"latitude={LAT}&longitude={LON}"
    f"&current_weather=true"
    f"&hourly=temperature_2m,relativehumidity_2m,pressure_msl,precipitation,windspeed_10m,winddirection_10m,weathercode"
    f"&daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max,precipitation_sum,weathercode"
    f"&forecast_days=7"
)

cache = {"metrics": "", "timestamp": 0}

def fetch_metrics():
    try:
        r = requests.get(URL, timeout=5)
        data = r.json()

        current = data["current_weather"]
        hourly = data["hourly"]
        daily = data["daily"]

        metrics = []

        # ---------------------------
        # MÉTRICAS ACTUALES
        # ---------------------------
        metrics.append(f'openmeteo_temperature_c {current["temperature"]}')
        metrics.append(f'openmeteo_wind_speed_ms {current["windspeed"]}')
        metrics.append(f'openmeteo_wind_direction_deg {current["winddirection"]}')
        metrics.append(f'openmeteo_weather_code {current["weathercode"]}')

        # ---------------------------
        # HORARIAS (últimas 6 horas)
        # ---------------------------
        for i in range(6):
            metrics.append(f'openmeteo_hourly_temperature_c{{hour="{i}"}} {hourly["temperature_2m"][-(i+1)]}')
            metrics.append(f'openmeteo_hourly_humidity_pct{{hour="{i}"}} {hourly["relativehumidity_2m"][-(i+1)]}')
            metrics.append(f'openmeteo_hourly_precip_mm{{hour="{i}"}} {hourly["precipitation"][-(i+1)]}')
            metrics.append(f'openmeteo_hourly_pressure_hpa{{hour="{i}"}} {hourly["pressure_msl"][-(i+1)]}')

        # ---------------------------
        # PRONÓSTICO 7 DÍAS
        # ---------------------------
        for day in range(7):
            metrics.append(f'openmeteo_daily_temp_max{{day="{day}"}} {daily["temperature_2m_max"][day]}')
            metrics.append(f'openmeteo_daily_temp_min{{day="{day}"}} {daily["temperature_2m_min"][day]}')
            metrics.append(f'openmeteo_daily_precip_probability{{day="{day}"}} {daily["precipitation_probability_max"][day]}')
            metrics.append(f'openmeteo_daily_precip_mm{{day="{day}"}} {daily["precipitation_sum"][day]}')
            metrics.append(f'openmeteo_daily_weather_code{{day="{day}"}} {daily["weathercode"][day]}')

        return "\n".join(metrics)

    except Exception as e:
        return f"# ERROR: {e}"

@app.route("/metrics")
def metrics():
    now = time.time()
    if now - cache["timestamp"] > 300:
        cache["metrics"] = fetch_metrics()
        cache["timestamp"] = now
    return Response(cache["metrics"], mimetype="text/plain")

@app.route("/")
def hello():
    return "OpenMeteo Exporter Extended + 7 Day Forecast"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
