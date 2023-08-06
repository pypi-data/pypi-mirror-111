import numpy as np
from numpy.typing import ArrayLike


def add_two_vectors(
    a: ArrayLike,
    b: ArrayLike
) -> ArrayLike:
    """[summary]

    Args:
        a (ArrayLike): First vector
        b (ArrayLike): Second vector

    Returns:
        ArrayLike: Sum of the two inputs

    Examples
        >>> from how_to_opensource import add_two_vectors
        >>> add_two_vectors(np.ones(2), np.ones(2))
        array([2., 2.])
    """
    result: ArrayLike
    result = np.add(a, b)
    return result
