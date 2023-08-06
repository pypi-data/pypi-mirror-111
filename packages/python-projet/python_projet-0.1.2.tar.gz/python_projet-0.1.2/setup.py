# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['docs', 'docs.source', 'src', 'src.python_projet', 'tests']

package_data = \
{'': ['*'],
 'docs': ['build/doctrees/*',
          'build/doctrees/autoapi/*',
          'build/doctrees/autoapi/area/*',
          'build/doctrees/autoapi/city/*',
          'build/doctrees/autoapi/generate_points/*',
          'build/doctrees/autoapi/main/*',
          'build/doctrees/autoapi/python_projet/*',
          'build/doctrees/autoapi/tools/*',
          'build/doctrees/autoapi/viewer/*',
          'build/html/*',
          'build/html/_sources/*',
          'build/html/_sources/autoapi/*',
          'build/html/_sources/autoapi/area/*',
          'build/html/_sources/autoapi/city/*',
          'build/html/_sources/autoapi/generate_points/*',
          'build/html/_sources/autoapi/main/*',
          'build/html/_sources/autoapi/python_projet/*',
          'build/html/_sources/autoapi/tools/*',
          'build/html/_sources/autoapi/viewer/*',
          'build/html/_static/*',
          'build/html/autoapi/*',
          'build/html/autoapi/area/*',
          'build/html/autoapi/city/*',
          'build/html/autoapi/generate_points/*',
          'build/html/autoapi/main/*',
          'build/html/autoapi/python_projet/*',
          'build/html/autoapi/tools/*',
          'build/html/autoapi/viewer/*']}

modules = \
['requirements', 'README', 'AUTHORS']
install_requires = \
['Fiona>=1.8.20,<2.0.0',
 'Geometry>=0.0.23,<0.0.24',
 'Shapely>=1.7.1,<2.0.0',
 'geopandas>=0.9.0,<0.10.0',
 'matplotlib>=3.4.2,<4.0.0',
 'numpy>=1.21.0,<2.0.0',
 'scipy>=1.7.0,<2.0.0',
 'voronoi>=0.2.0,<0.3.0']

setup_kwargs = {
    'name': 'python-projet',
    'version': '0.1.2',
    'description': 'Projet de generation de ville',
    'long_description': None,
    'author': 'Samy Belbachir',
    'author_email': 'samy.belbachir@epita.fr',
    'maintainer': 'Maridiyath Bachirou ',
    'maintainer_email': 'maridiyath-folake-odeofe.bachirou@epita.fr',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.10',
}


setup(**setup_kwargs)
