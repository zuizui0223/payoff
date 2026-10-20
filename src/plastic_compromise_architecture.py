"""Exact plastic-versus-fixed-module boundary in a two-function Markov environment.

This is a declared minimal theoretical model, NOT a fit to Wurmbea, nor an
estimate of a structural origin, a new genetically accessible mutant, or
SLK's empirically identified architecture value Phi.

Both functions are active in every state, their positive quadratic weights
exchange priority across two Markov environments. The single shared
coordinate can stay constant or respond to a noisy cue; an idealized
two-coordinate fixed architecture resolves simultaneous mismatch at a
per-period construction/maintenance cost. All losses are log-fitness debits.

The optimized plasticity policy is constrained to *memoryless, symmetric,
linear cue amplitude*: x_t=Delta/2 + alpha*d*cue_t/2, alpha in [0,1].
It is not optimal over every possible memory-based learning strategy.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import isfinite, sqrt
from typing import Any


def _nonnegative(value: float, label: str) -> float:
    value = float(value)
    if not isfinite(value) or value < 0:
        raise ValueError(f"{label} must be finite and nonnegative")
    return value


@dataclass(frozen=True)
class PlasticCompromise:
    """Two swapped functional demands under a stationary symmetric Markov chain.

    A state has weights (a,b) on quadratic functions with optima 0 and
    Delta. The alternate state swaps (b,a). The Markov transition changes
    state with probability rho, and the contemporaneous binary cue identifies
    the current state with accuracy q independently conditional on the state.

    c is the cost per unit physical trait change whenever the observed cue
    differs from the previous observation. kappa is the fixed per-period cost
    of a separate two-coordinate, simultaneously operating architecture.
    """
    a: float
    b: float
    delta: float
    q: float
    rho: float
    plastic_running_cost: float
    plastic_switch_cost: float
    module_cost: float

    def __post_init__(self) -> None:
        for label in ("a", "b", "delta", "plastic_running_cost",
                      "plastic_switch_cost", "module_cost"):
            _nonnegative(getattr(self, label), label)
        if self.a <= 0 or self.b <= 0:
            raise ValueError("a and b must be strictly positive")
        if self.a < self.b:
            raise ValueError("a must be >= b; state labels otherwise exchanged")
        for label, lower, upper in (("q", 0.5, 1.0), ("rho", 0.0, 1.0)):
            value = float(getattr(self, label))
            if not isfinite(value) or value < lower or value > upper:
                raise ValueError(f"{label} must be in [{lower}, {upper}]")

    @property
    def unavoidable_simultaneous_conflict(self) -> float:
        """Per-state optimized single-coordinate loss, C>0 if Delta !=0."""
        return self.a * self.b / (self.a + self.b) * self.delta**2

    @property
    def between_environment_compromise_loss(self) -> float:
        """Extra loss of constant shared x=Delta/2 above optimized C."""
        return (
            (self.a - self.b)**2 * self.delta**2
            / (4.0 * (self.a + self.b))
        )

    @property
    def trait_optimum_separation(self) -> float:
        """Absolute between-state difference of state-optimized x."""
        return (self.a - self.b) * self.delta / (self.a + self.b)

    @property
    def cue_reliability_signal(self) -> float:
        return 2.0 * self.q - 1.0

    @property
    def cue_flip_probability(self) -> float:
        """Exact observed-cue switching probability, not state rho itself."""
        u = self.cue_reliability_signal
        return 2.0 * self.q * (1.0 - self.q) + self.rho * u * u

    @property
    def shared_loss(self) -> float:
        return (
            self.unavoidable_simultaneous_conflict
            + self.between_environment_compromise_loss
        )

    def plastic_loss(self, response_amplitude: float) -> float:
        """Long-run mean loss over the declared stationary state/cue process."""
        alpha = float(response_amplitude)
        if not isfinite(alpha) or not 0 <= alpha <= 1:
            raise ValueError("response_amplitude must lie in [0, 1]")
        T = self.between_environment_compromise_loss
        u = self.cue_reliability_signal
        return (
            self.unavoidable_simultaneous_conflict
            + T * (1.0 + alpha * alpha - 2.0 * alpha * u)
            + self.plastic_running_cost
            + self.plastic_switch_cost
            * self.trait_optimum_separation
            * alpha
            * self.cue_flip_probability
        )

    @property
    def optimal_memoryless_amplitude(self) -> float:
        """Exact constrained quadratic optimum including actual cue switching."""
        T = self.between_environment_compromise_loss
        if T == 0.0:
            return 0.0
        u = self.cue_reliability_signal
        penalty = (
            self.plastic_switch_cost
            * self.trait_optimum_separation
            * self.cue_flip_probability
            / (2.0 * T)
        )
        return max(0.0, min(1.0, u - penalty))

    @property
    def optimized_plastic_loss(self) -> float:
        return self.plastic_loss(self.optimal_memoryless_amplitude)

    def result(self, *, coordination_penalty: float = 0.0) -> dict[str, Any]:
        """Return exact model receipts; invasion is conditional on added eta."""
        eta = _nonnegative(coordination_penalty, "coordination_penalty")
        losses = {
            "SHARED": self.shared_loss,
            "PLASTIC": self.optimized_plastic_loss,
            "FIXED_MODULES": self.module_cost,
        }
        minimum = min(losses.values())
        tolerance = 1e-10 * max(1.0, max(losses.values()))
        best = sorted(k for k, value in losses.items() if abs(value - minimum) <= tolerance)
        best_nonmodule = min(losses["SHARED"], losses["PLASTIC"])
        intrinsic_margin = best_nonmodule - losses["FIXED_MODULES"]
        return {
            "schema": "PAYOFF_PLASTIC_COMPROMISE_MODULE_BOUNDARY_V1",
            "fitness_unit": "per-period log-fitness debit",
            "stationary_environment_flip_probability": self.rho,
            "cue_accuracy": self.q,
            "same_time_conflict_floor_C": self.unavoidable_simultaneous_conflict,
            "between_environment_loss_T": self.between_environment_compromise_loss,
            "observed_cue_flip_rate": self.cue_flip_probability,
            "optimal_plastic_amplitude": self.optimal_memoryless_amplitude,
            "losses": losses,
            "loss_minimizers": best,
            "intrinsic_module_vs_best_nonmodule_margin": intrinsic_margin,
            "hypothetical_rare_module_invasion_margin_given_eta": intrinsic_margin - eta,
            "assumed_coordination_penalty_eta": eta,
            "not_a_genotype_invasion_without_fitness_frequency_measurement": True,
            "not_a_historical_structural_origin_or_Wurmbea_fit": True,
        }


def analytic_turnover_crossover(params: PlasticCompromise) -> dict[str, Any]:
    """Where increasing rho reverses P vs D under the restricted policy.

    Exact interior only when P is strictly cheaper at rho=0 and the module
    is strictly cheaper at rho=1, and the module outperforms SHARED.
    This returns a boundary, not evidence of a real evolutionary switch.
    """
    inputs = {
        "a": params.a, "b": params.b, "delta": params.delta,
        "q": params.q, "plastic_running_cost": params.plastic_running_cost,
        "plastic_switch_cost": params.plastic_switch_cost,
        "module_cost": params.module_cost,
    }
    low = PlasticCompromise(rho=0.0, **inputs)
    high = PlasticCompromise(rho=1.0, **inputs)
    T = params.between_environment_compromise_loss
    d = params.trait_optimum_separation
    u = params.cue_reliability_signal
    k = params.plastic_switch_cost

    valid = (
        T > 0 and d > 0 and u > 0 and k > 0
        and params.module_cost < params.shared_loss
        and low.optimized_plastic_loss < params.module_cost
        and high.optimized_plastic_loss > params.module_cost
    )
    if not valid:
        return {
            "status": "NO_STRICT_INTERIOR_PLASTIC_TO_MODULE_CROSSOVER",
            "rho_crossing": None,
            "comparison": "restricted memoryless plastic versus fixed differentiated architecture",
        }
    gain_required = params.shared_loss + params.plastic_running_cost - params.module_cost
    alpha_required = sqrt(gain_required / T)
    h_required = (u - alpha_required) * 2.0 * T / (k * d)
    rho_cross = (h_required - 2 * params.q * (1 - params.q)) / (u*u)
    if not 0.0 < rho_cross < 1.0:
        raise ValueError("Interior crossover derivation escaped [0,1]; check numerical inputs")
    return {
        "status": "STRICT_INTERIOR_PLASTIC_TO_MODULE_CROSSOVER",
        "rho_crossing": rho_cross,
        "plastic_amplitude_at_crossing": alpha_required,
        "three_strategies_assessed": True,
        "source_status": "MATHEMATICAL_COUNTERFACTUAL_NOT_EMPIRICAL_TRANSITION",
    }



def analytic_overlap_crossover_perfect_cue(params: PlasticCompromise) -> dict[str, Any]:
    """Perfect-cue threshold in simultaneous weaker-function demand b.

    This is a *different parameter slice* from the turnover result:
    q=1, switching cost=0 and plastic running cost=0, so the memoryless
    response eliminates only T and retains C=ab/(a+b)*Delta^2.
    For fixed a, Delta and module cost K, unique b* solves C(b*)=K.
    Since the declared weights satisfy 0<b<=a, a strict interior switch
    requires 0<K<a*Delta^2/2.
    """
    exact_slice = (
        params.q == 1.0
        and params.plastic_running_cost == 0.0
        and params.plastic_switch_cost == 0.0
    )
    ceiling = params.a * params.delta**2 / 2.0
    if (
        not exact_slice
        or params.delta <= 0.0
        or params.module_cost <= 0.0
        or params.module_cost >= ceiling
    ):
        return {
            "status": "NO_QUALIFYING_PERFECT_CUE_INTERIOR_OVERLAP_CROSSOVER",
            "weaker_function_weight_crossing": None,
            "source_status": "MODEL_ONLY",
        }
    denom = params.a * params.delta**2 - params.module_cost
    b_star = params.module_cost * params.a / denom
    if not 0.0 < b_star < params.a:
        raise ValueError("Perfect-cue overlap threshold escaped positive b<a")
    return {
        "status": "STRICT_INTERIOR_SIMULTANEOUS_OVERLAP_CROSSOVER",
        "weaker_function_weight_crossing": b_star,
        "ecological_interpretation": (
            "Below b_star the plastic single coordinate is intrinsically "
            "best with perfect cues; above it separate coordinates beat "
            "the unavoidable simultaneous shared-coordinate conflict."
        ),
        "not_observed_evolutionary_structural_transition": True,
    }
