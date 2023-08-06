from src.area import *


class Townhall:
    """
                Castle class polygon.

                ...

                Attributes
                ----------
                _polygon : polygon
                    polygon of the TownHall
                _area : Area
                    Area of the polygon

                Methods
                -------
                components(self):
                    Return the component of the TownHall.
                get_area(self):
                    Return the area of the TownHall.
                get_id():
                    Return the id of the area.
                """
    # private:
    _polygon = None
    _area = None

    # public:

    def __init__(self, polygon):
        """
                Constructs all the necessary attributes for the TownHall object.

                Parameters
                ----------
                    polygon : Polygon
                        Polygon use for the area constructor
                """
        self._polygon = polygon
        self._area = Area(self._polygon, Category.TOWNHALL)

    def components(self):
        """
                Get the components of the object TownHall

                Parameters
                ----------
                None

                Returns
                -------
                Components of TownHall
                """
        return self._area.components()

    def get_area(self):
        """
                Get the area of the object TownHall

                Parameters
                ----------
                None

                Returns
                -------
                Area of TownHall
                """
        return self._area

    @staticmethod
    def get_id():
        """
                Get the area's id of the object TownHall

                Parameters
                ----------
                None

                Returns
                -------
                Area's id of TownHall
                """
        return Area._last_id