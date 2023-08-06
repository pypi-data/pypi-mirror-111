import random

from src import area
from src.district import divide_districts


def generate_buildings(city):
    """
        Generate the buildings in the city.
        Creates mainly houses (90%), but also mansions (10%).
        The biggest polygons become lakes, and one (or zero) cathedral.
        The smallest ones are parks.
        There are one church and between 0 and 2 markets in each district.
        If the city has to have a castle, one district becomes the castle and will not be split.

        Args:
          city (City): the city where we generate the buildings in

        Returns:
          void
    """
    cathedral_placed = False
    cathedral_district = random.randint(0, len(city.districts))
    mansion_prob = [area.Category.HOUSE] * 9 + [area.Category.MANSION]
    castle_district = random.randint(0, len(city.districts))

    for r in city.districts:
        if castle_district == 0 and city.has_castle:
            cathedral_district -= 1
            castle_district -= 1
            a = area.Area(r, area.Category.FORT)
            city.areas.append(a)
            continue
        poly_split = divide_districts(r, 5000, 20)
        church_placed = False
        church_place = random.randint(0, len(poly_split))
        market_placed = False
        market_place = [random.randint(0, len(poly_split)), random.randint(0, len(poly_split))]
        for p in poly_split:
            if p.area < 1500:
                category = area.Category.PARK
            elif p.area > 4900:
                if cathedral_district <= 0 and not cathedral_placed:
                    category = area.Category.CATHEDRAL
                    cathedral_placed = True
                else:
                    category = area.Category.LAKE
            elif church_place <= 0 and not church_placed:
                category = area.Category.CHURCH
                church_placed = True
            elif (0 in market_place) and not market_placed:
                category = area.Category.MARKET
                if market_place[0] <= 0 and market_place[1] <= 0:
                    market_placed = True
            else:
                category = random.choice(mansion_prob)
            church_place -= 1
            market_place = [p - 1 for p in market_place]

            a = area.Area(p, category)
            city.areas.append(a)

        cathedral_district -= 1
        castle_district -= 1