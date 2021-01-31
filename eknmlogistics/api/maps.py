import requests

api_key = 'AIzaSyChUMNWC0jTUqm_cf5vAtxLICIFLQEOolc'


def reverse_geocode_url(latitude, longitude):
    return 'https://maps.googleapis.com/maps/api/geocode/json?key={0}&latlng={1},{2}' \
        .format(api_key, latitude, longitude)

def directions_url(origin_lat, origin_lng, destination_lat, destination_lng):
    return 'https://maps.googleapis.com/maps/api/directions/json?origin={0},{1}&destination={2},{3}&key={4}' \
        .format(origin_lat, origin_lng, destination_lat, destination_lng, api_key)

def reverse_geocode(latitude, longitude):
    request_url = reverse_geocode_url(latitude, longitude)
    response = requests.get(request_url)
    return response.json()

def directions(origin_lat, origin_lng, destination_lat, destination_lng):
    request_url = directions_url(origin_lat, origin_lng, destination_lat, destination_lng)
    response = requests.get(request_url)
    return response.json()

def route_waypoints(origin_lat, origin_lng, destination_lat, destination_lng):
    raw = directions(origin_lat, origin_lng, destination_lat, destination_lng)
    raw
    return