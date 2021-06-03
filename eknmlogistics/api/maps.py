from itertools import chain

import googlemaps
import requests

api_key = 'AIzaSyChUMNWC0jTUqm_cf5vAtxLICIFLQEOolc'
gmaps: googlemaps.Client = googlemaps.Client(key=api_key)


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


def trans(value, index):
    global comp
    byte, result, shift = None, 0, 0

    while byte is None or byte >= 0x20:
        byte = ord(value[index]) - 63
        index += 1
        result |= (byte & 0x1f) << shift
        shift += 5
        comp = result & 1

    return ~(result >> 1) if comp else (result >> 1), index


def decode_polyline(expression, precision=5):
    coordinates, index, lat, lng, length, factor = [], 0, 0, 0, len(expression), float(10 ** precision)

    while index < length:
        lat_change, index = trans(expression, index)
        lng_change, index = trans(expression, index)
        lat += lat_change
        lng += lng_change
        coordinates.append((lat / factor, lng / factor))

    return coordinates


def route_waypoints(origin_lat, origin_lng, destination_lat, destination_lng):
    raw = directions(origin_lat, origin_lng, destination_lat, destination_lng)
    legs = raw['routes'][0]['legs']
    steps = legs[0]['steps']
    polylines = list(map(lambda x: x['polyline']['points'], steps))
    decoded_points = list(map(decode_polyline, polylines))
    decoded_points = list(chain.from_iterable(decoded_points))
    i = 1
    while i < len(decoded_points):
        if decoded_points[i] == decoded_points[i - 1]:
            del decoded_points[i]
            i -= 1
        i += 1
    points = list(map(lambda x: {'latitude': x[0], 'longitude': x[1]}, decoded_points))
    return points
