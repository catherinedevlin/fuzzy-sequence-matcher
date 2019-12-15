#!/usr/bin/env python

import pytest

"""Tests for `fuzzy_sequence_matcher` package."""


from fuzzy_sequence_matcher import fuzzy_sequence_matcher as fsm

# note: not a Pastafarian


def test_n_columns_to_remove():
    for threshold in (1_000, 10_000):
        for s in range(1, 20):
            for l in range(s + 1, 50):
                result = fsm._n_columns_to_remove(s, l, threshold=1_000)
                assert fsm.n_combinations(s, l - result) < threshold


def test_max_by_column():
    score_matrix = [
        [7, 1, 3, 9, 2],
        [5, 1, 4, 8, 1],
    ]
    expected = [7, 1, 4, 9, 2]
    assert fsm._max_by_column(score_matrix) == expected


def similarity(n1, n2):

    return -abs(n1 - n2)


def test_build_score_matrix():
    short_list = [7, 1, 4]
    long_list = [2, 6, 4, 9, 2, 9, 0, 0, 9, 5, 1, 3]

    result = fsm._build_score_matrix(short_list, long_list, similarity)
    assert len(result) == len(short_list)
    assert len(result[0]) == len(long_list)


def test_best_matches():
    short_list = [7, 1, 4]
    long_list = [2, 6, 4, 9, 2, 9, 0, 0, 9, 5, 1, 3]

    result = fsm.best_matches(short_list, long_list, similarity)
    assert result == [(7, 6), (1, 1), (4, 3)]


def test_best_matches_long_given_first():
    short_list = [7, 1, 4]
    long_list = [2, 6, 4, 9, 2, 9, 0, 0, 9, 5, 1, 3]

    result = fsm.best_matches(long_list, short_list, similarity)
    assert result == [(6, 7), (1, 1), (3, 4)]


def test_empty_list():
    short_list = []
    long_list = [2, 6, 4, 9, 2, 9, 0, 0, 9, 5, 1, 3]

    result = fsm.best_matches(short_list, long_list, similarity)
    assert result == []


def test_threshold_warning():
    short_list = [2, 0, 29]
    long_list = [
        14,
        17,
        64,
        68,
        13,
        95,
        87,
        34,
        24,
        29,
        62,
        96,
        29,
        94,
        71,
        92,
        81,
        9,
    ]

    result = fsm.best_matches(short_list, long_list, similarity)
    assert result == [(2, 14), (0, 13), (29, 29)]

    with pytest.warns(UserWarning):
        result = fsm.best_matches(short_list, long_list, similarity, threshold=100)
        assert result == [(2, 29), (0, 29), (29, 9)]
