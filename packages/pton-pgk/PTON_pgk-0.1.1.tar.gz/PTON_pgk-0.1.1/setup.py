# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['src', 'src.pton_pgk', 'tests']

package_data = \
{'': ['*'], 'tests': ['.ipynb_checkpoints/*']}

install_requires = \
['Shapely>=1.7.1,<2.0.0', 'geopandas>=0.9.0,<0.10.0', 'numpy>=1.21.0,<2.0.0']

setup_kwargs = {
    'name': 'pton-pgk',
    'version': '0.1.1',
    'description': 'Medieval City',
    'long_description': "# PTON Project : City Generator\n**Marius PON** et **Tom THIL**, *EPITA Promo 2023*\n\nThis projects consists in a medieval city generator in python. The generated city depends on attributes as the number of population and its density.\n\n## Features\n- Generate a medieval city depending on the number of population and the density of the population\n- It is possible to generate or not a castle, a wall and a lake in the city\n- The result is stored in a *.json* file\n- The user has to possibility to use a city viewer\n\n\n## How to use\n\n### Instantiate a 'City' object\nThis project can be executed with your *Pycharm* IDE. You have to run the *city.py* file, located in the *src/* repository.\n\nA city object is instanciated as follows :\n``city = City(population, density, has_walls, has_castle, has_lake)``\n\nA City object has already been created in *city.py* with values giving good results.  You can custom the generated cities by replacing them by your own values.\n\nThere is a last *'seed'* parameter, none as default. 2 cities generated with the same parameters and the same seeds will be identical.\n\n### Generating a *.json* file\nYou can generate a *.json* file for your 'city' object as follows :\n``tools.json(city, 'path/to/your/file/.json')``\n\n### Use the city viewer\nTo use the **city viewer**, you have to run run *viewer.py*. There is a *view* function taking as parameter a *.json* file corresponding to a generated city. By default, the fonction takes *tmp/city.json* as argument.\n\n## Documentation\nA documentation has already been generated (in *docs/_build/html/tml/index.html*).\n\nHowever, if you want to generate it again for some reason, you must run the command ``make html`` in the *docs* folder.",
    'author': 'Tom',
    'author_email': 'tom.thil@epita.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
