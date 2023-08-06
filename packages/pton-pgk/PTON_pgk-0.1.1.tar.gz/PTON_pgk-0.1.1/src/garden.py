from area import *


class Garden:
    """
            Garden class polygon.

            ...

            Attributes
            ----------
            _polygon : polygon
                polygon of the Garden
            _area : Area
                Area of the polygon

            Methods
            -------
            components(self):
                Return the component of the Garden.
            get_area(self):
                Return the area of the Garden.
            get_id():
                Return the id of the area.
            """
    # private:
    _polygon = None
    _area = None

    # public:

    def __init__(self, polygon):
        """
                Constructs all the necessary attributes for the Garden object.

                Parameters
                ----------
                    polygon : Polygon
                        Polygon use for the area constructor
                """
        self._polygon = polygon
        self._area = Area(self._polygon, Category.GARDEN)

    def components(self):
        """
                Get the components of the object Garden

                Parameters
                ----------
                None

                Returns
                -------
                Components of Garden
                """
        return self._area.components()

    def get_area(self):
        """
                Get the area of the object Garden

                Parameters
                ----------
                None

                Returns
                -------
                Area of Garden
                """
        return self._area

    @staticmethod
    def get_id():
        """
                Get the area's id of the object Garden

                Parameters
                ----------
                None

                Returns
                -------
                Area's id of Garden
                """
        return Area._last_id
