# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['proselint',
 'proselint.checks',
 'proselint.checks.airlinese',
 'proselint.checks.annotations',
 'proselint.checks.archaism',
 'proselint.checks.cliches',
 'proselint.checks.consistency',
 'proselint.checks.corporate_speak',
 'proselint.checks.cursing',
 'proselint.checks.dates_times',
 'proselint.checks.hedging',
 'proselint.checks.hyperbole',
 'proselint.checks.inprogress',
 'proselint.checks.jargon',
 'proselint.checks.lexical_illusions',
 'proselint.checks.lgbtq',
 'proselint.checks.links',
 'proselint.checks.malapropisms',
 'proselint.checks.misc',
 'proselint.checks.mixed_metaphors',
 'proselint.checks.mondegreens',
 'proselint.checks.needless_variants',
 'proselint.checks.nonwords',
 'proselint.checks.oxymorons',
 'proselint.checks.psychology',
 'proselint.checks.redundancy',
 'proselint.checks.security',
 'proselint.checks.sexism',
 'proselint.checks.skunked_terms',
 'proselint.checks.spelling',
 'proselint.checks.terms',
 'proselint.checks.typography',
 'proselint.checks.uncomparables',
 'proselint.checks.weasel_words']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.0,<9.0.0', 'future>=0.18.2,<0.19.0', 'six>=1.15.0,<2.0.0']

setup_kwargs = {
    'name': 'proselint',
    'version': '0.11.0',
    'description': 'A linter for prose.',
    'long_description': None,
    'author': 'Amperser Labs',
    'author_email': 'hello@amperser.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
