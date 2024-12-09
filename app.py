from flask import Flask, render_template, request
import requests

API_KEY = 'DJSN5EyQIbyAUC4brCjeyFKDZ9Qa6NvG'

app = Flask(__name__)

def get_location_key(city_name):
    url = f"http://dataservice.accuweather.com/locations/v1/cities/autocomplete?apikey={API_KEY}&q={city_name}&language=ru"
    response = requests.get(url)
    if response.status_code == 200:
        data=response.json()
        if data:
            return data[0]["Key"]
        else:
            return None
    return None

def get_weather_details(location_key):
    url = f"http://dataservice.accuweather.com/currentconditions/v1/{location_key}?apikey={API_KEY}&details=true"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data:
            return {
                "Температура в градусах Цельсия": data[0]["Temperature"]["Metric"]["Value"],
                "Влажность": data[0]["RelativeHumidity"],
                "Скорость ветра": data[0]["Wind"]["Speed"]["Metric"]["Value"],
                "Вероятность дождя": data[0].get("PrecipitationProbability", 0)
            }
    return None

def check_bad_weather(temperature, wind_speed, rain_probability):
    if temperature < 0:
        return "Плохие погодные условия: температура ниже 0°C."
    if temperature > 35:
        return "Плохие погодные условия: температура выше 35°C."
    if wind_speed > 50:
        return "Плохие погодные условия: сильный ветер."
    if rain_probability > 70:
        return "Плохие погодные условия: высокая вероятность осадков."
    return "Хорошие погодные условия."

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        start_city = request.form.get("start_city")
        end_city = request.form.get("end_city")

        start_location_key = get_location_key(start_city)
        end_location_key = get_location_key(end_city)

        if not start_location_key or not end_location_key:
            return render_template("app.html", error_message="Не удалось найти один из городов.")

        start_weather = get_weather_details(start_location_key)
        end_weather = get_weather_details(end_location_key)

        if not start_weather or not end_weather:
            return render_template("app.html", error_message="Не удалось получить данные о погоде.")

        start_weather_status = check_bad_weather(
            start_weather["Температура в градусах Цельсия"],
            start_weather["Скорость ветра"],
            start_weather["Вероятность дождя"]
        )

        end_weather_status = check_bad_weather(
            end_weather["Температура в градусах Цельсия"],
            end_weather["Скорость ветра"],
            end_weather["Вероятность дождя"]
        )

        return render_template("app.html",
                               start_city=start_city,
                               end_city=end_city,
                               start_weather=start_weather,
                               end_weather=end_weather,
                               start_weather_status=start_weather_status,
                               end_weather_status=end_weather_status)
    return render_template("app.html")


if __name__ == "__main__":
    app.run(debug=True)
