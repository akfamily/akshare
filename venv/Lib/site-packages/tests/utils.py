import hashlib

import numpy as np

# non-randomized hash function
hash = lambda s: int(hashlib.sha512(s.encode('utf-8')).hexdigest()[:16], 16)


def isclose(a, b, rel_tol=1e-06, abs_tol=0.0):
    if np.isnan(a) == np.isnan(b):
        return True
    if np.isinf(a) == np.isinf(b):
        return True
    if a == b:
        return True
    return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)


def record_arrays_close(x, y):
    for field in x.dtype.names:
        np.testing.assert_allclose(x[field], y[field], rtol=1e-06)
