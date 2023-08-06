from area import *


class Castle:
    """
        Castle class polygon.

        ...

        Attributes
        ----------
        _polygon : polygon
            polygon of the castle
        _area : Area
            Area of the polygon

        Methods
        -------
        components(self):
            Return the component of the Castle.
        get_area(self):
            Return the area of the Castle.
        get_id():
            Return the id of the area.
        """
    # private:
    _polygon = None
    _area = None

    # public:

    def __init__(self, polygon):
        """
                Constructs all the necessary attributes for the Castle object.

                Parameters
                ----------
                    polygon : Polygon
                        Polygon use for the area constructor
                """
        self._polygon = polygon
        self._area = Area(self._polygon, Category.CASTLE)

    def components(self):
        """
                Get the components of the object Castle

                Parameters
                ----------
                None

                Returns
                -------
                Components of Castle
                """
        return self._area.components()

    def get_area(self):
        """
                Get the area of the object Castle

                Parameters
                ----------
                None

                Returns
                -------
                Area of Castle
                """
        return self._area

    @staticmethod
    def get_id():
        """
                Get the area's id of the object Castle

                Parameters
                ----------
                None

                Returns
                -------
                Area's id of Castle
                """
        return Area._last_id

