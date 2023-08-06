import tools
import numpy as np
import random as rand

from shapely.geometry import Polygon, MultiPolygon
from scipy.spatial import Voronoi

from district import District
from wall import Wall


class City:
    """
        A class to represent a City.
        This is the main class of this project.
        City is use to create a randomized city with some option that you can write in a Json file.
        ...

        Attributes
        ----------
        population : int
            Population of the city
        density : int
            Density of the city
        districts : list
            List of all district in the city
        has_walls : bool
            If True, the city has walls
        has_castle : bool
            If True, the city has a district castle
        has_lake : bool
            If True, the city has a district lake

        Methods
        -------
        components():
            Get all districts components of the city.
        """

    def __init__(self, population, density=10000, has_walls=False, has_castle=False, has_lake=False, seed=None):
        """
        Constructs all the necessary attributes for the city object.

        Parameters
        ----------
            population : int
                Population of the city
            density : int
                Density of the city
            has_walls : bool
                If True, the city has walls
            has_castle : bool
                If True, the city has a district castle
            has_lake : bool
                If True, the city has a district lake
            seed : int
                Seed for random generation
        """
        np.random.seed(seed)
        rand.seed(seed, 2)

        self.population = population
        self.density = density

        # Some options
        self.has_castle = has_castle
        self.has_lake = has_lake
        self.has_walls = has_walls

        self.districts = []

        # Max number of district per row
        max_district = 8 if density > 2000 else 5
        # Radius of the city
        radius = density / 2
        # Randomized points of districts centers
        points = np.array(
            [[x, y] for x in np.linspace(-1, 1, max_district) for y in np.linspace(-1, 1, max_district)])
        points *= radius
        points += np.random.random((len(points), 2)) * (radius / 6)

        # Make the Voronoi partition of the plane
        vor = Voronoi(points)

        # Get all regions that are in a specific random zone
        zone = Polygon((2 * np.random.random((8, 2)) - 1) * radius).convex_hull.buffer(radius / 2)

        regions = [r for r in vor.regions if -1 not in r and len(r) > 0]
        regions = [Polygon([vor.vertices[i] for i in r]) for r in regions]
        regions = [r for r in regions if zone.contains(r)]

        # Make walls if necessary
        if self.has_walls:
            self.districts.append(Wall(MultiPolygon(regions).buffer(density * 0.008, join_style=1, cap_style=3)))

        # Add all districts in the city
        for polygon in regions:
            if self.has_castle and (rand.randint(0, 100) < 20 or regions[-1] == polygon):
                self.districts.append(District(polygon, 3, density, seed=seed))
                self.has_castle = False
            elif self.has_lake and (rand.randint(0, 100) < 20 or regions[-2] == polygon):
                self.districts.append(District(polygon, 4, density, seed=seed))
                self.has_lake = False
            else:
                r = rand.randint(0, 100)
                self.districts.append(District(polygon, 1 if r > 10 else 2, density, seed=seed))

    def components(self):
        """
        Get the components of the object City

        Parameters
        ----------
        None

        Returns
        -------
        Components of City
        """
        if len(self.districts) > 0:
            return [block.components() for block in self.districts]
        else:
            return []


if __name__ == "__main__":
    city = City(10000, 10000, has_walls=True, has_castle=True, has_lake=True, seed=None)
    # Population is mandatory
    # By default density=10000, has_walls=False, has_castle=False, has_lake=False
    tools.json(city, '../tmp/city.json')
