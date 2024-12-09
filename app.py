import requests

API_KEY = 'KHXWLTBiA9EGX0QMGScjGMogCLUaSv6p'
location = 'New York'

url=f"http://dataservice.accuweather.com/locations/v1/cities/autocomplete?apikey={API_KEY}&q={location}"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    location_key = data[0]["Key"]
url2 = f"http://dataservice.accuweather.com/currentconditions/v1/{location_key}?apikey={API_KEY}"
response = requests.get(url2)
if response.status_code == 200:
    data = response.json()
    print(data)
