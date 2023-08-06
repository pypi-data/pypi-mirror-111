from area import *


class Park:
    """
                Park class polygon.

                ...

                Attributes
                ----------
                _polygon : polygon
                    polygon of the park
                _area : Area
                    Area of the polygon

                Methods
                -------
                components(self):
                    Return the component of the Park.
                get_area(self):
                    Return the area of the Park.
                get_id():
                    Return the id of the area.
                """
    # private:
    _polygon = None
    _area = None

    # public:

    def __init__(self, polygon):
        """
                Constructs all the necessary attributes for the Park object.

                Parameters
                ----------
                    polygon : Polygon
                        Polygon use for the area constructor
                """
        self._polygon = polygon
        self._area = Area(self._polygon, Category.PARK)

    def components(self):
        """
                Get the components of the object Park

                Parameters
                ----------
                None

                Returns
                -------
                Components of Park
                """
        return self._area.components()

    def get_area(self):
        """
                Get the area of the object Park

                Parameters
                ----------
                None

                Returns
                -------
                Area of Park
                """
        return self._area

    @staticmethod
    def get_id():
        """
                Get the area's id of the object Park

                Parameters
                ----------
                None

                Returns
                -------
                Area's id of Park
                """
        return Area._last_id
