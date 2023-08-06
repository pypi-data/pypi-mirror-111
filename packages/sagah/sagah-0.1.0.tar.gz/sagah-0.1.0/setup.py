# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sagah']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'sagah',
    'version': '0.1.0',
    'description': 'Orchestrated, async sagas in Python',
    'long_description': '# sagah\n\n[![](https://img.shields.io/pypi/v/sagah.svg)](https://pypi.org/pypi/sagah/) [![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)\n\nOrchestrated, async sagas in Python\n\nTable of Contents:\n\n- [Installation](#installation)\n- [Guide](#guide)\n- [Development](#development)\n\n## Installation\n\nsagah requires Python 3.6 or above.\n\n```bash\npip install sagah\n```\n\n## Guide\n\nExample usage:\n\n```python\nfrom sagah import Saga\n\nstate = {"counter": 0}\n\ndef incr():\n    state["counter"] += 1\n\ndef decr():\n    state["counter"] -= 1\n\nwith Saga() as saga:\n    await saga.action(incr, decr)\n    await saga.action(incr, decr)\n\nassert state["counter"] == 2\n```\n\nIf some action fails, the compensating functions from previous transactions will be called to restore the state:\n\n```python\nfrom sagah import Saga\n\nstate = {"counter": 0}\n\ndef incr():\n    state["counter"] += 1\n\ndef decr():\n    state["counter"] -= 1\n\ndef fail():\n    raise ValueError("oops")\n\ntry:\n    with Saga() as saga:\n        await saga.action(incr, decr)\n        await saga.action(incr, decr)\n        await saga.action(fail, noop)\nexcept Exception:\n    assert state["counter"] == 0\n```\n\n## Development\n\nTo develop sagah, install dependencies and enable the pre-commit hook:\n\n```bash\npip install pre-commit poetry\npoetry install\npre-commit install\n```\n\nTo run tests:\n\n```bash\npoetry run pytest\n```\n',
    'author': 'Jonathan Drake',
    'author_email': 'jdrake@narrativescience.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/NarrativeScience/sagah',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6.5,<4.0.0',
}


setup(**setup_kwargs)
