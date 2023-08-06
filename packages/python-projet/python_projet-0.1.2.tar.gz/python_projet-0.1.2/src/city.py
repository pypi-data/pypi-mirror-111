import tools
from scipy.spatial import Voronoi
from shapely.geometry import Polygon, LineString, MultiPolygon
from shapely.ops import linemerge, unary_union, polygonize
import numpy as np
from math import *
import random
import matplotlib.pylab as plt
from src.generate_points import generate_random_around

from src.area import Area, Category


class City:

    def __init__(self, population, density=10000, has_walls=False, has_castle=False, has_river=False):
        """
        Represents the general class that is used to build a city at random
        according to the number of inhabitants, density, walls, castles and rivers.

        Args:
            population: int - number of inhabitants of the city
            density: int - the number of inhabitants per km2
            has_walls: boolean - set to true if the city has walls
            has_castle: boolean - set to true if the city has castle
            has_river: boolean - set to true if the city has river
            _areas: list - list of all the areas that composed the city
            _list_of_category: list - list of all the Category that a city can have
        """
        self.population = population
        self.density = density  # 10 000 ha/km2 par défaut mais peut baisser à 2000 ha/km2 avec les champs et monter à 30000 ha/km2
        self.has_walls = has_walls
        self.has_castle = has_castle
        self.has_river = has_river
        self.districts = []
        self._areas = []
        self.nbr_hab_max = 2000
        self._list_of_category = [Category.LAND, Category.HOUSE]
        if has_river:
            self._list_of_category.append(Category.RIVER)
        if has_castle:
            self._list_of_category.append(Category.CASTLE)

    def components(self):
        """
        Returns the list of areas that constitute the city's areas

        """
        if len(self._areas) > 0:
            return self._areas
        else:
            return []

    def cityBuild(self):
        """
        Generates the city randomly based on the voronoi algorithm
        algorithm which is used to randomly generate points and to keep the regions delimited by these points.
        by these points. Then it cuts each region into sub-regions and then into houses.
        Then finally it creates the boulevard(street) by making an intersection between the regions.
        Depending on the has_wall parameter, it builds or not the walls around the city.

        """

        N = round(self.population * 1800 / self.density)
        radius = (N - 2)
        nbr_points = round(sqrt(self.population / self.nbr_hab_max)) + 3
        points = np.array([[x, y] for x in np.linspace(-1, 1, nbr_points) for y in np.linspace(-1, 1, nbr_points)])
        points *= radius
        points += np.random.random((len(points), 2)) * (radius / 3)
        vor = Voronoi(points)

        regions = [r for r in vor.regions if -1 not in r and len(r) > 0]
        regions = [Polygon([vor.vertices[i] for i in r]) for r in regions]

        zone = Polygon((2 * np.random.random((8, 2)) - 1) * radius).convex_hull.buffer(radius / 2)
        regions = [r for r in regions if zone.contains(r)]

        if self.has_walls:
            walls = MultiPolygon(regions).buffer(10, join_style=2)
            plt.plot(*walls.exterior.xy)
            for tower in np.array(walls.exterior):
                plt.plot(*tower, '*')
            self._areas.append(Area(walls, Category.WALL))
        for r in regions:
            plt.plot(*r.exterior.xy, zorder=1, color='black')
            plt.fill(*r.exterior.xy, facecolor='LightGreen', zorder=2)

        for c in regions:
            left, right, top, bot = generate_random_around(5, c)

            list = []
            for co in range(0, 5):
                list.append(LineString([left[co].coords[0], right[co].coords[0]]))
                list.append(LineString([top[co].coords[0], bot[co].coords[0]]))

            list.append(c.boundary)
            borders = unary_union(list)
            merged = linemerge(borders)
            kat = polygonize(merged)

            limit_of_river, cpt1 = 2, 0
            for k in kat:
                cate = random.choice(self._list_of_category)
                if cate == Category.CASTLE:
                    self._list_of_category.remove(Category.CASTLE)
                if cate == Category.RIVER:
                    cpt1 += 1
                    if cpt1 == limit_of_river:
                        self._list_of_category.remove(Category.RIVER)
                self._areas.append(Area(k, cate))

        for i in range(0, len(regions)):
            for j in range(i + 1, len(regions)):
                inter = regions[i].intersection(regions[j])
                inter_d = inter.buffer(10, cap_style=3, join_style=3)  # cf doc pour les styles

                res = MultiPolygon([inter_d])
                for poly in res:
                    plt.plot(*poly.exterior.xy, color='grey')
                    plt.fill(*poly.exterior.xy, color='grey', zorder=4)
                    self._areas.append(Area(poly, Category.STREET))

        #plt.show()

if __name__ == "__main__":
    city = City(10000, 30000, has_walls=True, has_river=True, has_castle=True)
    city.cityBuild()
    tools.json(city, '/tmp/city.json')
