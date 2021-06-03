from ..drivers.driver import provide_drivers
from ..maps import gmaps

orders = {}
drivers = []


def add_order(user_id, origin, destination):
    orders[user_id] = Order(user_id, origin, destination)
    update_distance_matrix()


def get_driver(user_id):
    return drivers[user_id]


class Order:
    user_id = 0
    origin = None
    destination = None

    def __init__(self, user_id, origin, destination):
        self.user_id = user_id
        self.origin = origin
        self.destination = destination


def update_distance_matrix():
    drivers = provide_drivers()
    drivers_cord = list(map(lambda driver: driver.location(), drivers))
    clients_origin = [v.origin for k, v in orders.items()]
    matrix = gmaps.distance_matrix(origins=drivers_cord, destinations=clients_origin)
    return
