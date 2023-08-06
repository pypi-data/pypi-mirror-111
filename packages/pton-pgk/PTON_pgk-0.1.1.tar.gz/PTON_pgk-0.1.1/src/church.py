from area import *


class Church:
    """
            Church class polygon.

            ...

            Attributes
            ----------
            _polygon : polygon
                polygon of the church
            _area : Area
                Area of the polygon

            Methods
            -------
            components(self):
                Return the component of the Church.
            get_area(self):
                Return the area of the Church.
            get_id():
                Return the id of the area.
            """
    # private:
    _polygon = None
    _area = None

    # public:

    def __init__(self, polygon):
        """
                Constructs all the necessary attributes for the Church object.

                Parameters
                ----------
                    polygon : Polygon
                        Polygon use for the area constructor
                """
        self._polygon = polygon
        self._area = Area(self._polygon, Category.CHURCH)

    def components(self):
        """
                Get the components of the object Church

                Parameters
                ----------
                None

                Returns
                -------
                Components of Church
                """
        return self._area.components()

    def get_area(self):
        """
                Get the area of the object Church

                Parameters
                ----------
                None

                Returns
                -------
                Area of Church
                """
        return self._area

    @staticmethod
    def get_id():
        """
                Get the area's id of the object Church

                Parameters
                ----------
                None

                Returns
                -------
                Area's id of Church
                """
        return Area._last_id
