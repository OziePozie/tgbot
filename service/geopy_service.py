from geopy.geocoders import Nominatim
from geopy.distance import geodesic


def get_km(city):
    try:
        geolocator = Nominatim(user_agent="Tester")
        default_city = "Энгельс"
        location_1 = geolocator.geocode(default_city)
        location_2 = geolocator.geocode(city)
        gps_point_1 = location_1.latitude, location_1.longitude
        gps_point_2 = location_2.latitude, location_2.longitude
        return geodesic(gps_point_1, gps_point_2).kilometers
    except Exception as e:
        return False


# TOKEN = '5b3ce3597851110001cf62480d6d2a97c2e444708fd600df1581d525'
#
#
# def matrix(locations: list, profile=0):
#     headers = {
#         'Content-Type': 'application/json; charset=utf-8',
#         'Accept': 'application/json',
#         'Authorization': TOKEN
#     }
#     profile_dict = {
#         0: 'driving-car',
#         1: 'foot-walking'
#     }
#     data = {"locations": [i[::-1] for i in locations],"metrics":["distance","duration"],"units":"m"}
#     res = requests.post(f'https://api.openrouteservice.org/v2/matrix/{profile_dict[profile]}',
#                         headers=headers,
#                         json=data).json()
#     return dict(durations = res['durations'][0][1], distances = res['distances'][0][1])
#
#
# print('\nМОСКВА - УФА на автомобиле')
# result = matrix([[55.7489, 37.6199], [54.7266, 55.9444]], 0)
# print(f'Результат: {result}')
# print(f'Расстояние: ~ {int(result["distances"] / 1000)} км')
# print(f'Время в пути: ~ {int(result["durations"] // 3600)} часов')
