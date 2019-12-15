import typing as tp
from itertools import combinations
from math import factorial
from warnings import warn

THRESHOLD = 1_000_000

Matrix = tp.NewType("Matrix", tp.List[tp.List[float]])


def n_combinations(short_n: int, long_n: int) -> int:
    """Number of potential combinations between two sequences of given lengths 

    Formula is taken from Python `itertools.combinations` docs:

        The number of items returned is n! / r! / (n-r)! 
        when 0 <= r <= n or zero when r > n.

    Arguments:
        short_n {int} -- length of the shorter sequence 
        long_n {int} -- length of the longer sequence
    
    Returns:
        int -- [description]
    """
    assert short_n <= long_n, "First sequence given must be the shorter one"
    return factorial(long_n) / factorial(short_n) / factorial(long_n - short_n)


def _n_columns_to_remove(
    short_len: int, long_len: int, threshold: int = THRESHOLD
) -> int:
    """Number of columns to remove to get n_combinations under threshold

    Given matrix with short_len rows and long_len columns.
    
    Arguments:
        short_len {int} -- Number of rows in matrix 
        long_len {int} -- Number of columns in matrix 
    
    Keyword Arguments:
        threshold {int} -- Max # of combinations to tolerate (default: {THRESHOLD})
    
    Returns:
        int -- Number of columns to remove from matrix to get 
            number of combinations below threshold.
    """
    final_len = long_len
    while n_combinations(short_len, final_len) > threshold:
        final_len -= 1
    return long_len - final_len


def _max_by_column(score_matrix: Matrix) -> tp.List[float]:
    result: tp.List[float] = []
    for long_idx in range(len(score_matrix[0])):
        score = 0
        for row in score_matrix:
            score = max(score, row[long_idx])
        result.append(score)
    return result


def _indexes_of_smallest_n_scores(scores: tp.List[float], n: int) -> tp.List[int]:
    ranked: tp.List[tp.Tuple[float, int]] = [
        (score, i) for (i, score) in enumerate(scores)
    ]
    ranked.sort()
    return [t[1] for t in ranked[:n]]


def pruned(
    long_seq: tp.List,
    score_matrix: Matrix,
    threshold: int = THRESHOLD,
    give_warnings: bool = True,
) -> tp.Tuple[tp.List, Matrix]:

    n_removals = _n_columns_to_remove(
        len(score_matrix), len(score_matrix[0]), threshold=threshold
    )
    if n_removals:
        if give_warnings:
            warn(
                "More potential combinations than {threshold} threshold. "
                "Approximating by dropping least likely {n_removals} "
                "elements from longer sequence."
            )
        else:
            return (long_seq, score_matrix)
    column_scores = _max_by_column(score_matrix)
    indexes_to_remove = _indexes_of_smallest_n_scores(column_scores, n_removals)
    new_long_seq = [
        e for (idx, e) in enumerate(long_seq) if idx not in indexes_to_remove
    ]
    new_score_matrix = [
        [r for (idx, r) in enumerate(row) if idx not in indexes_to_remove]
        for row in score_matrix
    ]
    return (new_long_seq, new_score_matrix)


def _build_score_matrix(
    short_seq: tp.List, long_seq: tp.List, scorer: tp.Callable[[tp.Any, tp.Any], float]
) -> Matrix:

    assert len(short_seq) <= len(
        long_seq
    ), "First sequence given must be the shorter one"

    score_matrix = [
        [scorer(short_val, long_val) for long_val in long_seq]
        for (short_idx, short_val) in enumerate(short_seq)
    ]
    return score_matrix


def _best_matches_short_first(
    short_seq: tp.List,
    long_seq: tp.List,
    scorer: tp.Callable[[tp.Any, tp.Any], float],
    threshold: int = THRESHOLD,
    give_warnings: bool = True,
):

    # The number of items returned is n! / r! / (n-r)! when 0 <= r <= n or zero when r > n.

    assert len(short_seq) <= len(
        long_seq
    ), "First sequence given must be the shorter one"

    if not short_seq:
        return []

    score_matrix = _build_score_matrix(short_seq, long_seq, scorer)

    (long_seq, score_matrix) = pruned(
        long_seq, score_matrix, threshold=threshold, give_warnings=give_warnings
    )

    def score_seq(seq):
        return sum(
            [
                score_matrix[short_idx][long_idx]
                for (short_idx, long_idx) in enumerate(seq)
            ]
        )

    best_score = float("-inf")
    best_seq = None
    pairing_index_sequences = combinations(range(len(long_seq)), len(short_seq))
    for seq in pairing_index_sequences:
        score = score_seq(seq)
        if score > best_score:
            best_score = score
            best_seq = seq

    if best_seq:
        return [
            (short_seq[short_idx], long_seq[long_idx])
            for (short_idx, long_idx) in enumerate(best_seq)
        ]


def best_matches(
    seq1: tp.List[tp.Any],
    seq2: tp.List[tp.Any],
    scorer: tp.Callable[[tp.Any, tp.Any], float],
    threshold: int = THRESHOLD,
    give_warnings: bool = True,
):

    if len(seq2) > len(seq1):
        return _best_matches_short_first(
            seq1, seq2, scorer=scorer, threshold=threshold, give_warnings=give_warnings,
        )
    result = _best_matches_short_first(
        seq2, seq1, scorer=scorer, threshold=threshold, give_warnings=give_warnings
    )
    return [(tup[1], tup[0]) for tup in result]
