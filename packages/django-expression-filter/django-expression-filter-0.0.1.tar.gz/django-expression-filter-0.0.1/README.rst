About
=====

(WIP)

This package provides a class that enables direct filtering on an expression that you'd usually use as an annotation.

Usage
=====

The class ``AnnotationBypass`` takes 3 arguments. The first is any valid annotation value, the second is the lookup string you'd use in the filter kwarg name, the third is the value you'd use for the filter.

.. code-block:: python

    from expression_filter import AnnotationBypass

    filter = AnnotationBypass(Sum('book__page_count'), 'gte', 1000)

But why
=======

Consider the following:

.. code-block:: python

    Book.objects.annotate(words_per_page=F('word_count') / F('page_count')).filter(words_per_page__gte=100)

This executes the following query:

.. code-block:: sql

    SELECT `books_book`.`id`,
           `books_book`.`word_count`,
           `books_book`.`page_count`,
           `books_book`.`word_count` / `books_book`.`page_count` AS `words_per_page`
    FROM `books_book`
    WHERE `books_book`.`word_count` / `books_book`.`page_count` >= 100

Notice that the expression is duplicated, as using the ``words_per_page`` annotation by name in the ``WHERE`` clause is not allowed. Usually the annotated value is not needed in the response, and depending on how complex the annotation is or how many objects are returned, this could have a performance impact.

This is better:

.. code-block:: python

    from expression_filter import AnnotationBypass

    Book.objects.filter(AnnotationBypass(F('word_count') / F('page_count'), 'gte', 100))

.. code-block:: sql

    SELECT `books_book`.`id`,
           `books_book`.`word_count`,
           `books_book`.`page_count`
    FROM `books_book`
    WHERE `books_book`.`word_count` / `books_book`.`page_count` >= 100
