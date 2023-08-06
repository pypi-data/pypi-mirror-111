from src.area import *


class Wall:
    """
                Wall class polygon.

                ...

                Attributes
                ----------
                _polygon : polygon
                    polygon of the Wall
                _area : Area
                    Area of the polygon

                Methods
                -------
                components(self):
                    Return the component of the Wall.
                get_area(self):
                    Return the area of the Wall.
                get_id():
                    Return the id of the area.
                """
    # private:
    _polygon = None
    _area = None

    # public:

    def __init__(self, polygon):
        """
                Constructs all the necessary attributes for the Wall object.

                Parameters
                ----------
                    polygon : Polygon
                        Polygon use for the area constructor
                """
        self._polygon = polygon
        self._area = Area(self._polygon, Category.WALL)

    def components(self):
        """
                Get the components of the object Wall

                Parameters
                ----------
                None

                Returns
                -------
                Components of Wall
                """
        return self._area.components()

    def get_area(self):
        """
                Get the area of the object Wall

                Parameters
                ----------
                None

                Returns
                -------
                Area of Wall
                """
        return self._area

    @staticmethod
    def get_id():
        """
                Get the area's id of the object Wall

                Parameters
                ----------
                None

                Returns
                -------
                Area's id of Wall
                """
        return Area._last_id
