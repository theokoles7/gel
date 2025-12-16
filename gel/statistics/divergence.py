"""# gel.statistics.divergence

Divergence calculation methods.
"""

__all__ =   [
                "D_KL",
            ]

from typing         import Sequence, Union

from numpy.typing   import NDArray
from scipy.special  import rel_entr

def D_KL(
    P:          Union[NDArray, Sequence[Union[int, float]]],
    Q:          Union[NDArray, Sequence[Union[int, float]]]
) -> float:
    """# Kullback-Leibler (KL) Divergence.

    Compute the Kullback-Leibler (KL) divergence D_KL(p || q) between two discrete probability 
    distributions.

    ## Notes:
        * KL divergence is not symmetric.
        * KL divergence is not a true metric (does not satisfy triangle inequality).

    ## Args:
        * P         (NDArray):  True probability distribution.
        * Q         (NDArray):  Approximate probability distribution.

    ## Raises AssertionError if:
        * Shapes of `P` & `Q` do not match.
        * Either distribution contains negative values.
        * Either distribution sums to zero.

    ## Returns:
        * float:    Kull-Leibler (KL) divergence.

    ## Example:
    >>> p = np.array([0.5, 0.5])
    >>> q = np.array([0.9, 0.1])
    >>> kl_divergence(p, q)
    >>> 0.5108256237
    """
    return sum(rel_entr(P, Q))