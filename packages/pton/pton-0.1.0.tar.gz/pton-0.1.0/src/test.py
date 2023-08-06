import unittest

from src.city import City


def get_city_informations(population=50000, density=10000):
    """
        Calculates the expected area and the actual total area of the city, depending of the population and density.

        Args:
            population (int): the number of inhabitants, default value to 50000
            density (int): the number of inhabitants by km², default value to 10000

        Returns:
            a couple of two integers
    """
    city = City(population, density=density)
    city_size = round(city.tot_area / 1000000, 3)

    print("Nb habitants:", city.population, "- Densité:", city.density)
    print("Aire totale:", round(city.tot_area), "m²", "(soit", city_size, "km²),",
          "expected ~", round(city.population / city.density, 3), "km²\n")
    return city.expected_area, city.tot_area


class MyTestCase(unittest.TestCase):

    def test_city_size_with_population(self):
        """
            Test with different numbers for population to check if the area of the generated city is valid.
        """
        for i in range(4000, 50001, 2000):
            expected_area, city_size = get_city_informations(i)
            self.assertTrue(expected_area * 5 / 4 >= city_size >= expected_area * 3 / 4)

    def test_city_size_with_density(self):
        """
            Test with different densities to check if the area of the generated city is valid.
        """
        for i in range(5000, 30000, 2500):
            expected_area, city_size = get_city_informations(density=i)
            self.assertTrue(expected_area * 5 / 4 >= city_size >= expected_area * 3 / 4)


if __name__ == '__main__':
    unittest.main()
