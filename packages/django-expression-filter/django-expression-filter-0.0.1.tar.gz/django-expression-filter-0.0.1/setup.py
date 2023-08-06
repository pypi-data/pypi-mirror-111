# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['expression_filter']

package_data = \
{'': ['*']}

install_requires = \
['Django>=2.2,<4']

setup_kwargs = {
    'name': 'django-expression-filter',
    'version': '0.0.1',
    'description': 'A class for Django filters to allow direct filtering on expressions, as you would normally do with annotations, so the annotation does not need to happen.',
    'long_description': "About\n=====\n\n(WIP)\n\nThis package provides a class that enables direct filtering on an expression that you'd usually use as an annotation.\n\nUsage\n=====\n\nThe class ``AnnotationBypass`` takes 3 arguments. The first is any valid annotation value, the second is the lookup string you'd use in the filter kwarg name, the third is the value you'd use for the filter.\n\n.. code-block:: python\n\n    from expression_filter import AnnotationBypass\n\n    filter = AnnotationBypass(Sum('book__page_count'), 'gte', 1000)\n\nBut why\n=======\n\nConsider the following:\n\n.. code-block:: python\n\n    Book.objects.annotate(words_per_page=F('word_count') / F('page_count')).filter(words_per_page__gte=100)\n\nThis executes the following query:\n\n.. code-block:: sql\n\n    SELECT `books_book`.`id`,\n           `books_book`.`word_count`,\n           `books_book`.`page_count`,\n           `books_book`.`word_count` / `books_book`.`page_count` AS `words_per_page`\n    FROM `books_book`\n    WHERE `books_book`.`word_count` / `books_book`.`page_count` >= 100\n\nNotice that the expression is duplicated, as using the ``words_per_page`` annotation by name in the ``WHERE`` clause is not allowed. Usually the annotated value is not needed in the response, and depending on how complex the annotation is or how many objects are returned, this could have a performance impact.\n\nThis is better:\n\n.. code-block:: python\n\n    from expression_filter import AnnotationBypass\n\n    Book.objects.filter(AnnotationBypass(F('word_count') / F('page_count'), 'gte', 100))\n\n.. code-block:: sql\n\n    SELECT `books_book`.`id`,\n           `books_book`.`word_count`,\n           `books_book`.`page_count`\n    FROM `books_book`\n    WHERE `books_book`.`word_count` / `books_book`.`page_count` >= 100\n",
    'author': 'Hameed Gifford',
    'author_email': 'giff.h92@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hamstap85/django-expression-filter/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4',
}


setup(**setup_kwargs)
