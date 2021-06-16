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
    driver = None

    def __init__(self, user_id, origin, destination):
        self.user_id = user_id
        self.origin = origin
        self.destination = destination


def update_distance_matrix():
    global drivers
    drivers = provide_drivers()
    drivers_cord = list(map(lambda driver: driver.location(), drivers))
    clients_origin_indexed = [[k, v.origin] for k, v in orders.items()]
    clients_origin =  [v[1] for v in clients_origin_indexed]
    matrix = gmaps.distance_matrix(origins=drivers_cord, destinations=clients_origin)
    rows = matrix['rows']
    matrix_elements = []
    for row_index, row in enumerate(rows):
        columns = row['elements']

        for column_index, cell in enumerate(columns):
            duration = cell['duration']
            matrix_elements.append({
                'row': row_index,
                'column': column_index,
                'duration': duration['value']
            })

    matrix_elements.sort(key=lambda x: x.get('duration'))

    used_orders = [False] * len(clients_origin)
    used_drivers = [False] * len(drivers_cord)
    for matrix_cell in matrix_elements:
        row = matrix_cell['row']
        column = matrix_cell['column']
        if not used_drivers[row] and not used_orders[column]:
            used_drivers[row] = True
            used_orders[column] = True
            order_key = clients_origin_indexed[column][0]
            order = orders[order_key]
            driver = drivers[row]
            order.driver = driver
            driver.order = order

    return
