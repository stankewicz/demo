r"""
Orthogonal arrays

This module gathers everything related to orthogonal arrays (or transversal
designs). One can build an `OA(k,n)` (or check that it can be built) with
:func:`orthogonal_array`::

    sage: OA = designs.orthogonal_array(4,8)

It defines the following functions:

.. csv-table::
    :class: contentstable
    :widths: 30, 70
    :delim: |

    :meth:`orthogonal_array` | Return an orthogonal array of parameters `k,n,t`.
    :meth:`transversal_design` | Return a transversal design of parameters `k,n`.
    :meth:`incomplete_orthogonal_array` | Return an `OA(k,n)-\sum_{1\leq i\leq x} OA(k,s_i)`.


.. csv-table::
    :class: contentstable
    :widths: 30, 70
    :delim: |

    :meth:`is_transversal_design` | Check that a given set of blocks ``B`` is a transversal design.
    :meth:`~sage.combinat.designs.designs_pyx.is_orthogonal_array` | Check that the integer matrix `OA` is an `OA(k,n,t)`.
    :meth:`wilson_construction` | Return a `OA(k,rm+u)` from a truncated `OA(k+s,r)` by Wilson's construction.
    :meth:`TD_product` | Return the product of two transversal designs.
    :meth:`OA_find_disjoint_blocks` | Return `x` disjoint blocks contained in a given `OA(k,n)`.
    :meth:`OA_relabel` | Return a relabelled version of the OA.
    :meth:`OA_from_quasi_difference_matrix` | Return an Orthogonal Array from a Quasi-Difference matrix
    :meth:`OA_from_Vmt` | Return an Orthogonal Array from a `V(m,t)`
    :meth:`OA_from_PBD` | Return an `OA(k,n)` from a PBD
    :meth:`OA_from_wider_OA` | Return the first `k` columns of `OA`.

.. TODO::

    - A resolvable `OA(k,n)` is equivalent to a `OA(k+1,n)`. Sage should be able
      to return resolvable OA, with sorted rows (so that building the
      decomposition is easy.

REFERENCES:

.. [CD96] Making the MOLS table
  Charles Colbourn and Jeffrey Dinitz
  Computational and constructive design theory
  vol 368,pages 67-134
  1996

Functions
---------

"""
from sage.misc.cachefunc import cached_function
from sage.categories.sets_cat import EmptySetError
from sage.misc.unknown import Unknown
from sage.rings.infinity import Infinity
from designs_pyx import is_orthogonal_array


def transversal_design(k,n,check=True,existence=False):
    r"""
    Return a transversal design of parameters `k,n`.

    A transversal design of parameters `k, n` is a collection `\mathcal{S}` of
    subsets of `V = V_1 \cup \cdots \cup V_k` (where the *groups* `V_i` are
    disjoint and have cardinality `n`) such that:

    * Any `S \in \mathcal{S}` has cardinality `k` and intersects each group on
      exactly one element.

    * Any two elements from distincts groups are contained in exactly one
      element of `\mathcal{S}`.

    More general definitions sometimes involve a `\lambda` parameter, and we
    assume here that `\lambda=1`.

    For more information on transversal designs, see
    `<http://mathworld.wolfram.com/TransversalDesign.html>`_.

    INPUT:

    - `n,k` -- integers. If ``k is None`` it is set to the largest value
      available.

    - ``check`` -- (boolean) Whether to check that output is correct before
      returning it. As this is expected to be useless (but we are cautious
      guys), you may want to disable it whenever you want speed. Set to
      ``True`` by default.

    - ``existence`` (boolean) -- instead of building the design, return:

        - ``True`` -- meaning that Sage knows how to build the design

        - ``Unknown`` -- meaning that Sage does not know how to build the
          design, but that the design may exist (see :mod:`sage.misc.unknown`).

        - ``False`` -- meaning that the design does not exist.

      .. NOTE::

          When ``k=None`` and ``existence=True`` the function returns an
          integer, i.e. the largest `k` such that we can build a `TD(k,n)`.

    OUTPUT:

    The kind of output depends on the input:

    - if ``existence=False`` (the default) then the output is a list of lists
      that represent a `TD(k,n)` with
      `V_1=\{0,\dots,n-1\},\dots,V_k=\{(k-1)n,\dots,kn-1\}`

    - if ``existence=True`` and ``k`` is an integer, then the function returns a
      troolean: either ``True``, ``Unknown`` or ``False``

    - if ``existence=True`` and ``k=None`` then the output is the largest value
      of ``k`` for which Sage knows how to compute a `TD(k,n)`.

    .. SEEALSO::

        :func:`orthogonal_array` -- a tranversal design `TD(k,n)` is equivalent to an
        orthogonal array `OA(k,n,2)`.

    EXAMPLES::

        sage: designs.transversal_design(5,5)
        [[0, 5, 10, 15, 20], [0, 6, 12, 18, 24], [0, 7, 14, 16, 23],
         [0, 8, 11, 19, 22], [0, 9, 13, 17, 21], [1, 5, 14, 18, 22],
         [1, 6, 11, 16, 21], [1, 7, 13, 19, 20], [1, 8, 10, 17, 24],
         [1, 9, 12, 15, 23], [2, 5, 13, 16, 24], [2, 6, 10, 19, 23],
         [2, 7, 12, 17, 22], [2, 8, 14, 15, 21], [2, 9, 11, 18, 20],
         [3, 5, 12, 19, 21], [3, 6, 14, 17, 20], [3, 7, 11, 15, 24],
         [3, 8, 13, 18, 23], [3, 9, 10, 16, 22], [4, 5, 11, 17, 23],
         [4, 6, 13, 15, 22], [4, 7, 10, 18, 21], [4, 8, 12, 16, 20],
         [4, 9, 14, 19, 24]]

    Some examples of the maximal number of transversal Sage is able to build::

        sage: TD_4_10 = designs.transversal_design(4,10)
        sage: designs.transversal_design(5,10,existence=True)
        Unknown

    For prime powers, there is an explicit construction which gives a
    `TD(n+1,n)`::

        sage: designs.transversal_design(4, 3, existence=True)
        True
        sage: designs.transversal_design(674, 673, existence=True)
        True

    For other values of ``n`` it depends::

        sage: designs.transversal_design(7, 6, existence=True)
        False
        sage: designs.transversal_design(4, 6, existence=True)
        Unknown
        sage: designs.transversal_design(3, 6, existence=True)
        True

        sage: designs.transversal_design(11, 10, existence=True)
        False
        sage: designs.transversal_design(4, 10, existence=True)
        True
        sage: designs.transversal_design(5, 10, existence=True)
        Unknown

        sage: designs.transversal_design(7, 20, existence=True)
        Unknown
        sage: designs.transversal_design(6, 12, existence=True)
        True
        sage: designs.transversal_design(7, 12, existence=True)
        True
        sage: designs.transversal_design(8, 12, existence=True)
        Unknown

        sage: designs.transversal_design(6, 20, existence = True)
        True
        sage: designs.transversal_design(7, 20, existence = True)
        Unknown

    If you ask for a transversal design that Sage is not able to build then an
    ``EmptySetError`` or a ``NotImplementedError`` is raised::

        sage: designs.transversal_design(47, 100)
        Traceback (most recent call last):
        ...
        NotImplementedError: I don't know how to build a TD(47,100)!
        sage: designs.transversal_design(55, 54)
        Traceback (most recent call last):
        ...
        EmptySetError: There exists no TD(55,54)!

    Those two errors correspond respectively to the cases where Sage answer
    ``Unknown`` or ``False`` when the parameter ``existence`` is set to
    ``True``::

        sage: designs.transversal_design(47, 100, existence=True)
        Unknown
        sage: designs.transversal_design(55, 54, existence=True)
        False

    If for a given `n` you want to know the largest `k` for which Sage is able
    to build a `TD(k,n)` just call the function with `k` set to ``None`` and
    ``existence`` set to ``True`` as follows::

        sage: designs.transversal_design(None, 6, existence=True)
        3
        sage: designs.transversal_design(None, 20, existence=True)
        6
        sage: designs.transversal_design(None, 30, existence=True)
        6
        sage: designs.transversal_design(None, 120, existence=True)
        9

    TESTS:

    The case when `n=1`::

        sage: designs.transversal_design(5,1)
        [[0, 1, 2, 3, 4]]

    Obtained through Wilson's decomposition::

        sage: _ = designs.transversal_design(4,38)

    Obtained through product decomposition::

        sage: _ = designs.transversal_design(6,60)
        sage: _ = designs.transversal_design(5,60) # checks some tricky divisibility error

    For small values of the parameter ``n`` we check the coherence of the
    function :func:`transversal_design`::

        sage: for n in xrange(2,25):                               # long time -- 15 secs
        ....:     i = 2
        ....:     while designs.transversal_design(i, n, existence=True) is True:
        ....:         i += 1
        ....:     _ = designs.transversal_design(i-1, n)
        ....:     assert designs.transversal_design(None, n, existence=True) == i - 1
        ....:     j = i
        ....:     while designs.transversal_design(j, n, existence=True) is Unknown:
        ....:         try:
        ....:             _ = designs.transversal_design(j, n)
        ....:             raise AssertionError("no NotImplementedError")
        ....:         except NotImplementedError:
        ....:             pass
        ....:         j += 1
        ....:     k = j
        ....:     while k < n+4:
        ....:         assert designs.transversal_design(k, n, existence=True) is False
        ....:         try:
        ....:             _ = designs.transversal_design(k, n)
        ....:             raise AssertionError("no EmptySetError")
        ....:         except EmptySetError:
        ....:             pass
        ....:         k += 1
        ....:     print "%2d: (%2d, %2d)"%(n,i,j)
         2: ( 4,  4)
         3: ( 5,  5)
         4: ( 6,  6)
         5: ( 7,  7)
         6: ( 4,  7)
         7: ( 9,  9)
         8: (10, 10)
         9: (11, 11)
        10: ( 5, 11)
        11: (13, 13)
        12: ( 8, 14)
        13: (15, 15)
        14: ( 7, 15)
        15: ( 7, 17)
        16: (18, 18)
        17: (19, 19)
        18: ( 8, 20)
        19: (21, 21)
        20: ( 7, 22)
        21: ( 8, 22)
        22: ( 6, 23)
        23: (25, 25)
        24: (10, 26)

    The special case `n=1`::

        sage: designs.transversal_design(3, 1)
        [[0, 1, 2]]
        sage: designs.transversal_design(None, 1, existence=True)
        +Infinity
        sage: designs.transversal_design(None, 1)
        Traceback (most recent call last):
        ...
        ValueError: there is no upper bound on k when 0<=n<=1
    """
    # Is k is None we find the largest available
    if k is None:
        if n == 0 or n == 1:
            if existence:
                from sage.rings.infinity import Infinity
                return Infinity
            raise ValueError("there is no upper bound on k when 0<=n<=1")

        k = orthogonal_array(None,n,existence=True)
        if existence:
            return k

    if existence and _OA_cache_get(k,n) is not None:
        return _OA_cache_get(k,n)

    may_be_available = _OA_cache_construction_available(k,n) is not False

    if n == 1:
        if existence:
            return True
        TD = [range(k)]

    elif k >= n+2:
        if existence:
            return False
        raise EmptySetError("No Transversal Design exists when k>=n+2 if n>=2")

    elif n == 12 and k <= 6:
        _OA_cache_set(6,12,True)
        if existence:
            return True
        from sage.combinat.designs.database import TD_6_12
        TD = [l[:k] for l in TD_6_12()]

    # Section 6.6 of [Stinson2004]
    elif orthogonal_array(k, n, existence=True) is not Unknown:

        # Forwarding non-existence results
        if orthogonal_array(k, n, existence=True):
            if existence:
                return True
        else:
            if existence:
                return False
            raise EmptySetError("There exists no TD({},{})!".format(k,n))

        OA = orthogonal_array(k,n, check = False)
        TD = [[i*n+c for i,c in enumerate(l)] for l in OA]

    else:
        if existence:
            return Unknown
        raise NotImplementedError("I don't know how to build a TD({},{})!".format(k,n))

    if check:
        assert is_transversal_design(TD,k,n)

    return TD

def is_transversal_design(B,k,n, verbose=False):
    r"""
    Check that a given set of blocks ``B`` is a transversal design.

    See :func:`~sage.combinat.designs.orthogonal_arrays.transversal_design`
    for a definition.

    INPUT:

    - ``B`` -- the list of blocks

    - ``k, n`` -- integers

    - ``verbose`` (boolean) -- whether to display information about what is
      going wrong.

    .. NOTE::

        The tranversal design must have `\{0, \ldots, kn-1\}` as a ground set,
        partitioned as `k` sets of size `n`: `\{0, \ldots, k-1\} \sqcup
        \{k, \ldots, 2k-1\} \sqcup \cdots \sqcup \{k(n-1), \ldots, kn-1\}`.

    EXAMPLES::

        sage: TD = designs.transversal_design(5, 5, check=True) # indirect doctest
        sage: from sage.combinat.designs.orthogonal_arrays import is_transversal_design
        sage: is_transversal_design(TD, 5, 5)
        True
        sage: is_transversal_design(TD, 4, 4)
        False
    """
    return is_orthogonal_array([[x%n for x in R] for R in B],k,n,verbose=verbose)

def wilson_construction(OA,k,r,m,n_trunc,u,check=True):
    r"""
    Return a `OA(k,rm+u)` from a truncated `OA(k+s,r)` by Wilson's construction.

    Let `OA` be a truncated `OA(k+s,r)` with `s` truncated columns of sizes
    `u_1,...,u_s`, whose blocks have sizes in `\{k+b_1,...,k+b_t\}`. If there
    exist:

    - An `OA(k,m+b_i) - b_i.OA(k,1)` for every `1\leq i\leq t`

    - An `OA(k,u_i)` for every `1\leq i\leq s`

    Then there exists an `OA(k,rm+\sum u_i)`. The construction is a
    generalization of Lemma 3.16 in [HananiBIBD]_.

    INPUT:

    - ``OA`` -- an incomplete orthogonal array with ``k+n_trunc`` columns. The
      elements of a column of size `c` must belong to `\{0,...,c\}`. The missing
      entries of a block are represented by ``None`` values.

    - ``k,r,m,n_trunc`` (integers)

    - ``u`` (list) -- a list of length ``n_trunc`` such that column ``k+i`` has
      size ``u[i]``.

    - ``check`` (boolean) -- whether to check that output is correct before
      returning it. As this is expected to be useless (but we are cautious
      guys), you may want to disable it whenever you want speed. Set to ``True``
      by default.

    REFERENCE:

    .. [HananiBIBD] Balanced incomplete block designs and related designs,
      Haim Hanani,
      Discrete Mathematics 11.3 (1975) pages 255-369.

    EXAMPLES::

        sage: from sage.combinat.designs.orthogonal_arrays import wilson_construction
        sage: from sage.combinat.designs.orthogonal_arrays import OA_relabel
        sage: from sage.combinat.designs.orthogonal_arrays_recursive import find_wilson_decomposition_with_one_truncated_group
        sage: total = 0
        sage: for k in range(3,8):
        ....:    for n in range(1,30):
        ....:        if find_wilson_decomposition_with_one_truncated_group(k,n):
        ....:            total += 1
        ....:            f, args = find_wilson_decomposition_with_one_truncated_group(k,n)
        ....:            _ = f(*args)
        sage: print total
        41
    """
    n = r*m+sum(u)
    master_design = OA

    assert n_trunc == len(u)

    # Computing the sizes of the blocks by filtering out None entries
    block_sizes = set(sum(xx!=None for xx in B) for B in OA)

    # For each block of size k+i we need a OA(k,m+i)-i.OA(k,1)
    OA_k_mpi = {i-k+m: incomplete_orthogonal_array(k, i-k+m, (1,)*(i-k)) for i in block_sizes}

    # For each truncated column of size uu we need a OA(k,uu)
    OA_k_u = {uu: orthogonal_array(k, uu) for uu in u}

    # Building the actual design ! The set of integers is :
    # 0*m+0...0*m+(m-1)|...|(r-1)m+0...(r-1)m+(m-1)|mr+0...mr+(r1-1)|mr+r1...mr+r1+r2-1
    OA = []
    for B in master_design:
        # The missing entries belong to the last n_trunc columns
        assert all(x is not None for x in B[:k])
        n_in_truncated = n_trunc-B.count(None)

        # We replace the block with a OA(k,m+n_in_truncated) properly relabelled
        matrix = [range(i*m,(i+1)*m) for i in B[:k]]
        c = r*m
        for i in range(n_trunc):
            if B[k+i] is not None:
                for C in matrix:
                    C.append(c+B[k+i])
            c += u[i]
        OA.extend(OA_relabel(OA_k_mpi[m+n_in_truncated],k,m+n_in_truncated,matrix=matrix))

    # The missing OA(k,uu)
    c = r*m
    for uu in u:
        OA.extend(OA_relabel(OA_k_u[uu],k,u,matrix=[range(c,c+uu)]*k))
        c += uu

    if check:
        from designs_pyx import is_orthogonal_array
        assert is_orthogonal_array(OA,k,n,2)

    return OA

def TD_product(k,TD1,n1,TD2,n2, check=True):
    r"""
    Return the product of two transversal designs.

    From a transversal design `TD_1` of parameters `k,n_1` and a transversal
    design `TD_2` of parameters `k,n_2`, this function returns a transversal
    design of parameters `k,n` where `n=n_1\times n_2`.

    Formally, if the groups of `TD_1` are `V^1_1,\dots,V^1_k` and the groups of
    `TD_2` are `V^2_1,\dots,V^2_k`, the groups of the product design are
    `V^1_1\times V^2_1,\dots,V^1_k\times V^2_k` and its blocks are the
    `\{(x^1_1,x^2_1),\dots,(x^1_k,x^2_k)\}` where `\{x^1_1,\dots,x^1_k\}` is a
    block of `TD_1` and `\{x^2_1,\dots,x^2_k\}` is a block of `TD_2`.

    INPUT:

    - ``TD1, TD2`` -- transversal designs.

    - ``k,n1,n2`` (integers) -- see above.

    - ``check`` (boolean) -- Whether to check that output is correct before
      returning it. As this is expected to be useless (but we are cautious
      guys), you may want to disable it whenever you want speed. Set to ``True``
      by default.

    .. NOTE::

        This function uses transversal designs with
        `V_1=\{0,\dots,n-1\},\dots,V_k=\{(k-1)n,\dots,kn-1\}` both as input and
        ouptut.

    EXAMPLES::

        sage: from sage.combinat.designs.orthogonal_arrays import TD_product
        sage: TD1 = designs.transversal_design(6,7)
        sage: TD2 = designs.transversal_design(6,12)
        sage: TD6_84 = TD_product(6,TD1,7,TD2,12)
    """
    N = n1*n2
    TD = []
    for X1 in TD1:
        for X2 in TD2:
            TD.append([x1*n2+(x2%n2) for x1,x2 in zip(X1,X2)])
    if check:
        assert is_transversal_design(TD,k,N)

    return TD

# Stores for every integer n the four values :
# - max_true
# - min_unknown
# - max_unknown
# - min_false
#
# corresponding to the max/min values of which orthogonal_array returns
# truth_value.

_OA_cache = {0:(Infinity,None,None,None),1:(Infinity,None,None,None)}
def _OA_cache_set(k,n,truth_value):
    r"""
    Sets a value in the OA cache of existence results

    INPUT:

    - ``k,n`` (integers)

    - ``truth_value`` -- one of ``True,False,Unknown``

    EXAMPLES::

        sage: from sage.combinat.designs.orthogonal_arrays import _OA_cache_set, _OA_cache_get, _OA_cache
        sage: if 10 in _OA_cache:
        ....:    del _OA_cache[10]
        sage: _OA_cache_get(4,10)
        sage: _OA_cache_set(4,10,True)
        sage: _OA_cache_get(4,10)
        True
    """
    global _OA_cache

    k = int(k)
    n = int(n)

    max_true, min_unknown, max_unknown, min_false = _OA_cache.get(n,(0,None,None,n+2))

    if truth_value is True:
        max_true    = k if k>max_true else max_true
    elif truth_value is Unknown:
        min_unknown = k if (min_unknown is None or k<min_unknown) else min_unknown
        max_unknown = k if (max_unknown is None or k>max_unknown) else max_unknown
    else:
        min_false   = k if k<min_false else min_false

    _OA_cache[n] = (max_true, min_unknown, max_unknown, min_false)

def _OA_cache_get(k,n):
    r"""
    Gets a value from the OA cache of existence results

    INPUT:

    ``k,n`` (integers)

    EXAMPLES::

        sage: from sage.combinat.designs.orthogonal_arrays import _OA_cache_set, _OA_cache_get
        sage: _OA_cache_get(0,10)
        True
        sage: _OA_cache_get(1,10)
        True
        sage: _OA_cache_get(2,10)
        True
        sage: _OA_cache_get(2**10+1,2**10)
        sage: _OA_cache_set(2**10+1,2**10,True)
        sage: _OA_cache_get(2**10+1,2**10)
        True
    """
    global _OA_cache

    k = int(k)
    n = int(n)

    try:
        max_true, min_unknown, max_unknown, min_false = _OA_cache[n]
    except KeyError:
        return None

    if k <= max_true:
        return True
    elif min_unknown is not None and (k >= min_unknown and k <= max_unknown):
        return Unknown
    elif k >= min_false:
        return False

    return None

def _OA_cache_construction_available(k,n):
    r"""
    Tests if a construction is implemented using the cache's information

    INPUT:

    - ``k,n`` (integers)

    EXAMPLES::

        sage: from sage.combinat.designs.orthogonal_arrays import _OA_cache_construction_available
        sage: _OA_cache_construction_available(5,10)
        Unknown
        sage: designs.orthogonal_array(5,10,existence=True)
        Unknown
        sage: _OA_cache_construction_available(5,10)
        False
    """
    ans = _OA_cache.get(n,None)
    if ans is not None:
        max_true, min_unknown, max_unknown, min_false = ans
        if k <= max_true:
            return True
        if min_unknown is not None and k >= min_unknown:
            return False
        else:
            return Unknown
    else:
        return Unknown

def orthogonal_array(k,n,t=2,check=True,existence=False):
    r"""
    Return an orthogonal array of parameters `k,n,t`.

    An orthogonal array of parameters `k,n,t` is a matrix with `k` columns
    filled with integers from `[n]` in such a way that for any `t` columns, each
    of the `n^t` possible rows occurs exactly once. In
    particular, the matrix has `n^t` rows.

    More general definitions sometimes involve a `\lambda` parameter, and we
    assume here that `\lambda=1`.

    For more information on orthogonal arrays, see
    :wikipedia:`Orthogonal_array`.

    INPUT:

    - ``k`` -- (integer) number of columns. If ``k=None`` it is set to the
      largest value available.

    - ``n`` -- (integer) number of symbols

    - ``t`` -- (integer; default: 2) -- strength of the array

    - ``check`` -- (boolean) Whether to check that output is correct before
      returning it. As this is expected to be useless (but we are cautious
      guys), you may want to disable it whenever you want speed. Set to
      ``True`` by default.

    - ``existence`` (boolean) -- instead of building the design, return:

        - ``True`` -- meaning that Sage knows how to build the design

        - ``Unknown`` -- meaning that Sage does not know how to build the
          design, but that the design may exist (see :mod:`sage.misc.unknown`).

        - ``False`` -- meaning that the design does not exist.

      .. NOTE::

          When ``k=None`` and ``existence=True`` the function returns an
          integer, i.e. the largest `k` such that we can build a `TD(k,n)`.

    OUTPUT:

    The kind of output depends on the input:

    - if ``existence=False`` (the default) then the output is a list of lists
      that represent an orthogonal array with parameters ``k`` and ``n``

    - if ``existence=True`` and ``k`` is an integer, then the function returns a
      troolean: either ``True``, ``Unknown`` or ``False``

    - if ``existence=True`` and ``k=None`` then the output is the largest value
      of ``k`` for which Sage knows how to compute a `TD(k,n)`.

    .. NOTE::

        This method implements theorems from [Stinson2004]_. See the code's
        documentation for details.

    .. SEEALSO::

        When `t=2` an orthogonal array is also a transversal design (see
        :func:`transversal_design`) and a family of mutually orthogonal latin
        squares (see
        :func:`~sage.combinat.designs.latin_squares.mutually_orthogonal_latin_squares`).

    EXAMPLES::

        sage: designs.orthogonal_array(3,2)
        [[0, 0, 0], [0, 1, 1], [1, 0, 1], [1, 1, 0]]

        sage: designs.orthogonal_array(5,5)
        [[0, 0, 0, 0, 0], [0, 1, 2, 3, 4], [0, 2, 4, 1, 3],
         [0, 3, 1, 4, 2], [0, 4, 3, 2, 1], [1, 0, 4, 3, 2],
         [1, 1, 1, 1, 1], [1, 2, 3, 4, 0], [1, 3, 0, 2, 4],
         [1, 4, 2, 0, 3], [2, 0, 3, 1, 4], [2, 1, 0, 4, 3],
         [2, 2, 2, 2, 2], [2, 3, 4, 0, 1], [2, 4, 1, 3, 0],
         [3, 0, 2, 4, 1], [3, 1, 4, 2, 0], [3, 2, 1, 0, 4],
         [3, 3, 3, 3, 3], [3, 4, 0, 1, 2], [4, 0, 1, 2, 3],
         [4, 1, 3, 0, 2], [4, 2, 0, 3, 1], [4, 3, 2, 1, 0],
         [4, 4, 4, 4, 4]]

    What is the largest value of `k` for which Sage knows how to compute a
    `OA(k,14,2)`?::

        sage: designs.orthogonal_array(None,14,existence=True)
        6

    If you ask for an orthogonal array that does not exist, then the function
    either raise an ``EmptySetError`` (if it knows that such an orthogonal array
    does not exist) or a ``NotImplementedError``::

        sage: designs.orthogonal_array(4,2)
        Traceback (most recent call last):
        ...
        EmptySetError: No Orthogonal Array exists when k>=n+t except when n<=1
        sage: designs.orthogonal_array(12,20)
        Traceback (most recent call last):
        ...
        NotImplementedError: I don't know how to build an OA(12,20)!

    Note that these errors correspond respectively to the answers ``False`` and
    ``Unknown`` when the parameter ``existence`` is set to ``True``::

        sage: designs.orthogonal_array(4,2,existence=True)
        False
        sage: designs.orthogonal_array(12,20,existence=True)
        Unknown

    TESTS:

    The special cases `n=0,1`::

        sage: designs.orthogonal_array(3,0)
        []
        sage: designs.orthogonal_array(3,1)
        [[0, 0, 0]]
        sage: designs.orthogonal_array(None,0,existence=True)
        +Infinity
        sage: designs.orthogonal_array(None,1,existence=True)
        +Infinity
        sage: designs.orthogonal_array(None,1)
        Traceback (most recent call last):
        ...
        ValueError: there is no upper bound on k when 0<=n<=1
        sage: designs.orthogonal_array(None,0)
        Traceback (most recent call last):
        ...
        ValueError: there is no upper bound on k when 0<=n<=1
        sage: designs.orthogonal_array(16,0)
        []
        sage: designs.orthogonal_array(16,1)
        [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    when `t>2` and `k=None`::

        sage: t = 3
        sage: designs.orthogonal_array(None,5,t=t,existence=True) == t
        True
        sage: _ = designs.orthogonal_array(t,5,t)
    """

    from latin_squares import mutually_orthogonal_latin_squares
    from database import OA_constructions, MOLS_constructions
    from block_design import projective_plane, projective_plane_to_OA
    from orthogonal_arrays_recursive import find_recursive_construction

    assert n>=0

    # If k is set to None we find the largest value available
    if k is None:
        if n == 0 or n == 1:
            if existence:
                from sage.rings.infinity import Infinity
                return Infinity
            raise ValueError("there is no upper bound on k when 0<=n<=1")
        elif t == 2 and projective_plane(n,existence=True):
            k = n+1
        else:
            for k in range(t-1,n+2):
                if not orthogonal_array(k+1,n,t=t,existence=True):
                    break
        if existence:
            return k

    if k < t:
        raise ValueError("undefined for k<t")

    if existence and _OA_cache_get(k,n) is not None and t == 2:
        return _OA_cache_get(k,n)

    may_be_available = _OA_cache_construction_available(k,n) is not False

    if n <= 1:
        if existence:
            return True
        OA = [[0]*k]*n

    elif k >= n+t:
        # When t=2 then k<n+t as it is equivalent to the existence of n-1 MOLS.
        # When t>2 the submatrix defined by the rows whose first t-2 elements
        # are 0s yields a OA with t=2 and k-(t-2) columns. Thus k-(t-2) < n+2,
        # i.e. k<n+t.
        if existence:
            return False
        raise EmptySetError("No Orthogonal Array exists when k>=n+t except when n<=1")

    elif k <= t:
        if existence:
            return True

        from itertools import product
        return map(list, product(range(n), repeat=k))

    elif t != 2:
        if existence:
            return Unknown
        raise NotImplementedError("Only trivial orthogonal arrays are implemented for t>=2")

    elif k <= 3:
        if existence:
            return True
        return [[i,j,(i+j)%n] for i in xrange(n) for j in xrange(n)]

    # projective spaces are equivalent to OA(n+1,n,2)
    elif (projective_plane(n, existence=True) or
           (k == n+1 and projective_plane(n, existence=True) is False)):
        _OA_cache_set(n+1,n,projective_plane(n, existence=True))
        if k == n+1:
            if existence:
                return projective_plane(n, existence=True)
            p = projective_plane(n, check=False)
            OA = projective_plane_to_OA(p, check=False)
        else:
            if existence:
                return True
            p = projective_plane(n, check=False)
            OA = [l[:k] for l in projective_plane_to_OA(p, check=False)]

    # Constructions from the database
    elif may_be_available and n in OA_constructions and k <= OA_constructions[n][0]:
        _OA_cache_set(OA_constructions[n][0],n,True)
        if existence:
            return True
        _, construction = OA_constructions[n]

        OA = OA_from_wider_OA(construction(),k)

    # Constructions from the database II
    elif may_be_available and k <= 6 and n == 12:
        _OA_cache_set(6,12,True)

        if existence:
            return True
        else:
            from database import TD_6_12
            TD = TD_6_12()
            OA = [[x%n for x in R] for R in TD]

    # Constructions from the database III
    # Section 6.5.1 from [Stinson2004]
    elif may_be_available and n in MOLS_constructions and k-2 <= MOLS_constructions[n][0]:
        _OA_cache_set(MOLS_constructions[n][0]+2,n,True)

        if existence:
            return True
        else:
            construction = MOLS_constructions[n][1]
            mols = construction()
            OA = [[i,j]+[m[i,j] for m in mols]
                  for i in range(n) for j in range(n)]
            OA = OA_from_wider_OA(OA,k)

    elif may_be_available and find_recursive_construction(k,n):
        _OA_cache_set(k,n,True)
        if existence:
            return True
        f,args = find_recursive_construction(k,n)
        OA = f(*args)

    else:
        _OA_cache_set(k,n,Unknown)
        if existence:
            return Unknown
        raise NotImplementedError("I don't know how to build an OA({},{})!".format(k,n))

    if check:
        assert is_orthogonal_array(OA,k,n,t)

    return OA

def incomplete_orthogonal_array(k,n,holes_sizes,existence=False):
    r"""
    Return an `OA(k,n)-\sum_{1\leq i\leq x} OA(k,s_i)`.

    An `OA(k,n)-\sum_{1\leq i\leq x} OA(k,s_i)` is an orthogonal array from
    which have been removed disjoint `OA(k,s_1),...,OA(k,s_x)`. So it can
    exist only if a `OA(k,n)` exists.

    A very useful particular case (see e.g. the Wilson construction in
    :func:`wilson_construction`) is when all `s_i=1`. In that case the
    incomplete design is a `OA(k,n)-x.OA(k,1)`. Such design is equivalent to
    transversal design `TD(k,n)` from which has been removed `x` disjoint
    blocks. This specific case is the only one available through this function
    at the moment.

    INPUT:

    - ``k,n`` (integers)

    - ``holes_sizes`` (list of integers) -- respective sizes of the holes to be
      found.

      .. NOTE::

          Right now the feature is only available when all holes have size 1,
          i.e. `s_i=1`.

    - ``existence`` (boolean) -- instead of building the design, return:

        - ``True`` -- meaning that Sage knows how to build the design

        - ``Unknown`` -- meaning that Sage does not know how to build the
          design, but that the design may exist (see :mod:`sage.misc.unknown`).

        - ``False`` -- meaning that the design does not exist.

    .. NOTE::

        By convention, the ground set is always `V = \{0, ..., n-1\}` and the
        holes are `\{n-1, ..., n-s_1\}^k`, `\{n-s_1-1,...,n-s_1-s_2\}^k`, etc.

    .. SEEALSO::

        :func:`OA_find_disjoint_blocks`

    EXAMPLES::

        sage: IOA = designs.incomplete_orthogonal_array(3,3,[1,1,1])
        sage: IOA
        [[0, 1, 2], [0, 2, 1], [1, 0, 2], [1, 2, 0], [2, 0, 1], [2, 1, 0]]
        sage: missing_blocks = [[0,0,0],[1,1,1],[2,2,2]]
        sage: from sage.combinat.designs.orthogonal_arrays import is_orthogonal_array
        sage: is_orthogonal_array(IOA + missing_blocks,3,3,2)
        True

    TESTS:

    Affine planes and projective planes::

        sage: for q in xrange(2,100):
        ....:     if is_prime_power(q):
        ....:         assert designs.incomplete_orthogonal_array(q,q,[1]*q,existence=True)
        ....:         assert not designs.incomplete_orthogonal_array(q+1,q,[1]*2,existence=True)

    Further tests::

        sage: designs.incomplete_orthogonal_array(8,4,[1,1,1],existence=True)
        False
        sage: designs.incomplete_orthogonal_array(5,10,[1,1,1],existence=True)
        Unknown
        sage: designs.incomplete_orthogonal_array(5,10,[1,1,1])
        Traceback (most recent call last):
        ...
        NotImplementedError: I don't know how to build an OA(5,10)!
        sage: designs.incomplete_orthogonal_array(4,3,[1,1])
        Traceback (most recent call last):
        ...
        EmptySetError: There is no OA(n+1,n) - 2.OA(n+1,1) as all blocks do
        intersect in a projective plane.
        sage: n=10
        sage: k=designs.orthogonal_array(None,n,existence=True)
        sage: designs.incomplete_orthogonal_array(k,n,[1,1,1],existence=True)
        True
        sage: _ = designs.incomplete_orthogonal_array(k,n,[1,1,1])
        sage: _ = designs.incomplete_orthogonal_array(k,n,[1])

    REFERENCES:

    .. [BvR82] More mutually orthogonal Latin squares,
      Andries Brouwer and John van Rees
      Discrete Mathematics
      vol.39, num.3, pages 263-281
      1982
    """
    assert all(xx > 0 for xx in holes_sizes)

    y = sum(holes_sizes)
    x = len(holes_sizes)
    if y > n:
        if existence:
            return False
        raise EmptySetError("The total size of holes must be smaller or equal than the size of the ground set")

    if any(xx != 1 for xx in holes_sizes):
        if existence:
            return Unknown
        raise NotImplementedError("This function is only implemented for holes of size 1")

    # Easy case
    if x <= 1:
        if existence:
            return orthogonal_array(k,n,existence=True)
        OA = orthogonal_array(k,n)
        independent_set = OA[:x]

    elif x <= 3 and n > k-1 and k >= 3 and existence:
        # This is lemma 2.3 from [BvR82]_ with u=1
        return orthogonal_array(k,n,existence=True)

    elif x >= 2 and k == n+1:
        if existence:
            return False
        raise EmptySetError("There is no OA(n+1,n) - {}.OA(n+1,1) as all blocks do intersect in a projective plane.".format(x))

    # If we can build OA(k+1,n) then we can find n disjoint blocks in OA(k,n)
    elif orthogonal_array(k+1,n,existence=True):
        if existence:
            return True
        OA = orthogonal_array(k+1,n)
        independent_set = [B[:-1] for B in OA if B[-1] == 0][:x]
        OA = [B[:-1] for B in OA]

    elif orthogonal_array(k,n,existence=True):
        OA = orthogonal_array(k,n)
        try:
            independent_set = OA_find_disjoint_blocks(OA,k,n,x)
        except ValueError:
            if existence:
                return Unknown
            raise NotImplementedError("I was not able to build this OA({},{})-{}.OA({},1)".format(k,n,x,k))
        if existence:
            return True
        independent_set = OA_find_disjoint_blocks(OA,k,n,x)

    else:
        return orthogonal_array(k,n,existence=existence)

    assert x == len(independent_set)

    for B in independent_set:
        OA.remove(B)

    OA = OA_relabel(OA,k,n,blocks=independent_set)

    return OA

def OA_find_disjoint_blocks(OA,k,n,x):
    r"""
    Return `x` disjoint blocks contained in a given `OA(k,n)`.

    `x` blocks of an `OA` are said to be disjoint if they all have
    different values for a every given index, i.e. if they correspond to
    disjoint blocks in the `TD` assciated with the `OA`.

    INPUT:

    - ``OA`` -- an orthogonal array

    - ``k,n,x`` (integers)

    .. SEEALSO::

        :func:`incomplete_orthogonal_array`

    EXAMPLES::

        sage: from sage.combinat.designs.orthogonal_arrays import OA_find_disjoint_blocks
        sage: k=3;n=4;x=3
        sage: Bs = OA_find_disjoint_blocks(designs.orthogonal_array(k,n),k,n,x)
        sage: assert len(Bs) == x
        sage: for i in range(k):
        ....:     assert len(set([B[i] for B in Bs])) == x
        sage: OA_find_disjoint_blocks(designs.orthogonal_array(k,n),k,n,5)
        Traceback (most recent call last):
        ...
        ValueError: There does not exist 5 disjoint blocks in this OA(3,4)
    """

    # Computing an independent set of order x with a Linear Program
    from sage.numerical.mip import MixedIntegerLinearProgram, MIPSolverException
    p = MixedIntegerLinearProgram()
    b = p.new_variable(binary=True)
    p.add_constraint(p.sum(b[i] for i in range(len(OA))) == x)

    # t[i][j] lists of blocks of the OA whose i'th component is j
    t = [[[] for _ in range(n)] for _ in range(k)]
    for c,B in enumerate(OA):
        for i,j in enumerate(B):
            t[i][j].append(c)

    for R in t:
        for L in R:
            p.add_constraint(p.sum(b[i] for i in L) <= 1)

    try:
        p.solve()
    except MIPSolverException:
        raise ValueError("There does not exist {} disjoint blocks in this OA({},{})".format(x,k,n))

    b = p.get_values(b)
    independent_set = [OA[i] for i,v in b.items() if v]
    return independent_set

def OA_relabel(OA,k,n,blocks=tuple(),matrix=None):
    r"""
    Return a relabelled version of the OA.

    INPUT:

    - ``OA`` -- an OA, or rather a list of blocks of length `k`, each
      of which contains integers from `0` to `n-1`.

    - ``k,n`` (integers)

    - ``blocks`` (list of blocks) -- relabels the integers of the OA
      from `[0..n-1]` into `[0..n-1]` in such a way that the `i`
      blocks from ``block`` are respectively relabeled as
      ``[n-i,...,n-i]``, ..., ``[n-1,...,n-1]``. Thus, the blocks from
      this list are expected to have disjoint values for each
      coordinate.

      If set to the empty list (default) no such relabelling is
      performed.

    - ``matrix`` -- a matrix of dimensions `k,n` such that if the i th
      coordinate of a block is `x`, this `x` will be relabelled with
      ``matrix[i][x]``. This is not necessarily an integer between `0`
      and `n-1`, and it is not necessarily an integer either. This is
      performed *after* the previous relabelling.

      If set to ``None`` (default) no such relabelling is performed.

      .. NOTE::

          A ``None`` coordinate in one block remains a ``None``
          coordinate in the final block.

    EXAMPLES::

        sage: from sage.combinat.designs.orthogonal_arrays import OA_relabel
        sage: OA = designs.orthogonal_array(3,2)
        sage: OA_relabel(OA,3,2,matrix=[["A","B"],["C","D"],["E","F"]])
        [['A', 'C', 'E'], ['A', 'D', 'F'], ['B', 'C', 'F'], ['B', 'D', 'E']]

        sage: TD = OA_relabel(OA,3,2,matrix=[[0,1],[2,3],[4,5]]); TD
        [[0, 2, 4], [0, 3, 5], [1, 2, 5], [1, 3, 4]]
        sage: from sage.combinat.designs.orthogonal_arrays import is_transversal_design
        sage: is_transversal_design(TD,3,2)
        True

    Making sure that ``[2,2,2,2]`` is a block of `OA(4,3)`. We do this
    by relabelling block ``[0,0,0,0]`` which belongs to the design::

        sage: designs.orthogonal_array(4,3)
        [[0, 0, 0, 0], [0, 1, 2, 1], [0, 2, 1, 2], [1, 0, 2, 2], [1, 1, 1, 0], [1, 2, 0, 1], [2, 0, 1, 1], [2, 1, 0, 2], [2, 2, 2, 0]]
        sage: OA_relabel(designs.orthogonal_array(4,3),4,3,blocks=[[0,0,0,0]])
        [[2, 2, 2, 2], [2, 0, 1, 0], [2, 1, 0, 1], [0, 2, 1, 1], [0, 0, 0, 2], [0, 1, 2, 0], [1, 2, 0, 0], [1, 0, 2, 1], [1, 1, 1, 2]]

    TESTS::

        sage: OA_relabel(designs.orthogonal_array(3,2),3,2,blocks=[[0,1],[0,1]])
        Traceback (most recent call last):
        ...
        RuntimeError: Two block have the same coordinate for one of the k dimensions

    """
    if blocks:
        l = []
        for i,B in enumerate(zip(*blocks)): # the blocks are disjoint
            if len(B) != len(set(B)):
                raise RuntimeError("Two block have the same coordinate for one of the k dimensions")

            l.append(dict(zip([xx for xx in range(n) if xx not in B] + list(B),range(n))))

        OA = [[l[i][x] for i,x in enumerate(R)] for R in OA]

    if matrix:
        OA = [[matrix[i][j] if j is not None else None for i,j in enumerate(R)] for R in OA]

    return OA

def OA_from_quasi_difference_matrix(M,G,add_col=True):
    r"""
    Return an Orthogonal Array from a Quasi-Difference matrix

    **Difference Matrices**

    Let `G` be a group of order `g`. A *difference matrix* `M` is a `k \times g`
    matrix with entries from `G` such that for any `1\leq i < j < k` the set
    `\{d_{il}-d_{jl}:1\leq l \leq g\}` is equal to `G`.

    By concatenating the `g` matrices `M+x` (where `x\in G`), one obtains a
    matrix of size `x\times g^2` which is also an `OA(k,g)`.

    **Quasi-difference Matrices**

    A quasi-difference matrix is a difference matrix with missing entries. The
    construction above can be applied again in this case, where the missing
    entries in each column of `M` are replaced by unique values on which `G` has
    a trivial action.

    This produces an incomplete orthogonal array with a "hole" (i.e. missing
    rows) of size 'u' (i.e. the number of missing values per row of `M`). If
    there exists an `OA(k,u)`, then adding the rows of this `OA(k,u)` to the
    incomplete orthogonal array should lead to an OA...

    **Formal definition** (from the Handbook of Combinatorial Designs [DesignHandbook]_)

    Let `G` be an abelian group of order `n`. A
    `(n,k;\lambda,\mu;u)`-quasi-difference matrix (QDM) is a matrix `Q=(q_{ij})`
    with `k` rows and `\lambda(n-1+2u)+\mu` columns, with each entry either
    empty or containing an element of `G`. Each row contains exactly `\lambda u`
    entries, and each column contains at most one empty entry. Furthermore, for
    each `1 \leq i < j \leq k` the multiset

    .. MATH::

        \{ q_{il} - q_{jl}: 1 \leq l \leq \lambda (n-1+2u)+\mu, \text{ with }q_{il}\text{ and }q_{jl}\text{ not  empty}\}

    contains every nonzero element of `G` exactly `\lambda` times, and contains
    0 exactly `\mu` times.

    **Construction**

    If a `(n,k;\lambda,\mu;u)`-QDM exists and `\mu \leq \lambda`, then an
    `ITD_\lambda (k,n+u;u)` exists. Start with a `(n,k;\lambda,\mu;u)`-QDM `A`
    over the group `G`. Append `\lambda-\mu` columns of zeroes. Then select `u`
    elements `\infty_1,\dots,\infty_u` not in `G`, and replace the empty
    entries, each by one of these infinite symbols, so that `\infty_i` appears
    exactly once in each row. Develop the resulting matrix over the group `G`
    (leaving infinite symbols fixed), to obtain a `k\times \lambda (n^2+2nu)`
    matrix `T`. Then `T` is an orthogonal array with `k` rows and index
    `\lambda`, having `n+u` symbols and one hole of size `u`.

    Adding to `T` an `OA(k,u)` with elements `\infty_1,\dots,\infty_u` yields
    the `ITD_\lambda(k,n+u;u)`.

    For more information, see the Handbook of Combinatorial Designs
    [DesignHandbook]_ or
    `<http://web.cs.du.edu/~petr/milehigh/2013/Colbourn.pdf>`_.

    INPUT:

    - ``M`` -- the difference matrix whose entries belong to ``G``

    - ``G`` -- a group

    - ``add_col`` (boolean) -- whether to add a column to the final OA equal to
      `(x_1,\dots,x_g,x_1,\dots,x_g,\dots)` where `G=\{x_1,\dots,x_g\}`.

    EXAMPLES::

        sage: _ = designs.orthogonal_array(6,20,2) # indirect doctest
    """
    Gn = G.cardinality()
    k = len(M)+bool(add_col)
    G_to_int = {v:i for i,v in enumerate(G)}

    new_M = []
    for line in M:
        new_line = []
        # Concatenating the line+x, for all x \in G
        for g in G:
            inf = Gn
            for x in line:
                if x is None:
                    new_line.append(inf)
                    inf = inf + 1
                else:
                    new_line.append(G_to_int[g+G(x)])
        new_M.append(new_line)

    if add_col:
        new_M.append([i%(Gn) for i in range(len(new_line))])

    # new_M = transpose(new_M)
    new_M = zip(*new_M)

    # Filling holes with a smaller orthogonal array
    if inf > Gn:
        for L in orthogonal_array(k,inf-Gn,2):
            new_M.append(tuple([x+Gn for x in L]))

    return new_M

def OA_from_Vmt(m,t,V):
    r"""
    Return an Orthogonal Array from a `V(m,t)`

    **Definition**

    Let `q` be a prime power and let `q=mt+1` for `m,t` integers. Let `\omega`
    be a primitive element of `\mathbb{F}_q`. A `V(m,t)` vector is a vector
    `(a_1,\dots,a_{m+1}` for which, for each `1\leq k < m`, the differences

    .. MATH::

        \{a_{i+k}-a_i:1\leq i \leq m+1,i+k\neq m+2\}

    represent the `m` cyclotomic classes of `\mathbb{F}_{mt+1}` (compute subscripts
    modulo `m+2`). In other words, for fixed `k`, is
    `a_{i+k}-a_i=\omega^{mx+\alpha}` and `a_{j+k}-a_j=\omega^{my+\beta}` then
    `\alpha\not\equiv\beta \mod{m}`

    *Construction of a quasi-difference matrix from a `V(m,t)` vector*

    Starting with a `V(m,t)` vector `(a_1,\dots,a_{m+1})`, form a single column
    of length `m+2` whose first entry is empty, and whose remaining entries are
    `(a_1,\dots,a_{m+1})`. Form `t` columns by multiplying this column by the
    `t` th roots, i.e. the powers of `\omega^m`. From each of these `t` columns,
    form `m+2` columns by taking the `m+2` cyclic shifts of the column. The
    result is a `(a,m+2;1,0;t)-QDM`.

    For more information, refer to the Handbook of Combinatorial Designs
    [DesignHandbook]_.

    INPUT:

    - ``m,t`` (integers)

    - ``V`` -- the vector `V(m,t)`.

    .. SEEALSO::

        :func:`OA_from_quasi_difference_matrix`

    EXAMPLES::

        sage: _ = designs.orthogonal_array(6,46) # indirect doctest
    """
    from sage.rings.finite_rings.constructor import FiniteField
    q = m*t+1
    Fq = FiniteField(q)
    w = Fq.primitive_element()

    # Cyclic shift of a list
    cyclic_shift = lambda l,i : l[-i:]+l[:-i]

    M = []
    wm = w**m
    for i in range(t):
        L = [None]
        for e in V:
            L.append(e*wm**i)
        for ii in range(m+2):
            M.append(cyclic_shift(L,ii))

    M.append([0]*q)
    M = zip(*M)
    M = OA_from_quasi_difference_matrix(M,Fq,add_col = False)

    return M

def OA_from_PBD(k,n,PBD, check=True):
    r"""
    Return an `OA(k,n)` from a PBD

    **Construction**

    Let `\mathcal B` be a `(n,K,1)`-PBD. If there exists for every `i\in K` a
    `TD(k,i)-i\times TD(k,1)` (i.e. if there exist `k` idempotent MOLS), then
    one can obtain a `OA(k,n)` by concatenating:

    - A `TD(k,i)-i\times TD(k,1)` defined over the elements of `B` for every `B
      \in \mathcal B`.

    - The rows `(i,...,i)` of length `k` for every `i\in [n]`.

    .. NOTE::

        This function raises an exception when Sage is unable to build the
        necessary designs.

    INPUT:

    - ``k,n`` (integers)

    - ``PBD`` -- a PBD on `0,...,n-1`.

    EXAMPLES:

    We start from the example VI.1.2 from the [DesignHandbook]_ to build an
    `OA(3,10)`::

        sage: from sage.combinat.designs.orthogonal_arrays import OA_from_PBD
        sage: from sage.combinat.designs.designs_pyx import is_orthogonal_array
        sage: pbd = [[0,1,2,3],[0,4,5,6],[0,7,8,9],[1,4,7],[1,5,8],
        ....: [1,6,9],[2,4,9],[2,5,7],[2,6,8],[3,4,8],[3,5,9],[3,6,7]]
        sage: oa = OA_from_PBD(3,10,pbd)
        sage: is_orthogonal_array(oa, 3, 10)
        True

    But we cannot build an `OA(4,10)`::

        sage: OA_from_PBD(4,10,pbd)
        Traceback (most recent call last):
        ...
        EmptySetError: There is no OA(n+1,n) - 3.OA(n+1,1) as all blocks do intersect in a projective plane.

    Or an `OA(6,10)`::

        sage: _ = OA_from_PBD(3,6,pbd)
        Traceback (most recent call last):
        ...
        RuntimeError: The PBD covers a point 8 which is not in {0, ..., 5}
    """
    # Size of the sets of the PBD
    K = set(map(len,PBD))
    if check:
        from bibd import _check_pbd
        _check_pbd(PBD, n, K)

    # Building the IOA
    OAs = {i:incomplete_orthogonal_array(k,i,(1,)*i) for i in K}

    OA = []
    # For every block B of the PBD we add to the OA rows covering all pairs of
    # (distinct) coordinates within the elements of B.
    for S in PBD:
        for B in OAs[len(S)]:
            OA.append([S[i] for i in B])

    # Adding the 0..0, 1..1, 2..2 .... rows
    for i in range(n):
        OA.append([i]*k)

    if check:
        assert is_orthogonal_array(OA,k,n,2)

    return OA

def OA_from_wider_OA(OA,k):
    r"""
    Return the first `k` columns of `OA`.

    If `OA` has `k` columns, this function returns `OA` immediately.

    INPUT:

    - ``OA`` -- an orthogonal array.

    - ``k`` (integer)

    EXAMPLES::

        sage: from sage.combinat.designs.orthogonal_arrays import OA_from_wider_OA
        sage: OA_from_wider_OA(designs.orthogonal_array(6,20,2),1)[:5]
        [(19,), (0,), (0,), (7,), (1,)]
        sage: _ = designs.orthogonal_array(5,46) # indirect doctest

    """
    if len(OA[0]) == k:
        return OA
    return [L[:k] for L in OA]
