from __future__ import annotations

import json
from math import isclose
from pathlib import Path

from src.anti_phase_temporal import (
    anti_phase_floquet_exponent,
    dimensionless_premium,
    dimensionless_premium_derivative,
    exact_optimal_dimensionless_migration,
    weak_contrast_optimal_dimensionless_migration,
    weak_contrast_shape,
)
from src.two_patch_floquet import two_season_closed_form


def verify() -> dict[str, object]:
    # 1. Closed form agrees with the general two-season Floquet implementation.
    floquet_cases = []
    max_formula_error = 0.0
    for rbar in (-0.3, 0.0, 0.4):
        for x in (0.15, 0.8, 2.0):
            for m in (0.03, 0.4, 2.5):
                for tau in (0.2, 0.8, 2.0):
                    seasons = [
                        (rbar + x, rbar - x, tau),
                        (rbar - x, rbar + x, tau),
                    ]
                    general = two_season_closed_form(seasons, m)
                    exact = anti_phase_floquet_exponent(rbar, x, m, tau)
                    err = abs(general - exact)
                    max_formula_error = max(max_formula_error, err)
                    assert isclose(general, exact, rel_tol=2e-11, abs_tol=2e-11)
                    floquet_cases.append((rbar, x, m, tau))

    # 2. Numerical implementation follows the theorem's derivative sign change
    # on a broad contrast grid. This is an implementation receipt, not the proof.
    v_grid = [0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0, 100.0]
    optimum_rows = []
    for v in v_grid:
        u = exact_optimal_dimensionless_migration(v)
        d0 = dimensionless_premium_derivative(u, v)
        before = dimensionless_premium_derivative(0.7 * u, v)
        after = dimensionless_premium_derivative(1.4 * u, v)
        assert abs(d0) < 2e-9
        assert before > 0.0
        assert after < 0.0
        peak = dimensionless_premium(u, v)
        assert peak > dimensionless_premium(0.25 * u, v)
        assert peak > dimensionless_premium(4.0 * u, v)
        optimum_rows.append(
            {
                "v": v,
                "u_star": u,
                "derivative_at_u_star": d0,
                "derivative_before": before,
                "derivative_after": after,
            }
        )

    # 3. Weak-contrast constants used in the manuscript.
    weak_u = weak_contrast_optimal_dimensionless_migration()
    weak_h = weak_contrast_shape(weak_u)
    assert isclose(weak_u, 1.60611529880277, rel_tol=1e-12, abs_tol=1e-12)
    assert isclose(weak_h, 0.1324875394468274, rel_tol=1e-12, abs_tol=1e-12)
    weak_exact = exact_optimal_dimensionless_migration(0.01)
    assert abs(weak_exact - weak_u) / weak_u < 2e-4

    # 4. Strong-contrast expansion u*=1+1/v+O(v^-2).
    strong_rows = []
    for v in (10.0, 30.0, 100.0):
        exact_u = exact_optimal_dimensionless_migration(v)
        first_order = 1.0 + 1.0 / v
        scaled_remainder = (exact_u - first_order) * v * v
        strong_rows.append(
            {
                "v": v,
                "exact_u_star": exact_u,
                "first_order": first_order,
                "v2_scaled_remainder": scaled_remainder,
            }
        )
    assert abs(strong_rows[-1]["exact_u_star"] - 1.0) < 0.011

    return {
        "paper": "PAYOFF_B_THEORETICAL_ECOLOGY_BRIEF_V1",
        "claim": "unique positive global migration optimum in the symmetric anti-phase model",
        "analytic_proof_source": "theory/EXACT_ANTI_PHASE_OPTIMUM.md",
        "numerical_receipt_is_not_proof": True,
        "floquet_formula_cases": len(floquet_cases),
        "max_floquet_formula_abs_error": max_formula_error,
        "optimum_grid": optimum_rows,
        "weak_contrast": {"u_star": weak_u, "shape_max": weak_h},
        "strong_contrast": strong_rows,
        "all_checks_pass": True,
    }


def main() -> None:
    receipt = verify()
    out = Path("submission/theoretical_ecology/generated/PAYOFF_B_VERIFICATION_RECEIPT.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(receipt, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
