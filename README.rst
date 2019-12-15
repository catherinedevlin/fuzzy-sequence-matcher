======================
Fuzzy Sequence Matcher
======================


.. image:: https://img.shields.io/pypi/v/fuzzy_sequence_matcher.svg
        :target: https://pypi.python.org/pypi/fuzzy_sequence_matcher

.. image:: https://img.shields.io/travis/catherinedevlin/fuzzy_sequence_matcher.svg
        :target: https://travis-ci.org/catherinedevlin/fuzzy_sequence_matcher

.. image:: https://readthedocs.org/projects/fuzzy-sequence-matcher/badge/?version=latest
        :target: https://fuzzy-sequence-matcher.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


Purpose
-------

Finds best pairings of elements between two sequences.

Each element can only be used at most once, and the order 
of elements is preserved.  That is, 
if X1 -> Y2, then X2 cannot match to Y1 or Y2; it must
match to Y3 or later.  This is appropriate for sequences 
where Y is a garbled or mutated copy of X. 

Example
-------

::

    >>> from fuzzy_sequence_matcher.fuzzy_sequence_matcher import best_matches
    >>> from jellyfish import jaro_distance
    >>> declaration = "We hold these truths to be self evident".split()
    >>> degradation = ("I guess wee hold them tooths and stuff "
    ...     "for being sort of evidence, y'know?").split()
    >>> best_matches(declaration, degradation, scorer=jaro_distance)
    [('We', 'wee'), ('hold', 'hold'), ('these', 'them'), ('truths', 'tooths'), ('to', 'for'), ('be', 'being'), ('self', 'sort'), ('evident', 'evidence,')]

Features
--------

* Match any objects you can write a scoring function for 
* No dependencies outside standard library

Scoring function
================

The matching is done with a scoring function you specify.
It should look something like::

    def score(element_from_seq1: Any, element_from_seq2: Any) -> float 

with high scores indicating better matches.

For comparing strings, you might use jellyfish_.jaro_distance.
For comparing numbers, ``-abs(n1 - n2)`` works.

threshold
==========

By default, fuzzy_sequence_matcher finds the combination that
maximizes the sum scores of all the pairings.  However, when one 
sequence is much longer than the other, the number of possible 
combinations grows impractically large to try them all.  The 
[itertools documenation](https://docs.python.org/3/library/itertools.html#itertools.combinations)
gives the number of combinations as 

    len(Y)! / len(X)! / (len(Y) - len(X))! 

when len(Y) >= len(X).

This function is exposed as fuzzy_sequence_matcher.n_combinations.

If the number of possible combinations exceeds a threshold - by 
default, 1_000_000, which happens when the long seq is ~ 15 or more 
elements longer than the short - then elements from the longer sequence 
will be dropped from consideration entirely, starting with those whose 
best match to the shorter sequence is worst, until n_combinations 
is under the threshold.  This could conceivably give a result that 
is not the ideal-scoring set of matches.


* Free software: MIT license
* Documentation: https://fuzzy-sequence-matcher.readthedocs.io.


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

Thanks to `Dayton Dynamic Languages`_ for advice and brainstorming

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _`Dayton Dynamic Languages`: http://d8ndl.org/
.. _jellyfish: https://github.com/jamesturk/jellyfish
