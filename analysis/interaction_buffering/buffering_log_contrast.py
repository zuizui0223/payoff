"""Log-mean contrast machinery; no biological estimates or imputed covariance."""
from __future__ import annotations
import numpy as np


def log_mean_contrasts(means, covariance_of_means, contrasts):
    """Delta-method estimates and joint sampling covariance.

    Means must be strictly positive and on the same endpoint scale. The
    covariance is for estimated means at the actual randomization/analysis
    unit, not individual outcomes. Never silently assume independence.
    """
    m = np.asarray(means, dtype=float)
    v = np.asarray(covariance_of_means, dtype=float)
    c = np.atleast_2d(np.asarray(contrasts, dtype=float))
    if m.ndim != 1 or not len(m) or not np.all(np.isfinite(m)) or np.any(m <= 0):
        raise ValueError('positive finite means required; use endpoint-specific model for zeros')
    n = len(m)
    if v.shape != (n, n) or c.ndim != 2 or c.shape[1] != n:
        raise ValueError('dimension mismatch')
    if not np.all(np.isfinite(v)) or not np.all(np.isfinite(c)):
        raise ValueError('finite covariance and contrasts required')
    if not np.allclose(v, v.T, rtol=1e-10, atol=1e-12):
        raise ValueError('covariance must be symmetric')
    v = (v + v.T) / 2
    if np.any(np.diag(v) < 0) or np.linalg.eigvalsh(v).min() < -1e-10 * max(1, np.linalg.norm(v, 2)):
        raise ValueError('covariance must be positive semidefinite')
    if not np.allclose(c.sum(axis=1), 0, rtol=0, atol=1e-12):
        raise ValueError('contrast must sum to zero')
    a = c / m
    return c @ np.log(m), a @ v @ a.T


def independent_mean_covariance(sds, ns, *, independent_arms_verified):
    """Only for documented independent arms and independent-unit SDs/counts."""
    if independent_arms_verified is not True:
        raise ValueError('independence must be documented')
    sd, n = np.asarray(sds, float), np.asarray(ns, float)
    if sd.ndim != 1 or n.shape != sd.shape or not len(n):
        raise ValueError('dimension mismatch')
    if not np.all(np.isfinite(sd)) or not np.all(np.isfinite(n)) or np.any(sd < 0) or np.any(n < 2) or np.any(n != np.floor(n)):
        raise ValueError('valid unit SDs and integer n >= 2 required')
    return np.diag(sd**2/n)


def factorial_buffer(means_00_10_01_11, covariance_of_means):
    """D timing perturbation, B buffer, arm order 00,10,01,11.

    Return low-buffer delay log ratio, high-buffer delay log ratio, their
    difference theta and full joint covariance. Positive theta is attenuation
    only if the low-buffer perturbation is detrimental. No causal conclusion
    follows from the numerical function itself.
    """
    est, cov = log_mean_contrasts(means_00_10_01_11, covariance_of_means,
                                  [[-1,1,0,0],[0,0,-1,1],[1,-1,-1,1]])
    return {'low_buffer': float(est[0]), 'high_buffer': float(est[1]),
            'theta': float(est[2]), 'covariance': cov.tolist(),
            'low_buffer_detrimental_point_estimate': bool(est[0] < 0)}
