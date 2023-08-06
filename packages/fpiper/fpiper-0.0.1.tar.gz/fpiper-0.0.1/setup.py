# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['fpiper']
setup_kwargs = {
    'name': 'fpiper',
    'version': '0.0.1',
    'description': 'A small library providing functional wrappers over Optional and Iterable',
    'long_description': 'When coming from a functional background, it is normal to miss common\n_chainable_ combinators for container types, namely:\n\n- `map`|`fmap`\n- `filter`|`where`\n- `flatMap`|`bind`|`collect`\n\nThis library contains simple wrappers for `Optional` and `Iterable` Python\nvalues which provide just that.\n\nThe library is currently in very experimental stage, use at your own risk.\n\nAn example:\n\n```\n  from fpiper import pipe, pipeOpt\n\n  x = pipe(myList).filter(lambda x: x > 0).flatMap(lambda x: x*2).run()\n  y = pipeOpt(loadCustomer).flatMap(validateCustomer).map(submitCustomer).run()\n```\n\n',
    'author': 'Vladimir Okhotnikov',
    'author_email': 'vokhotnikov@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
