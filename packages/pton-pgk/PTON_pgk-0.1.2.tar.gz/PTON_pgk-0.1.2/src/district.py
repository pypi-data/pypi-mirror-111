import random

from scipy.spatial import Voronoi
import numpy as np
import random as rand

from shapely.geometry import Polygon, Point, MultiPoint

from src.castle import Castle
from src.church import Church
from src.forest import Forest
from src.garden import Garden
from src.house import House
from src.fort import Fort
from src.field import Field
from src.lake import Lake
from src.mansion import Mansion
from src.market import Market
from src.park import Park
from src.street import Street
from src.townhall import Townhall


# List of constructor use in a category 1 district
ctor = [House, Park, Market, Mansion, Townhall, Church]


def cut_poly(polygon, n=50):
    """
    Find random points in a polygon to divide it

    Parameters
    ----------
    polygon : Polygon
        Input polygon
    n : int
        Number of points to find, default is 50

    Returns
    -------
    points : list of tuples
        Coordinates of points in the polygon
    """
    # Polygon bounds
    (min_x, min_y, max_x, max_y) = polygon.bounds
    nb = 0
    points = []
    (min_x, min_y, max_x, max_y) = (round(min_x), round(min_y), round(max_x), round(max_y))

    # Number of pieces the polygon need to be cut
    while nb < n:
        x = rand.randint(min_x, max_x)
        y = rand.randint(min_y, max_y)
        # Check if the polygon contains (x,y) point
        if polygon.contains(Point(x, y)):
            points.append((x, y))
            nb += 1
    return points


def voronoi_finite_polygons_2d(vor, radius=None):
    """
    Reconstruct infinite voronoi regions in a 2D diagram to finite
    regions.

    Parameters
    ----------
    vor : Voronoi
        Input diagram
    radius : float, optional
        Distance to 'points at infinity'.

    Returns
    -------
    regions : list of tuples
        Indices of vertices in each revised Voronoi regions.
    vertices : list of tuples
        Coordinates for revised Voronoi vertices. Same as coordinates
        of input vertices, with 'points at infinity' appended to the
        end.

    """

    if vor.points.shape[1] != 2:
        raise ValueError("Requires 2D input")

    new_regions = []
    new_vertices = vor.vertices.tolist()

    center = vor.points.mean(axis=0)
    if radius is None:
        radius = vor.points.ptp().max()

    # Construct a map containing all ridges for a given point
    all_ridges = {}
    for (p1, p2), (v1, v2) in zip(vor.ridge_points, vor.ridge_vertices):
        all_ridges.setdefault(p1, []).append((p2, v1, v2))
        all_ridges.setdefault(p2, []).append((p1, v1, v2))

    # Reconstruct infinite regions
    for p1, region in enumerate(vor.point_region):
        vertices = vor.regions[region]

        if all(v >= 0 for v in vertices):
            # finite region
            new_regions.append(vertices)
            continue

        # reconstruct a non-finite region
        ridges = all_ridges[p1]
        new_region = [v for v in vertices if v >= 0]

        for p2, v1, v2 in ridges:
            if v2 < 0:
                v1, v2 = v2, v1
            if v1 >= 0:
                # finite ridge: already in the region
                continue

            # Compute the missing endpoint of an infinite ridge

            t = vor.points[p2] - vor.points[p1]  # tangent
            t /= np.linalg.norm(t)
            n = np.array([-t[1], t[0]])  # normal

            midpoint = vor.points[[p1, p2]].mean(axis=0)
            direction = np.sign(np.dot(midpoint - center, n)) * n
            far_point = vor.vertices[v2] + direction * radius

            new_region.append(len(new_vertices))
            new_vertices.append(far_point.tolist())

        # sort region counterclockwise
        vs = np.asarray([new_vertices[v] for v in new_region])
        c = vs.mean(axis=0)
        angles = np.arctan2(vs[:, 1] - c[1], vs[:, 0] - c[0])
        new_region = np.array(new_region)[np.argsort(angles)]

        # finish
        new_regions.append(new_region.tolist())

    return new_regions, np.asarray(new_vertices)


def new_poly(polygon, liste, ctor1, ctor2, density, ratio):
    """
        Divide a polygon in two pieces, a border and a center.

        Parameters
        ----------
        polygon : Polygon
            Input Polygon
        liste : list of objects
            List to add the both objects
        ctor1 : constructor
            Constructor of the border object
        ctor2 : constructor
            Constructor of the center object
        density : int
            Density of the city
        ratio : float
            Ratio of border object

        Returns
        -------
        None
    """
    new_pol = polygon.difference(polygon.buffer(-density * ratio, cap_style=2))
    liste.append(ctor1(polygon.buffer(-density * ratio, cap_style=2)))
    liste.append(ctor2(new_pol))


class District:
    """
            A class to represent a City.
            This is the main class of this project.
            City is use to create a randomized city with some option that you can write in a Json file.
            ...

            Attributes
            ----------
            _polygon : Polygon
                Polygon of the district
            _density : int
                Density of the city
            _category : int
                Type of district
            _blocks : List of object
                List of all objects composing the district
            _roads : List of Street
                List of all Streets composing the district

            Methods
            -------
            cut_district(self):
                Cut a category 1 district in multiple object
            components():
                Get the district components.
    """
    # private:
    _polygon = None

    def __init__(self, polygon, category, density, seed=None):
        """
        Constructs all the necessary attributes for the district object.

        Parameters
        ----------
            polygon : Polygon
                Polygon of the district
            density : int
                Density of the city
            category : int
                Category of the district
            seed : int
                Seed for random generation
        """
        np.random.seed(seed)
        rand.seed(seed, 2)

        self._polygon = polygon
        self._category = category
        self._blocks = []
        self._density = density
        self._roads = []
        # Residential district
        if self._category == 1:
            self.cut_district()
        # Field district
        elif self._category == 2:
            self._blocks.append(Field(polygon))
        # Castle district
        elif self._category == 3:
            new_poly(polygon, self._blocks, Castle, Fort, density, 0.02)
        # Lake district
        elif self._category == 4:
            new_poly(polygon, self._blocks, Lake, Forest, density, 0.02)

    def cut_district(self):
        """
            Divide a district in many components pieces.
            From randoms points, make a new voronoi diagram from a definite polygon

            Parameters
            ----------
            None

            Returns
            -------
            None
        """
        # Cut the polygon into pieces with voronoi diagram
        points = cut_poly(self._polygon)
        vor = Voronoi(points)
        x, y = self._polygon.exterior.xy
        points = [(x[i], y[i]) for i in range(len(x))]

        # Get regions from the voronoi diagram
        regions, vertices = voronoi_finite_polygons_2d(vor)

        # Make a mask to cut regions at the border district
        pts = MultiPoint([Point(i) for i in points])
        mask = pts.convex_hull

        for region in regions:
            polygon = vertices[region]
            shape = list(polygon.shape)
            shape[0] += 1
            # Get the intersection between the region and the polygon
            p = Polygon(np.append(polygon, polygon[0]).reshape(*shape)).intersection(mask)
            new_vertices = np.array(list(zip(p.boundary.coords.xy[0][:-1], p.boundary.coords.xy[1][:-1])))
            tmp = [(x, y) for x, y in new_vertices]
            # Create a new polygon
            poly = Polygon(tmp)
            # Create Street from it
            road = poly.difference(poly.buffer(-self._density * 0.002, join_style=1, cap_style=3))
            index = 0 if random.randint(0, 100) > 3 else random.randint(1, len(ctor) - 1)
            # Generate a House 97% of the time
            # Else create a random building
            if index == 0:
                new_poly(poly, self._blocks, Garden, House, self._density, 0.009)
            else:
                self._blocks.append(ctor[index](poly.buffer(-self._density * 0.002, join_style=2, cap_style=3)))
            self._blocks.append(Street(road))

    def components(self):
        """
        Get the components of the object District

        Parameters
        ----------
        None

        Returns
        -------
        Components of District
        """
        if len(self._blocks) > 0:
            return [block.components() for block in self._blocks]
        else:
            return []
