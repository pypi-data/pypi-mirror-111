# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['docs', 'src', 'src.pton']

package_data = \
{'': ['*'],
 'docs': ['_build/doctrees/*',
          '_build/doctrees/autoapi/*',
          '_build/doctrees/autoapi/area/*',
          '_build/doctrees/autoapi/buildings/*',
          '_build/doctrees/autoapi/city/*',
          '_build/doctrees/autoapi/district/*',
          '_build/doctrees/autoapi/street/*',
          '_build/doctrees/autoapi/test/*',
          '_build/doctrees/autoapi/tools/*',
          '_build/doctrees/autoapi/viewer/*',
          '_build/html/*',
          '_build/html/_sources/*',
          '_build/html/_sources/autoapi/*',
          '_build/html/_sources/autoapi/area/*',
          '_build/html/_sources/autoapi/buildings/*',
          '_build/html/_sources/autoapi/city/*',
          '_build/html/_sources/autoapi/district/*',
          '_build/html/_sources/autoapi/street/*',
          '_build/html/_sources/autoapi/test/*',
          '_build/html/_sources/autoapi/tools/*',
          '_build/html/_sources/autoapi/viewer/*',
          '_build/html/_static/*',
          '_build/html/autoapi/*',
          '_build/html/autoapi/area/*',
          '_build/html/autoapi/buildings/*',
          '_build/html/autoapi/city/*',
          '_build/html/autoapi/district/*',
          '_build/html/autoapi/street/*',
          '_build/html/autoapi/test/*',
          '_build/html/autoapi/tools/*',
          '_build/html/autoapi/viewer/*']}

modules = \
['README']
install_requires = \
['Fiona>=1.8.20,<2.0.0',
 'Shapely>=1.7.1,<2.0.0',
 'geopandas>=0.9.0,<0.10.0',
 'matplotlib>=3.4.2,<4.0.0',
 'numpy>=1.21.0,<2.0.0',
 'scipy>=1.7.0,<2.0.0',
 'voronoi>=0.2.0,<0.3.0']

setup_kwargs = {
    'name': 'pton',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Emma Rachlin',
    'author_email': 'emma.rachlin@epita.fr',
    'maintainer': 'Maxence Ramos-Pariente',
    'maintainer_email': 'maxence.ramos-pariente@epita.fr',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
