import requests

API_KEY = 'KHXWLTBiA9EGX0QMGScjGMogCLUaSv6p'

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

if __name__ == "__main__":
    city = ("Moscow")  # Укажите название города
    location_key = get_location_key(city)
    if location_key:
        weather_details = get_weather_details(location_key)
        if weather_details:
            print("Прогноз погоды:")
            print(weather_details)
