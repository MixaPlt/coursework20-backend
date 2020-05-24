import requests

api_key = 'AIzaSyDTPebBcJ35uYn2DdLMokiSZHuhuZRXBsE'


def reverse_geocode_url(latitude, longitude):
    return 'https://maps.googleapis.com/maps/api/geocode/json?key={0}&latlng={1},{2}' \
        .format(api_key, latitude, longitude)


def reverseGeocode(latitude, longitude):
    request_url = reverse_geocode_url(latitude, longitude)
    response = requests.get(request_url)
    return response.json()