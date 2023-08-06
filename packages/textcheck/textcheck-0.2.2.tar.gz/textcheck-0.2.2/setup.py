# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['textcheck', 'textcheck.lib']

package_data = \
{'': ['*']}

install_requires = \
['rich',
 'spacy==2.3.7',
 'spacy_hunspell>=0.1.0,<0.2.0',
 'stackprinter',
 'typer']

entry_points = \
{'console_scripts': ['textcheck = textcheck.main:app']}

setup_kwargs = {
    'name': 'textcheck',
    'version': '0.2.2',
    'description': 'Check text files for issues.',
    'long_description': '# textcheck\n\nRun text checks on files from the command line.\n\n```\n┏━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓\n┃ Word    ┃ Alternatives                                    ┃ Context                       ┃\n┡━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩\n│ speling │ spieling, spelling, spewing, peeling, splinting │ should be checked for speling │\n└─────────┴─────────────────────────────────────────────────┴───────────────────────────────┘\n```\n## Installation\n\n```\npip install --user textcheck\n```\n\nHunspell dictionary files `en_US.dic` and `en_US.aff` need to be placed in `/usr/share/hunspell` directory.\n\n## Limitations\n\n* Only console output for now.\n* Only English language is supported.\n* Only Linux-based systems are supported.\n\n## CLI usage\n\n### `spellcheck`\n\nExample invocation:\n\n```\ntextcheck spellcheck ~/spellme.txt --ignore-list=/home/user/ignore_list.txt\n```\n\nRun spellcheck for a set of files. \n\nProvided ignore list is a file with ignore words on new lines.\n\n**Usage**:\n\n```console\n$ textcheck spellcheck [OPTIONS] FILES...\n```\n\n**Arguments**:\n\n* `FILES...`: The list of files to check\n\n**Options**\n\n* `ignore_list`: Path to the ignore list file.',
    'author': 'Petr Stribny',
    'author_email': 'petr@stribny.name',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/stribny/textcheck',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
