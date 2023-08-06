from src.area import *


class Street:
    """
                Street class polygon.

                ...

                Attributes
                ----------
                _polygon : polygon
                    polygon of the street
                _area : Area
                    Area of the polygon

                Methods
                -------
                components(self):
                    Return the component of the Street.
                get_area(self):
                    Return the area of the Street.
                get_id():
                    Return the id of the area.
                """
    # private:
    _polygon = None
    _area = None

    # public:

    def __init__(self, polygon):
        """
                Constructs all the necessary attributes for the Street object.

                Parameters
                ----------
                    polygon : Polygon
                        Polygon use for the area constructor
                """
        self._polygon = polygon
        self._area = Area(self._polygon, Category.STREET)

    def components(self):
        """
                Get the components of the object Street

                Parameters
                ----------
                None

                Returns
                -------
                Components of Street
                """
        return self._area.components()

    def get_area(self):
        """
                Get the area of the object Street

                Parameters
                ----------
                None

                Returns
                -------
                Area of Street
                """
        return self._area

    @staticmethod
    def get_id():
        """
                Get the area's id of the object Street

                Parameters
                ----------
                None

                Returns
                -------
                Area's id of Street
                """
        return Area._last_id