# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aioskynet']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp[speedups]>=3.7.4,<4.0.0']

setup_kwargs = {
    'name': 'aioskynet',
    'version': '1.0.0',
    'description': 'An async wrapper of the Sia Skynet API.',
    'long_description': '# aioskynet\n\nAn async wrapper of the Sia Skynet API.\n\n## Basic usage\n\n### Uploading a file\n\n```py\nfrom asyncio import run\n\nfrom aioskynet import SkynetClient, File\n\n\nclient = SkynetClient()\n\n\nasync def main():\n    file = File("test.py", open("test.py"))\n    data = await client.upload_file(file)\n\n    print(data)  # Instance of aioskynet.SkynetResponse\n\n    # Close the client when finished.\n    await client.close()\n\nrun(main())\n```\n',
    'author': 'vcokltfre',
    'author_email': 'vcokltfre@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
