from shapely.geometry import MultiPolygon

from src import area


def construct_streets(districts, areas):
    """
        Generate a rectangle polygon as a street of a city at each intersection between two districts.

        Args:
            districts (list(Polygons)): the lists of regions(districts) to put in the city
            areas (list(Area)): the list of areas to show at the end of the program

        Returns:
            void
    """
    for i in range(len(districts)):
        for j in range(i + 1, len(districts)):
            inter = districts[i].intersection(districts[j])
            inter_d = inter.buffer(10, cap_style=3, join_style=1)
            roads = MultiPolygon([inter_d])
            for r in roads:
                road = area.Area(r, area.Category.STREET)
                areas.append(road)
