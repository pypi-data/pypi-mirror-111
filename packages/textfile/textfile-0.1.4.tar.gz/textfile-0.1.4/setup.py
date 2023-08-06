# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['textfile']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'textfile',
    'version': '0.1.4',
    'description': 'Functions that enables us to write out or read from with text file in shorter syntax.',
    'long_description': '\nWrapper functions of codes of text file operation that are very commonly seen.\nBy using ``textfile``, readability of our program will be improve!\n\nInstall\n-------\n\n.. code-block:: Shell\n\n    > pip install textfile\n\n\nVery basic usage\n----------------\n\nCreate file and write text to it.\n\n.. code-block:: python\n\n    >>> import textfile\n    >>> textfile.write("a.txt", "any string value")\n\nRead text from text file.\n\n.. code-block:: python\n\n    >>> import textfile\n    >>> textfile.read("a.txt")\n    "any string value"\n\nUse cases\n---------\n\nWrite string to text file:\n\n.. code-block:: python\n\n    textfile.write("somefile.txt", "any string value")\n\nRead entire string from text file:\n\n.. code-block::\n\n    textfile.read("somefile.txt")\n\nReplace string in text file:\n\n.. code-block::\n\n    textfile.replace("somefile.txt", "replaced", "replacement")\n\nAppend string to text file:\n\n.. code-block::\n\n    textfile.append("somefile.txt", "text to append")\n\nInsert string to text file:\n\n.. code-block::\n\n    textfile.insert("somefile.txt", "text to insert", line=10)\n\n\nJust a implementation of facade pattern\n---------------------------------------\n\n``textfile`` wraps python algorithms that are very commonly used\nin the purpose of to more simplify basic operations.\n\nThis is just a facade pattern.\n\nThe side effect of simplify the interface of text file operation, gets less flexibility.\nFurther more, it becomes hard to do speed tuning.\n\nBut I think that those are not a matter in almost all situations of our programming.\n\nWe should pay more attention to code readability!\n\nI courage you to use ``textfile`` as much as possible you can.\nIf you do so, the readability of your code will increase, and will suppress many bugs.\n\n\nIs this document written in strange English?\n--------------------------------------------\nKenjimaru, the author of this document, I am Japanese and am not familiar to English.\n\nIf you read this document, and find anything should be fixed, feel free to contact me,\nand I will appreciate.\n\n',
    'author': 'kenjimaru',
    'author_email': 'kendimaru2@gmail.com',
    'maintainer': 'kenjimaru',
    'maintainer_email': 'kendimaru2@gmail.com',
    'url': 'https://jimaru.site/textfile/',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
