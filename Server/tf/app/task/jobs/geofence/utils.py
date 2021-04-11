import random

from shapely.geometry import Polygon, Point

from app.geofence.models import WrapperRect


def get_fencing_polygon(coordinates):
    result = []
    for coordinate in coordinates:
        result.append((float(coordinate.latitude), float(coordinate.longitude)))
    return Polygon(result)


def build_wrapper_rect(polygon):
    min_x, min_y, max_x, max_y = polygon.bounds
    return WrapperRect(maxX=str(max_x), minX=str(min_x), maxY=str(max_y), minY=str(min_y))


def random_point_within(poly):
    min_x, min_y, max_x, max_y = poly.bounds
    x = random.uniform(min_x, max_x)
    y = random.uniform(min_y, max_y)
    return Point([x, y])