from src.area import *


class Market:
    """
                Market class polygon.

                ...

                Attributes
                ----------
                _polygon : polygon
                    polygon of the Market
                _area : Area
                    Area of the polygon

                Methods
                -------
                components(self):
                    Return the component of the Market.
                get_area(self):
                    Return the area of the Market.
                get_id():
                    Return the id of the area.
                """
    # private:
    _polygon = None
    _area = None

    # public:

    def __init__(self, polygon):
        """
                Constructs all the necessary attributes for the Market object.

                Parameters
                ----------
                    polygon : Polygon
                        Polygon use for the area constructor
                """
        self._polygon = polygon
        self._area = Area(self._polygon, Category.MARKET)

    def components(self):
        """
                Get the components of the object Market

                Parameters
                ----------
                None

                Returns
                -------
                Components of Market
                """
        return self._area.components()

    def get_area(self):
        """
                Get the area of the object Market

                Parameters
                ----------
                None

                Returns
                -------
                Area of Market
                """
        return self._area

    @staticmethod
    def get_id():
        """
                Get the area's id of the object Market

                Parameters
                ----------
                None

                Returns
                -------
                Area's id of Market
                """
        return Area._last_id