import math
from typing import TypedDict


class Coordinates(TypedDict):
    min_latitude: float
    max_latitude: float
    min_longitude: float
    max_longitude: float


def find_min_max_latitude_longitude(latitude: float, longitude: float, distance: float) -> Coordinates:
    """Функция находит минимальные и максимальные значения широты и долготы
       для заданных координат и дистанции.
       Важно! Дистанция передается в километрах
    """

    degrees_per_km = 1 / 111  # Коэффициент перевода км в градусы
    distance_degrees = distance * degrees_per_km
    distance_degrees_for_longitude = distance_degrees / (111 * math.cos(math.radians(latitude)))

    min_latitude = latitude - distance_degrees
    max_latitude = latitude + distance_degrees
    min_longitude = longitude - distance_degrees_for_longitude
    max_longitude = longitude + distance_degrees_for_longitude

    result = Coordinates(min_latitude=min_latitude,
                         max_latitude=max_latitude,
                         min_longitude=min_longitude,
                         max_longitude=max_longitude)

    return result


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Функция расчета дистанции по формуле harvesine.
       Может использоваться для более точной фильтрации
       Важно! Дистанция возвращается в километрах
    """

    # Радиус Земли в километрах
    R = 6371

    # Перевод координат в радианы
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Разница между координатами
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    # Формула haversine
    a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(
        dlon / 2) * math.sin(dlon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c

    return distance
