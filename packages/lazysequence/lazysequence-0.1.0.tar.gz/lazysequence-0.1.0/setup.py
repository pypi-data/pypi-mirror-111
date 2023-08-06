# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['lazysequence']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'lazysequence',
    'version': '0.1.0',
    'description': 'lazysequence',
    'long_description': 'lazysequence\n============\n\n|PyPI| |Python Version| |License|\n\n|Read the Docs| |Tests| |Codecov|\n\n.. |PyPI| image:: https://img.shields.io/pypi/v/lazysequence.svg\n   :target: https://pypi.org/project/lazysequence/\n   :alt: PyPI\n.. |Python Version| image:: https://img.shields.io/pypi/pyversions/lazysequence\n   :target: https://pypi.org/project/lazysequence\n   :alt: Python Version\n.. |License| image:: https://img.shields.io/pypi/l/lazysequence\n   :target: https://opensource.org/licenses/MIT\n   :alt: License\n.. |Read the Docs| image:: https://img.shields.io/readthedocs/lazysequence/latest.svg?label=Read%20the%20Docs\n   :target: https://lazysequence.readthedocs.io/\n   :alt: Read the documentation at https://lazysequence.readthedocs.io/\n.. |Tests| image:: https://github.com/cjolowicz/lazysequence/workflows/Tests/badge.svg\n   :target: https://github.com/cjolowicz/lazysequence/actions?workflow=Tests\n   :alt: Tests\n.. |Codecov| image:: https://codecov.io/gh/cjolowicz/lazysequence/branch/main/graph/badge.svg\n   :target: https://codecov.io/gh/cjolowicz/lazysequence\n   :alt: Codecov\n\n\n**tl;dr** A lazy sequence makes an iterator look like a tuple.\n\n.. code:: python\n\n   from lazysequence import LazySequence\n\n   def load_records():\n       yield from [1, 2, 3, 4, 5, 6]  # pretend each iteration is expensive\n\n   records = LazySequence(load_records())\n   if not records:\n       raise SystemExit("no records found")\n\n   first, second = records[:2]\n\n   print("The first record is", first)\n   print("The second record is", second)\n\n   for record in records.release():  # do not cache all records in memory\n       print("record", record)\n\n\nSometimes you need to peek ahead at items returned by an iterator. How do you do that?\n\nIf the iterator does not need to be used later, just consume the items from the iterator. If later code needs to see all the items from the iterator, there are various options:\n\n1. You could pass the consumed items to the surrounding code separately. This can get messy, though.\n2. You could copy the items into a sequence beforehand. This is an option if the copy does not take a lot of space or time.\n3. You could duplicate the iterator using `itertools.tee`_, or write your own custom itertool. Consumed items are buffered internally. There are some good examples of this approach on SO, by `Alex Martelli`_, `Raymond Hettinger`_, and `Ned Batchelder`_.\n\n.. _itertools.tee: https://docs.python.org/3/library/itertools.html#itertools.tee\n.. _Alex Martelli: https://stackoverflow.com/a/1518097/1355754\n.. _Raymond Hettinger: https://stackoverflow.com/a/15726344/1355754\n.. _Ned Batchelder: https://stackoverflow.com/a/1517965/1355754\n\nA lazy sequence combines advantages from option 2 and option 3. It is constructed from an iterable, and implements `collections.abc.Sequence`_, providing the full set of immutable sequence operations on the iterable. Consumed items are cached internally, so the lookahead can happen transparently, and remains invisible to later code. Unlike a full copy (option 2), but like a duplicated iterator (option 3), items are only consumed and stored in memory as far as required for any given operation.\n\n.. _collections.abc.Sequence: https://docs.python.org/3/library/collections.abc.html#collections.abc.Sequence\n\n**Caveats:**\n\n- The lazy sequence will eventually store all items in memory. If this is a problem, use ``s.release()`` to obtain an iterator over the sequence items without further caching. After calling this function, the sequence should no longer be used.\n- Explicit is better than implicit. Clients may be better off being passed an iterator and dealing with its limitations. For example, clients may not expect ``len(s)`` to incur the cost of consuming the iterator to its end.\n\n\nInstallation\n------------\n\nYou can install *lazysequence* via pip_ from PyPI_:\n\n.. code:: console\n\n   $ pip install lazysequence\n\n\nContributing\n------------\n\nContributions are very welcome.\nTo learn more, see the `Contributor Guide`_.\n\n\nLicense\n-------\n\nDistributed under the terms of the `MIT license`_,\n*lazysequence* is free and open source software.\n\n\nIssues\n------\n\nIf you encounter any problems,\nplease `file an issue`_ along with a detailed description.\n\n\nCredits\n-------\n\nThis project was generated from `@cjolowicz`_\'s `Hypermodern Python Cookiecutter`_ template.\n\n.. _@cjolowicz: https://github.com/cjolowicz\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _MIT license: https://opensource.org/licenses/MIT\n.. _PyPI: https://pypi.org/\n.. _Hypermodern Python Cookiecutter: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n.. _file an issue: https://github.com/cjolowicz/lazysequence/issues\n.. _pip: https://pip.pypa.io/\n.. github-only\n.. _Contributor Guide: CONTRIBUTING.rst\n.. _Usage: https://lazysequence.readthedocs.io/en/latest/usage.html\n',
    'author': 'Claudio Jolowicz',
    'author_email': 'mail@claudiojolowicz.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/cjolowicz/lazysequence',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
