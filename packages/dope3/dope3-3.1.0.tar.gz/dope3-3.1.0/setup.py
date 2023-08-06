# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dope3']

package_data = \
{'': ['*']}

install_requires = \
['bchlib>=0.14.0,<0.15.0', 'dill>=0.3.3,<0.4.0', 'pycryptodome>=3.9,<4.0']

setup_kwargs = {
    'name': 'dope3',
    'version': '3.1.0',
    'description': 'Python3 Implementation of DOPE Encryption',
    'long_description': "# Double-Ratchet Over Parity Exchange(DOPE)\nPython3 Implementation of DOPE Encryption\n## Installation\n### From source\nTo install from source use the following command, make sure you have `setuptools>=50.0.0`\n```bash\npython3 seutp.py install\n```\n### From PyPI\n```bash\npip3 install dope3\n```\n## Using the DOPE API\nImport DOPE\n```python\nfrom dope3 import DOPE\n```\nOnce the dope package is imported you need to create the Dope class and initialize it with the required parameters\nThe parameters include:\n1. Your private Key\n2. Receiver's Public Key\n3. Session Key Size\n4. BCH Polynomial\n5. Error Correcting Code Size\n6. Racheting mode (`BLAKE0x0`/`BLAKEx0x`)\n7. AES Mode(`GCM`/`SIV`/`CBC`/`OFB`)\n8. HMAC(`SHA256`/`SHA384`/`SHA512`)\n9. Key Mode(`XOR-BL`/`AND-BL`)\n\n## Using the DOPE2 API\nImport DOPE2\n```python\nfrom dope3 import DOPE2\n```\nOnce the dope package is imported you need to create the Dope class and initialize it with the required parameters\nThe parameters include:\n1. Your Key\n2. BCH Polynomial\n3. Error Correcting Code Size\n4. AES Mode(`GCM`/`SIV`/`CBC`/`OFB`)\n5. Nonce\n6. Block Size",
    'author': 'Anubhav Mattoo',
    'author_email': 'anubhavmattoo@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
