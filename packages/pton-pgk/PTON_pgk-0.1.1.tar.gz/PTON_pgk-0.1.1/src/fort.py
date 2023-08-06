from area import *


class Fort:
    """
            Fort class polygon.

            ...

            Attributes
            ----------
            _polygon : polygon
                polygon of the fort
            _area : Area
                Area of the polygon

            Methods
            -------
            components(self):
                Return the component of the Fort.
            get_area(self):
                Return the area of the Fort.
            get_id():
                Return the id of the area.
            """
    # private:
    _polygon = None
    _area = None

    # public:

    def __init__(self, polygon):
        """
                Constructs all the necessary attributes for the Fort object.

                Parameters
                ----------
                    polygon : Polygon
                        Polygon use for the area constructor
                """
        self._polygon = polygon
        self._area = Area(self._polygon, Category.FORT)

    def components(self):
        """
                Get the components of the object Fort

                Parameters
                ----------
                None

                Returns
                -------
                Components of Fort
                """
        return self._area.components()

    def get_area(self):
        """
                Get the area of the object Fort

                Parameters
                ----------
                None

                Returns
                -------
                Area of Fort
                """
        return self._area

    @staticmethod
    def get_id():
        """
                Get the area's id of the object Fort

                Parameters
                ----------
                None

                Returns
                -------
                Area's id of Fort
                """
        return Area._last_id