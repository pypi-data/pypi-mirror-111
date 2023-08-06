import random

import numpy as np
from shapely import ops
from shapely.geometry import LineString, box, GeometryCollection, Polygon, MultiPolygon

from src import area


def divide_polygon(height, width, bounds):
    """
        Split randomly a Polygon into two parts depending on the width or the height of the polygon.

        Args:
            height (int): the height of the polygon
            width (int): the width of the polygon
            bounds (list(points)): list of points representing the approximate shape of the polygon

        Returns:
            couple of polygons as the result of the split of the initial one
    """
    box_glob = box(bounds[0], bounds[1], bounds[2], bounds[3])
    box_coords = list(box_glob.exterior.coords)
    bottom_right, top_right, top_left, bottom_left = box_coords[0:4]

    if height >= width:
        left_point = (bottom_left[0], random.uniform(bottom_left[1], top_left[1]))
        right_point = (bottom_right[0], random.uniform(bottom_right[1], top_right[1]))
        middle_point = (random.uniform(left_point[0], right_point[0]), random.uniform(left_point[1], right_point[1]))
        line = LineString([left_point, middle_point, right_point])
        poly_a, poly_b = ops.split(box_glob, line)
    else:
        bottom_point = (random.uniform(bottom_left[0], bottom_right[0]), bottom_left[1])
        top_point = (random.uniform(top_left[0], top_right[0]), top_left[1])
        middle_point = (random.uniform(bottom_point[0], top_point[0]), random.uniform(bottom_point[1], top_point[1]))
        line = LineString([bottom_point, middle_point, top_point])
        poly_a, poly_b = ops.split(box_glob, line)

    return poly_a, poly_b


def divide_districts(geometry, maximum_size, count=0):
    """
        Split all districts of the city into polygons with a maximum_size as threshold, calling on each the function `divide_polygon`.

        Args:
            geometry (Polygon): the district to divide
            maximum_size (int): the maximum_size of the polygon, it can not have a bigger area
            count (int): counter for the recursion in the function, default value to 0

        Returns:
            list, containing all divided Polygons of the district
    """
    bounds = geometry.bounds
    width = bounds[2] - bounds[0]
    height = bounds[3] - bounds[1]
    if geometry.area <= maximum_size or count == 250:
        return [geometry]

    poly_a, poly_b = divide_polygon(height, width, bounds)

    result = []
    for poly in (poly_a, poly_b,):
        inter = geometry.intersection(poly)
        if not isinstance(inter, GeometryCollection):
            inter = [inter]
        for p in inter:
            if isinstance(p, (Polygon, MultiPolygon)):
                result.extend(divide_districts(p, maximum_size, count + 1))
    if count > 0:
        return result
    final_result = []
    for r in result:
        if isinstance(r, MultiPolygon):
            final_result.extend(r)
        else:
            final_result.append(r)
    return final_result


def adjust_city_size(city, regions, city_radius):
    """
        Search the best size for the city, with the expected area found with the density.
        Set the zone to a category Land or Forest, all around the city.

        Args:
            city (City): the city to resize
            regions (list(Polygons)): the lists of regions(districts) to put in the city
            city_radius (int): the ray of the zone inside which the city will be built

        Returns:
            list, containing all divided Polygons of the district
    """
    city.districts = []
    for _ in range(100):
        city.tot_area = 0
        zone = Polygon((2 * np.random.random((8, 2)) - 1) * city_radius).convex_hull.buffer(city_radius / 2)

        city.districts = [r for r in regions if zone.contains(r)]
        for r in city.districts:
            city.tot_area += r.area
        if city.expected_area * 5 / 4 >= city.tot_area >= city.expected_area * 3 / 4:
            break
        if city.expected_area + city.expected_area / 4 >= city.tot_area:
            city_radius *= 21 / 20
        if city.tot_area >= city.expected_area - city.expected_area / 4:
            city_radius *= 9 / 10
    city_bounds = area.Area(zone, random.choice([area.Category.LAND,area.Category.FOREST]))
    city.areas.append(city_bounds)
