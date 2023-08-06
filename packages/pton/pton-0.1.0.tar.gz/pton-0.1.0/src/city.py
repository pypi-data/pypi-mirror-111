import math
import random
import area
import tools

from shapely.geometry import Polygon, MultiPolygon
from scipy.spatial import Voronoi
import numpy as np

from src.buildings import generate_buildings
from src.district import divide_districts, adjust_city_size
from src.street import construct_streets


class City:
    def __init__(self, population, density=10000, has_walls=False, has_castle=False, has_river=False):
        """
            Constructor of the class City
            Set all variables of the class and calls the construct_city function.

            Args:
              self (City): the city to build
              population (int): the number of inhabitants who live in the city
              density (int): the number of inhabitants by km²
              has_walls (boolean): boolean to set walls or not, default value to False
              has_castle (boolean): boolean to set a castle or not, default value to False
              has_river (boolean): boolean to set river or not, default value to False

            Tests:
                >>> city = City(10000, has_walls=True, has_river=True)
        """
        self.population = population
        self.density = density
        self.has_walls = has_walls
        self.has_castle = has_castle
        self.has_river = has_river
        self.districts = []
        self.areas = []
        self.expected_area = self.population / self.density * 1000000
        self.tot_area = 0
        self.construct_city()

    def generate_city(self):
        """
            Generate the city with its number of districts, its radius, and its regions.

            Args:
              self (City): the city to build

            Returns:
              regions (list of Polygons): a list containing all the districts of the city
              city_radius (int): the ray of the zone inside which the city will be built
        """
        nb_district = round(math.sqrt(self.population / 400) + 1)
        N = (self.population * 1000 / self.density)
        city_radius = N - 2
        points = np.array([[x, y] for x in np.linspace(-1, 1, nb_district) for y in np.linspace(-1, 1, nb_district)])
        points *= N
        points += np.random.random((len(points), 2)) * (city_radius / 3)
        vor = Voronoi(points)
        regions = [r for r in vor.regions if -1 not in r and len(r) > 0]
        regions = [Polygon([vor.vertices[i] for i in r]) for r in regions]
        return regions, city_radius

    def construct_city(self):
        """
            Construct our city depending on the characteristics of the class City.
            Calls the function `generate_city` to set regions (districts) of the city.
            Calls the function `adjust_city_size` to change the size of the city depending on the expected size with the given density.
            Sets a river as a moat and walls all around the city or not.
            Calls the function `generate_buildings` to generate all the houses, mansions, markets, churches, a cathedral...
            Constructs the streets with the function `construct_streets`.

            Args:
              self (City): the city to build

            Returns:
              void
        """
        regions, city_radius = self.generate_city()

        adjust_city_size(self, regions, city_radius)

        if self.has_river:
            moat = MultiPolygon(self.districts).buffer(50, join_style=2)
            city_moat = area.Area(moat, area.Category.RIVER)
            self.areas.append(city_moat)

        if self.has_walls:
            walls = MultiPolygon(self.districts).buffer(20, join_style=2)
            city_walls = area.Area(walls, area.Category.WALL)
            self.areas.append(city_walls)

        generate_buildings(self)

        construct_streets(self.districts, self.areas)

    def components(self):
        """
            Function components, to call the class with the viewer.py.

            Args:
              self (City): the city to build

            Returns:
              list: empty or self.areas
        """
        if len(self.areas) > 0:
            return self.areas
        else:
            return []


if __name__ == "__main__":
    city = City(10000, density=10000, has_walls=True, has_castle=False, has_river=True)
    tools.json(city, '/tmp/city.json')
