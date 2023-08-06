from area import *


class Mansion:
    """
                Mansion class polygon.

                ...

                Attributes
                ----------
                _polygon : polygon
                    polygon of the mansion
                _area : Area
                    Area of the polygon

                Methods
                -------
                components(self):
                    Return the component of the Mansion.
                get_area(self):
                    Return the area of the Mansion.
                get_id():
                    Return the id of the area.
                """
    # private:
    _polygon = None
    _area = None

    # public:

    def __init__(self, polygon):
        """
                Constructs all the necessary attributes for the Mansion object.

                Parameters
                ----------
                    polygon : Polygon
                        Polygon use for the area constructor
                """
        self._polygon = polygon
        self._area = Area(self._polygon, Category.MANSION)

    def components(self):
        """
                Get the components of the object Mansion

                Parameters
                ----------
                None

                Returns
                -------
                Components of Mansion
                """
        return self._area.components()

    def get_area(self):
        """
                Get the area of the object Mansion

                Parameters
                ----------
                None

                Returns
                -------
                Area of Mansion
                """
        return self._area

    @staticmethod
    def get_id():
        """
                Get the area's id of the object Mansion

                Parameters
                ----------
                None

                Returns
                -------
                Area's id of Mansion
                """
        return Area._last_id
