# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yatracker', 'yatracker.types', 'yatracker.utils']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7,<4.0', 'certifi>=2021,<2022', 'pydantic>=1.8,<2.0']

setup_kwargs = {
    'name': 'yatracker',
    'version': '2021.7.2',
    'description': 'Async client for Yandex Tracker API',
    'long_description': "# YaTracker\nAsyncio Yandex Tracker API client\n\nAPI docs: https://tech.yandex.com/connect/tracker/api/about-docpage/\n\n## Attention!\n* All `self` properties renamed to `url` cause it's incompatible with Python.\n* All `camelCase` properties renamed to `pythonic_case`.\n* Methods named by author, cause Yandex API has no clear method names.\n\n\n## How to install\n```text\npython3.7 -m pip install yatracker\n```\n\n\n## How to use\n```python\nfrom yatracker import YaTracker\n\ntracker = YaTracker(org_id=..., token=...)\n\nasync def foo():\n    # create issue\n    issue = await tracker.create_issue('New Issue', 'KEY')\n    \n    # get issue\n    issue = await tracker.get_issue('KEY-1')\n    \n    # update issue (just pass kwargs)\n    issue = await tracker.edit_issue('KEY-1', description='Hello World')\n\n    # get transitions:\n    transitions = await issue.get_transitions()\n\n    # execute transition\n    transition = transitions[0]\n    await transition.execute()\n\n```\n```python\n# don't forget to close tracker on app shutdown\nasync def on_shutdown():\n    await tracker.close()\n\n```\n",
    'author': 'Oleg A.',
    'author_email': 'oleg@trueweb.app',
    'maintainer': 'Oleg A.',
    'maintainer_email': 'oleg@trueweb.app',
    'url': 'https://github.com/Olegt0rr/YaTracker/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
