from area import *


class Forest:
    """
            Forest class polygon.

            ...

            Attributes
            ----------
            _polygon : polygon
                polygon of the Forest
            _area : Area
                Area of the polygon

            Methods
            -------
            components(self):
                Return the component of the Forest.
            get_area(self):
                Return the area of the Forest.
            get_id():
                Return the id of the area.
            """
    # private:
    _polygon = None
    _area = None

    # public:

    def __init__(self, polygon):
        """
                Constructs all the necessary attributes for the Forest object.

                Parameters
                ----------
                    polygon : Polygon
                        Polygon use for the area constructor
                """
        self._polygon = polygon
        self._area = Area(self._polygon, Category.FOREST)

    def components(self):
        """
                Get the components of the object Forest

                Parameters
                ----------
                None

                Returns
                -------
                Components of Forest
                """
        return self._area.components()

    def get_area(self):
        """
                Get the area of the object Forest

                Parameters
                ----------
                None

                Returns
                -------
                Area of Forest
                """
        return self._area

    @staticmethod
    def get_id():
        """
                Get the area's id of the object Forest

                Parameters
                ----------
                None

                Returns
                -------
                Area's id of Forest
                """
        return Area._last_id

