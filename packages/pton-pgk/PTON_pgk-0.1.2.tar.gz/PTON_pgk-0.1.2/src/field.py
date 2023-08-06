from src.area import *


class Field:
    """
            Field class polygon.

            ...

            Attributes
            ----------
            _polygon : polygon
                polygon of the field
            _area : Area
                Area of the polygon

            Methods
            -------
            components(self):
                Return the component of the Field.
            get_area(self):
                Return the area of the Field.
            get_id():
                Return the id of the area.
            """
    # private:
    _polygon = None
    _area = None

    # public:

    def __init__(self, polygon):
        """
                Constructs all the necessary attributes for the Field object.

                Parameters
                ----------
                    polygon : Polygon
                        Polygon use for the area constructor
                """
        self._polygon = polygon
        self._area = Area(self._polygon, Category.FIELD)

    def components(self):
        """
                Get the components of the object Field

                Parameters
                ----------
                None

                Returns
                -------
                Components of Field
                """
        return self._area.components()

    def get_area(self):
        """
                Get the area of the object Field

                Parameters
                ----------
                None

                Returns
                -------
                Area of Field
                """
        return self._area

    @staticmethod
    def get_id():
        """
                Get the area's id of the object Field

                Parameters
                ----------
                None

                Returns
                -------
                Area's id of Field
                """
        return Area._last_id

