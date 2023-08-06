# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['rtmilk']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.8.1', 'requests>=2.23.0']

setup_kwargs = {
    'name': 'rtmilk',
    'version': '0.0.2',
    'description': 'RTM API wrapper',
    'long_description': '# rtmilk\nPython wrapper for "Remember the Milk" [API](https://www.rememberthemilk.com/services/api/)\n\n# Idea\nIdea is to use pydantic to (de)structure the requests and responses\nThere is a raw api wrapper called API which handles authorization, wrapping each call in a function and removing common fields\nThere will be a higher level wrapper which will have objects representing the implicit objects in the API e.g. Task, TaskSeries, List\n\n# Authorization layer\nStores the key, secret etc\nGenerates the api sig\nMakes generic authorized/unauthorized calls. Inputs are able to be coerced to strings. Outputs are dictionaries that come out of the json parsing\n\n# Wrappers for the specific RTM calls\nInputs are proper types like datetime, enums, lists\nOutputs are parsed out into the same types (datetime, enums, lists etc)\nShould it throw RTM errors rather than return parsed fail objects? Probably, since it\'s possible with complete fidelity and fits with the way the code has to be written\n\n# Task objects\nOrdering of start/due dates\nHide whether they\'re dates or datetimes\nHiding of "no tag"/tag type inconsistency\nCoalesce sending of different attributes to the server with an explicit call - have to do that for start/due dates anyway\nValidate the repeat input values\n\n# List objects\nSometimes you only get the listid back, could hide the expansion of the other attributes\n\n# Filter objects\nConstruct from string\nConstruct from logical combination of conditions\nOutput strings to the server using the pydantic stuff\n\n# Client layer\nFirst entry point\nSearch for tasks\nCRUD for lists\nHolds the API object\n\n# Future?\nMake it sansio, so that we can use other than requests\n',
    'author': 'Rehan Khwaja',
    'author_email': 'rehan@khwaja.name',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rkhwaja/rtmilk',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
