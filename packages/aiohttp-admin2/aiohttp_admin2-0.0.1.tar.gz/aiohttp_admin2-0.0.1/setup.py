# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiohttp_admin2',
 'aiohttp_admin2.controllers',
 'aiohttp_admin2.mappers',
 'aiohttp_admin2.mappers.fields',
 'aiohttp_admin2.mappers.validators',
 'aiohttp_admin2.resources',
 'aiohttp_admin2.resources.dict_resource',
 'aiohttp_admin2.resources.mongo_resource',
 'aiohttp_admin2.resources.mysql_resource',
 'aiohttp_admin2.resources.postgres_resource',
 'aiohttp_admin2.views',
 'aiohttp_admin2.views.aiohttp',
 'aiohttp_admin2.views.aiohttp.views']

package_data = \
{'': ['*'],
 'aiohttp_admin2.views.aiohttp': ['static/css/*',
                                  'static/js/*',
                                  'templates/aiohttp_admin/blocks/*',
                                  'templates/aiohttp_admin/blocks/filters/*',
                                  'templates/aiohttp_admin/blocks/form/*',
                                  'templates/aiohttp_admin/blocks/form/fields/*',
                                  'templates/aiohttp_admin/layouts/*']}

install_requires = \
['SQLAlchemy==1.3.24',
 'aiofiles>=0.7.0,<0.8.0',
 'aiohttp-jinja2>=1.4.2,<2.0.0',
 'aiohttp==3.6.3',
 'aiomysql>=0.0.21,<0.0.22',
 'aiopg>=1.3.0,<2.0.0',
 'motor>=2.4.0,<3.0.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'sqlalchemy-stubs>=0.4,<0.5',
 'umongo>=3.0.0,<4.0.0']

setup_kwargs = {
    'name': 'aiohttp-admin2',
    'version': '0.0.1',
    'description': 'Generator an admin interface based on aiohttp.',
    'long_description': '===============\nAiohttp admin 2\n===============\n\n`Demo site\n<https://shrouded-stream-28595.herokuapp.com/>`_ | `Demo source code\n<https://github.com/Arfey/aiohttp_admin2/tree/master/aiohttp_admin2/demo/>`_.\n\nThe aiohttp admin is library for generate admin interface for your data based\non aiohttp. This interface support multiple data storages and can combine them\ntogether.\n\n.. image:: https://img.shields.io/pypi/v/aiohttp_admin2.svg\n        :target: https://pypi.python.org/pypi/aiohttp_admin2\n\n.. image:: https://img.shields.io/travis/arfey/aiohttp_admin2.svg\n        :target: https://travis-ci.com/arfey/aiohttp_admin2\n\n.. image:: https://readthedocs.org/projects/aiohttp-admin2/badge/?version=latest\n        :target: https://aiohttp-admin2.readthedocs.io/en/latest/?badge=latest\n        :alt: Documentation Status\n\n\n.. image:: https://pyup.io/repos/github/arfey/aiohttp_admin2/shield.svg\n     :target: https://pyup.io/repos/github/arfey/aiohttp_admin2/\n     :alt: Updates\n\n* Free software: MIT license\n* Documentation: https://aiohttp-admin2.readthedocs.io.\n\n\n=======\nHistory\n=======\n\n0.1.0 (2020-04-28)\n------------------\n\n* First release on PyPI.\n',
    'author': 'Mykhailo Havelia',
    'author_email': 'misha.gavela@gmail.com',
    'maintainer': 'Mykhailo Havelia',
    'maintainer_email': 'misha.gavela@gmail.com',
    'url': 'https://github.com/arfey/aiohttp_admin2',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
