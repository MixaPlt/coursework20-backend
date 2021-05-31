from abc import ABC
import time
from cmath import sqrt


class BaseDriver(ABC):
    def image_url(self):
        raise NotImplementedError

    def name(self):
        raise NotImplementedError

    def location(self):
        raise NotImplementedError


def sqr(a):
    return a * a


class MockedDriver(BaseDriver):
    locations = []
    timestamp = 0
    speed = 0.0003
    next_point = 1

    def __init__(self, locations: [[]]):
        self.locations = locations
        self.timestamp = time.time()

    def image_url(self):
        return "https://www.google.com/url?sa=i&url=https%3A%2F%2Fcoub.com%2Fview%2F1owfrd&psig=AOvVaw0_hb2y-C2Lco4nDGBheble&ust=1622143017256000&source=images&cd=vfe&ved=0CAIQjRxqFwoTCIC0m_iH6PACFQAAAAAdAAAAABAD"

    def name(self):
        return "Oleg Oleynik"

    def location(self):
        new_timestamp = time.time()
        distance = self.speed * (new_timestamp - self.timestamp)
        prev_point = self.locations[self.next_point - 1]
        next_point = self.locations[self.next_point]
        while (sqr(prev_point[0] - next_point[0]) + sqr(prev_point[1] - next_point[1])).real <= sqr(distance).real:
            distance -= sqrt(sqr(prev_point[0] - next_point[0]) + sqr(prev_point[1] - next_point[1])).real
            self.next_point += 1
            self.next_point = self.next_point % len(self.locations)
            prev_point = self.locations[self.next_point - 1]
            next_point = self.locations[self.next_point]
            self.timestamp = new_timestamp

        segment_dis_prc = distance / sqrt(sqr(prev_point[0] - next_point[0]) + sqr(prev_point[1] - next_point[1])).real

        return [(next_point[0] - prev_point[0]) * segment_dis_prc + prev_point[0], (next_point[1] - prev_point[1]) * segment_dis_prc + prev_point[1]]


mocked_routes = [
    [
        [50.01446249308336, 36.22676655650139],
        [50.01238812937883, 36.22736904770135],
        [50.01276302101477, 36.23200725764036],
        [50.01238877574624, 36.235036477446556],
        [50.017157868684976, 36.232367008924484],
        [50.01685044278706, 36.2307134270668],
        [50.01961677420948, 36.22904475778341],
        [50.01901380034983, 36.22745420783758],
        [50.018733961035835, 36.2254448980093],
    ]
]
drivers = []


def provide_drivers():
    if len(drivers) == 0:
        for route in mocked_routes:
            drivers.append(MockedDriver(route))
    return drivers
