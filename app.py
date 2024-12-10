from flask import Flask, render_template, request
import requests

API_KEY = 'UR7p8AAOwZnG8uokAjGSfJGtOpDrmPqE'

app = Flask(__name__)

def get_location_key(city_name):
    try:
        url = f"http://dataservice.accuweather.com/locations/v1/cities/autocomplete?apikey={API_KEY}&q={city_name}&language=ru"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data:
            return data[0]["Key"]
        else:
            return None
    except requests.exceptions.RequestException:
        return "Ошибка подключения к серверу. Проверьте сеть."

def get_weather_details(location_key):
    try:
        url = f"http://dataservice.accuweather.com/currentconditions/v1/{location_key}?apikey={API_KEY}&details=true"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data:
            return {
                "Температура в градусах Цельсия": data[0]["Temperature"]["Metric"]["Value"],
                "Влажность": data[0]["RelativeHumidity"],
                "Скорость ветра": data[0]["Wind"]["Speed"]["Metric"]["Value"],
                "Вероятность дождя": data[0].get("PrecipitationProbability", 0)
            }
        else:
            return None
    except requests.exceptions.RequestException:
        return "Ошибка подключения к серверу. Проверьте сеть."

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

        if not start_city or not end_city:
            return render_template("app.html", error_message="Пожалуйста, введите оба города.")

        start_location_key = get_location_key(start_city)
        end_location_key = get_location_key(end_city)

        if start_location_key == "Ошибка подключения к серверу. Проверьте сеть." or end_location_key == "Ошибка подключения к серверу. Проверьте сеть.":
            return render_template("app.html", error_message="Ошибка подключения к серверу. Проверьте сеть.")

        if start_location_key is None:
            return render_template("app.html",
                                   error_message=f"Город '{start_city}' не найден. Введите название города корректно.")
        if end_location_key is None:
            return render_template("app.html",
                                   error_message=f"Город '{end_city}' не найден. Введите название города корректно.")

        start_weather = get_weather_details(start_location_key)
        end_weather = get_weather_details(end_location_key)

        if start_weather == "Ошибка подключения к серверу. Проверьте сеть." or end_weather == "Ошибка подключения к серверу. Проверьте сеть.":
            return render_template("app.html", error_message="Ошибка подключения к серверу. Проверьте сеть.")

        if start_weather is None:
            return render_template("app.html",
                                   error_message=f"Не удалось получить данные о погоде для города '{start_city}'.")
        if end_weather is None:
            return render_template("app.html",
                                   error_message=f"Не удалось получить данные о погоде для города '{end_city}'.")

        start_weather_status  = check_bad_weather(
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
