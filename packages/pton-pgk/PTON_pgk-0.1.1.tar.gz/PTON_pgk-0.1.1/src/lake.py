from area import *


class Lake:
    """
                Lake class polygon.

                ...

                Attributes
                ----------
                _polygon : polygon
                    polygon of the lake
                _area : Area
                    Area of the polygon

                Methods
                -------
                components(self):
                    Return the component of the Lake.
                get_area(self):
                    Return the area of the Lake.
                get_id():
                    Return the id of the area.
                """
    # private:
    _polygon = None
    _area = None

    # public:

    def __init__(self, polygon):
        """
                Constructs all the necessary attributes for the Lake object.

                Parameters
                ----------
                    polygon : Polygon
                        Polygon use for the area constructor
                """
        self._polygon = polygon
        self._area = Area(self._polygon, Category.LAKE)

    def components(self):
        """
                Get the components of the object Lake

                Parameters
                ----------
                None

                Returns
                -------
                Components of Lake
                """
        return self._area.components()

    def get_area(self):
        """
                Get the area of the object Lake

                Parameters
                ----------
                None

                Returns
                -------
                Area of Lake
                """
        return self._area

    @staticmethod
    def get_id():
        """
                Get the area's id of the object Lake

                Parameters
                ----------
                None

                Returns
                -------
                Area's id of Lake
                """
        return Area._last_id