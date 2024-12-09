from flask import Flask, render_template, request
import requests

API_KEY = 'KHXWLTBiA9EGX0QMGScjGMogCLUaSv6p'

app = Flask(__name__)

def get_location_key(city_name):
    url = f"http://dataservice.accuweather.com/locations/v1/cities/autocomplete?apikey={API_KEY}&q={city_name}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data:
            return data[0]["Key"]
        else:
            print("Не найдено локаций.")
            return None
    else:
        print(f"Error: {response.status_code}, Message: {response.text}")
        return None

def get_weather_details(location_key):
    url = f"http://dataservice.accuweather.com/currentconditions/v1/{location_key}?apikey={API_KEY}&details=true"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data:
            try:
                weather = {
                    "Температура в градусах Цельсия": data[0]["Temperature"]["Metric"]["Value"],
                    "Влажность": data[0]["RelativeHumidity"],
                    "Скорость ветра": data[0]["Wind"]["Speed"]["Metric"]["Value"],
                    "Вероятность дождя": data[0].get("PrecipitationProbability", 0)
                }
                return weather
            except KeyError as e:
                print(f"Ошибка в ключе: {e}")
                return None
        else:
            print("Нет данных о погоде.")
            return None
    else:
        print(f"Error: {response.status_code}, Message: {response.text}")
        return None

def check_bad_weather(temperature, wind_speed, rain_probability):
    temp_threshold_min = 0
    temp_threshold_max = 35
    wind_speed_threshold = 50
    rain_probability_threshold = 70

    if temperature < temp_threshold_min:
        return "Плохие погодные условия: температура ниже 0°C."
    elif temperature > temp_threshold_max:
        return "Плохие погодные условия: температура выше 35°C."
    elif wind_speed > wind_speed_threshold:
        return "Плохие погодные условия: сильный ветер."
    elif rain_probability > rain_probability_threshold:
        return "Плохие погодные условия: высокая вероятность осадков."
    else:
        return "Хорошие погодные условия."

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        start_city = request.form["start_city"]
        end_city = request.form["end_city"]
        start_location_key = get_location_key(start_city)
        end_location_key = get_location_key(end_city)

        if start_location_key and end_location_key:
            start_weather = get_weather_details(start_location_key)
            end_weather = get_weather_details(end_location_key)

            if start_weather and end_weather:
                start_weather_status = check_bad_weather(start_weather["Температура в градусах Цельсия"], start_weather["Скорость ветра"], start_weather["Вероятность дождя"])
                end_weather_status = check_bad_weather(end_weather["Температура в градусах Цельсия"], end_weather["Скорость ветра"], end_weather["Вероятность дождя"])

                return render_template("app.html",
                                       start_weather=start_weather,
                                       end_weather=end_weather,
                                       start_weather_status=start_weather_status,
                                       end_weather_status=end_weather_status)
            else:
                return "Не удалось получить данные о погоде для одного из городов."
        else:
            return "Не удалось найти город."
    return render_template("app.html")

if __name__ == "__main__":
    app.run(debug=True)
