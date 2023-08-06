# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['itranslate']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.18.2,<0.19.0', 'joblib>=1.0.1,<2.0.0', 'logzero>=1.7.0,<2.0.0']

setup_kwargs = {
    'name': 'itranslate',
    'version': '0.1.0',
    'description': 'Google translate free and unlimited, itranslate since gtranslate is taken',
    'long_description': '# itranslate\n[![tests](https://github.com/ffreemt/google-itranslate/actions/workflows/routine-tests.yml/badge.svg)][![python](https://img.shields.io/static/v1?label=python+&message=3.7%2B&color=blue)](https://img.shields.io/static/v1?label=python+&message=3.7%2B&color=blue)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)[![PyPI version](https://badge.fury.io/py/itranslate.svg)](https://badge.fury.io/py/itranslate)\n\nGoogle translate free and unlimited access, `itranslate` because gtranslate is taken\n\n## Install it\n\n```shell\npip install itranslate\n\n# or pip install git+https://github.com/ffreemt/google-itranslate\n# or use poetry\n# poetry add itranslate\n# poetry add git+https://github.com/ffreemt/google-itranslate\n\n```\n\n## Use it\n\nThe quality from this service is not as good as web google translate. There is nothing we can do about it.\n\nIt\'s unclear whether your ip will be blocked if you relentlessly use the service. Please feedback should you find out any information.\n\n```python\nfrom itranslate import itranslate as itrans\n\nitrans("test this and that")  # \'测试这一点\'\n\n# new lines are preserved\nitrans("test this \\n\\nand that")  # \'测试这一点\\n\\n然后\'\n\nitrans("test this and that", to_lang="de")  # \'Testen Sie das und das\'\nitrans("test this and that", to_lang="ja")  # \'これとそれをテストします\'\n```\n\n### Not ready yet: `async version`: `atranslate`\nIf you feel so inclined, you may use the async version of itranslate: atranslate:\n```python\nimport asyncio\nfrom itranslate import atranslate as atrans\n\ntexts = ["test this", test that"]\ncoros = [atrans(elm) for elm in tests]\n\nloop = asyncio.get_event_loop()\n\ntrtexts = loop.run_until_complete(asycnio.gather(*coros))\n\nprint(trtexts)\n#\n```\n\n### Proxies support\n```\nitrans("test this and that", proxies="http://localhost:8030")\n```\nor\n```python\nproxies = {\n    "http://": "http://localhost:8030",\n    "https://": "http://localhost:8031",\n}\nitrans("test this and that\\n another test", proxies=proxies)\n```\n\nCheck [https://www.python-httpx.org/advanced/](https://www.python-httpx.org/advanced/) for other ways of setting up proxies.\n\n## Disclaimer\n``itranslate`` is for study and research purpose only. The interface used by ``itranslate`` may become invalid without notice and render ``itranslate`` completely useless.\n',
    'author': 'ffreemt',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ffreemt/google-itranslate',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
