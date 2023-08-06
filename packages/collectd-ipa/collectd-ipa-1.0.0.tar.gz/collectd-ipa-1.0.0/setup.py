# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['collectd_ipa']

package_data = \
{'': ['*']}

install_requires = \
['python-ldap>=3.3.1,<4.0.0']

setup_kwargs = {
    'name': 'collectd-ipa',
    'version': '1.0.0',
    'description': 'A CollectD plugin to get metrics from IPA',
    'long_description': "# Collectd plugin for IPA\n\nA Collectd plugin to extract metrics from IPA\n\nCurrently supported metrics:\n\n- `groups`: the number of groups\n- `users`: the number of users, active or disabled\n- `users_rate`: the rate at which the number of users is changing (registered\n  users and deletions)\n- `staged_users`: the number of staged users (users in the process of\n  registering for an account), split by their spam detection status.\n\n\n## Installation\n\nOn the IPA host:\n\n- install the python module where Collectd's python plugin can see it\n- run `make install`\n\nOn the host where the collectd server is running:\n\n- run `make install-data`\n- append the content of `collection.conf` to your `/etc/collection.conf`\n\n\n## Configuration\n\nThe `collectd.d/ipa.conf` file has an example of the available configuration\nvalues that you can adjust, in the `Module collectd_ipa` block.\n\nIt contains descriptions of what the configuration variables mean and their\ndefault values.\n\n\n## License\n\nLicensed under [lgpl-3.0](./LICENSE)\n",
    'author': 'Fedora Infrastructure',
    'author_email': 'infrastructure@lists.fedoraproject.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fedora-infra/collectd-ipa',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
