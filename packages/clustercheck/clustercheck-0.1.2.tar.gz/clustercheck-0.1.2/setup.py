# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['clustercheck']
install_requires = \
['pyyaml>=5.4.1,<6.0.0',
 'requests>=2.25.1,<3.0.0',
 'websocket-client>=1.1.0,<2.0.0']

entry_points = \
{'console_scripts': ['clustercheck = clustercheck:main']}

setup_kwargs = {
    'name': 'clustercheck',
    'version': '0.1.2',
    'description': 'check a cluster of services',
    'long_description': '# clustercheck\n\nCheck a cluster before it goes live.\n\n## Usage:\n\n```\nclustercheck -c my.config\n```\n\n\nExample of config:\n\n```\ndns_map:\n    www.blah.com: kube.aws.longthing.com\n    www.bar.com: 12.34.56.7\n\nplugin:\n    - lib: myplugin.py\n      name: MyCheck\n\nchecks:\n    - url: "wss://dev-site.example.io"\n      plugin: MyCheck\n    - url: "wss://prod-site.example.io"\n      plugin: MyCheck\n    - url: "https://prod-site.example.io"\n      expect: \n        contains: some-string\n      args:\n        verify: False\n```\n\nThis will run 3 checks, 2 of them will re-use the same plugin (MyCheck), and the 3rd, will just hit the url with requests() lib.\n\n\nExample of plugin:\n\n```\nclass MyCheck(clustercheck.Plugin):\n    def check(self, url, args):\n        return True\n\n```\n\nArgs are "anything in the args yml".   They are not checked, so plugins must verify these values.\n\n\n# Check Execution\n    - dns map is applied first, it monkey-patches the socket library\n    - dns map is not inherited by subprocesses, it is python in-process only\n    - each check is executed in order\n    - if a plugin is not specified, the url must be valid\n    - plugsin can be named as "module.name" or as "/path/to/file.py"\n     \n\n# Generic checks\n    - urls are checked for status 200, unless expect: status: is changes.\n    - websockets are only checked for a ping\n    - args, if any, are passed to the `requests.request()` or `websocket.create_connection()` calls directly\n    - default "method" for requests is "GET"\n\n# Output format\n    - output is recorded internally as (PASS/FAIL, time, message, check_config)\n    - default output format is: "{ok} [{time}] {message} {config.url}"\n    - passing results are not output unless --verbose is set\n',
    'author': 'erik aronesty',
    'author_email': 'erik@q32.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/AtakamaLLC/clustercheck',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
