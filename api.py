import requests

TOKEN = "833e684e3cba42a5a30fb3a63ae0bd4809dac91a"


def search_station(keyword):
    """
    Mencari station berdasarkan kata kunci.
    """

    url = f"https://api.waqi.info/search/?token={TOKEN}&keyword={keyword}"

    response = requests.get(url)
    result = response.json()

    if result["status"] != "ok":
        return []

    stations = []

    for item in result["data"]:

        stations.append({
            "name": item["station"]["name"],
            "url": item["station"]["url"]
        })

    return stations


def get_air_quality(station_url):
    """
    Mengambil data AQI berdasarkan station URL.
    """

    url = f"https://api.waqi.info/feed/{station_url}/?token={TOKEN}"

    response = requests.get(url)
    result = response.json()

    if result["status"] != "ok":
        return None

    d = result["data"]

    return {
        "Kota": d["city"]["name"],
        "AQI": d["aqi"],
        "PM2.5": d["iaqi"].get("pm25", {}).get("v"),
        "Suhu": d["iaqi"].get("t", {}).get("v"),
        "Kelembapan": d["iaqi"].get("h", {}).get("v"),
        "Tekanan": d["iaqi"].get("p", {}).get("v"),
        "Angin": d["iaqi"].get("w", {}).get("v"),
        "Update": d["time"].get("iso", d["time"].get("s", "-")),        
        "Polutan": d.get("dominentpol", "-"),
        "Latitude": d["city"]["geo"][0],
        "Longitude": d["city"]["geo"][1],
        "Forecast_PM25": d["forecast"]["daily"].get("pm25", []),
        "Forecast_PM10": d["forecast"]["daily"].get("pm10", [])
    }