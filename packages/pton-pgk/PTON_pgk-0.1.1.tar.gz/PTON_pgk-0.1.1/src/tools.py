from collections import Iterable

from shapely.geometry import mapping
import fiona

SCHEMA = {
    'geometry': 'Polygon',
    'properties': {'category': 'int'},
}


def write(obj, stream):
    if isinstance(obj, Iterable):
        for e in obj:
            write(e, stream)
    else:
        stream.write({
            'geometry': mapping(obj._polygon),
            'properties': {'category': obj._category.value},
        })


def json(what, filename):
    with fiona.open(filename, 'w', 'GeoJSON', SCHEMA) as c:
        write(what.components(), c)
