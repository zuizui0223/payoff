"""Finite-N stochastic escape from two-species tracking coordination barriers.

The deterministic coevolution model accepts only strictly improving unilateral
mutations. Here each species is a finite monomorphic population between
mutation events. One-step mutants can therefore fix stochastically according to
the constant-fitness Moran probability, including mildly deleterious steps.

The main diagnostic asks whether finite-N drift can move an interacting pair
from the deterministic local endpoint into states with joint payoff closer to
the coordinated matched optimum.
"""

from __future__ import annotations

from dataclasses import dataclass
from random import Random
from statistics import mean

from src.spatiotemporal_tracking import TrackingStrategy
from src.tracking_coevolution import (
    CoevolutionScenario,
    coevolve_tracking_pair,
    optimize_matched_pair,
    simulate_coevolving_pair,
)
from src.tracking_finite_evolution import (
    moran_fixation_probability_from_growth_difference,
)
from src.tracking_mutation_selection import StrategyLattice


PairState = tuple[int, int]


@dataclass(frozen=True)
class PairGrowthLandscape:
    lattice: StrategyLattice
    growth_a: tuple[tuple[float, ...], ...]
    growth_b: tuple[tuple[float, ...], ...]
    local_state: PairState
    matched_state: PairState
    local_joint_growth: float
    matched_joint_growth: float

    @property
    def accessibility_gap(self) -> float:
        return max(
            0.0,
            self.matched_joint_growth - self.local_joint_growth,
        )


@dataclass(frozen=True)
class FiniteCoevolutionResult:
    population_size_a: int
    population_size_b: int
    selection_strength: float
    state_path: tuple[PairState, ...]
    accepted_a: int
    accepted_b: int
    local_state: PairState
    matched_state: PairState
    local_joint_growth: float
    matched_joint_growth: float
    high_payoff_threshold: float
    evolutionary_burn_in: int
    growth_a: tuple[tuple[float, ...], ...]
    growth_b: tuple[tuple[float, ...], ...]

    def _joint_growth(self, state: PairState) -> float:
        a, b = state
        return 0.5 * (
            self.growth_a[a][b]
            + self.growth_b[a][b]
        )

    def summary(self) -> dict[str, float | int]:
        tail = self.state_path[self.evolutionary_burn_in :]
        if not tail:
            raise ValueError("evolutionary burn-in removes all states")
        matched_fraction = (
            sum(state == self.matched_state for state in tail)
            / len(tail)
        )
        local_fraction = (
            sum(state == self.local_state for state in tail)
            / len(tail)
        )
        high_fraction = (
            sum(
                self._joint_growth(state)
                >= self.high_payoff_threshold
                for state in tail
            )
            / len(tail)
        )
        mean_joint = mean(
            self._joint_growth(state)
            for state in tail
        )
        return {
            "population_size_a": self.population_size_a,
            "population_size_b": self.population_size_b,
            "selection_strength": self.selection_strength,
            "accepted_a": self.accepted_a,
            "accepted_b": self.accepted_b,
            "matched_optimum_fraction": matched_fraction,
            "local_endpoint_fraction": local_fraction,
            "high_payoff_fraction": high_fraction,
            "mean_joint_growth": mean_joint,
            "local_joint_growth": self.local_joint_growth,
            "matched_joint_growth": self.matched_joint_growth,
            "accessibility_gap": max(
                0.0,
                self.matched_joint_growth
                - self.local_joint_growth,
            ),
        }


@dataclass(frozen=True)
class FiniteCoevolutionEnsemble:
    replicates: tuple[FiniteCoevolutionResult, ...]

    def summary(self) -> dict[str, float | int]:
        rows = [row.summary() for row in self.replicates]
        return {
            "replicates": len(rows),
            "population_size": rows[0]["population_size_a"],
            "selection_strength": rows[0]["selection_strength"],
            "mean_matched_optimum_fraction": mean(
                float(row["matched_optimum_fraction"])
                for row in rows
            ),
            "mean_local_endpoint_fraction": mean(
                float(row["local_endpoint_fraction"])
                for row in rows
            ),
            "mean_high_payoff_fraction": mean(
                float(row["high_payoff_fraction"])
                for row in rows
            ),
            "mean_joint_growth": mean(
                float(row["mean_joint_growth"])
                for row in rows
            ),
            "escape_replicate_fraction": mean(
                float(row["high_payoff_fraction"]) > 0.0
                for row in rows
            ),
            "accessibility_gap": rows[0]["accessibility_gap"],
        }


def _strategy_index(
    strategy: TrackingStrategy,
    lattice: StrategyLattice,
) -> int:
    i = int(round(strategy.migration_rate / lattice.step))
    j = int(round(strategy.phenology_rate / lattice.step))
    candidate = lattice.strategy(i, j)
    if (
        abs(candidate.migration_rate - strategy.migration_rate) > 1e-9
        or abs(candidate.phenology_rate - strategy.phenology_rate) > 1e-9
    ):
        raise ValueError("strategy is not aligned to lattice")
    return lattice.index(i, j)


def _proposal(
    index: int,
    lattice: StrategyLattice,
    rng: Random,
) -> int:
    """Symmetric eight-direction proposal with boundary self-loops."""

    i, j = lattice.coordinate(index)
    directions = (
        (-1, -1),
        (-1, 0),
        (-1, 1),
        (0, -1),
        (0, 1),
        (1, -1),
        (1, 0),
        (1, 1),
    )
    di, dj = directions[rng.randrange(len(directions))]
    ii = i + di
    jj = j + dj
    if not (0 <= ii < lattice.points and 0 <= jj < lattice.points):
        return index
    return lattice.index(ii, jj)


def build_pair_growth_landscape(
    scenario: CoevolutionScenario,
    lattice: StrategyLattice,
) -> PairGrowthLandscape:
    """Precompute all pair payoffs and deterministic reference states."""

    strategies = lattice.strategies()
    size = lattice.size
    growth_a = [[0.0] * size for _ in range(size)]
    growth_b = [[0.0] * size for _ in range(size)]

    for a_index, strategy_a in enumerate(strategies):
        for b_index, strategy_b in enumerate(strategies):
            result = simulate_coevolving_pair(
                strategy_a,
                strategy_b,
                scenario,
            )
            growth_a[a_index][b_index] = result.mean_log_growth_a
            growth_b[a_index][b_index] = result.mean_log_growth_b

    local = coevolve_tracking_pair(
        scenario,
        mutation_step=lattice.step,
        max_rate=lattice.max_rate,
        max_cycles=100,
    ).final
    matched = optimize_matched_pair(
        scenario,
        max_rate=lattice.max_rate,
        points=lattice.points,
    )
    local_state = (
        _strategy_index(local.strategy_a, lattice),
        _strategy_index(local.strategy_b, lattice),
    )
    matched_index = _strategy_index(
        matched.strategy_a,
        lattice,
    )
    matched_state = (matched_index, matched_index)

    local_joint = 0.5 * (
        local.mean_log_growth_a + local.mean_log_growth_b
    )
    matched_joint = 0.5 * (
        matched.mean_log_growth_a + matched.mean_log_growth_b
    )

    return PairGrowthLandscape(
        lattice=lattice,
        growth_a=tuple(tuple(row) for row in growth_a),
        growth_b=tuple(tuple(row) for row in growth_b),
        local_state=local_state,
        matched_state=matched_state,
        local_joint_growth=local_joint,
        matched_joint_growth=matched_joint,
    )


def simulate_finite_coevolution_escape(
    landscape: PairGrowthLandscape,
    *,
    population_size_a: int = 100,
    population_size_b: int | None = None,
    selection_strength: float = 10.0,
    mutation_events: int = 20_000,
    evolutionary_burn_in: int = 2_000,
    seed: int = 20260920,
    high_payoff_fraction_of_gap: float = 0.5,
) -> FiniteCoevolutionResult:
    """Simulate stochastic substitutions starting at deterministic local state."""

    if population_size_b is None:
        population_size_b = population_size_a
    if population_size_a < 2 or population_size_b < 2:
        raise ValueError("population sizes must be at least 2")
    if selection_strength < 0.0:
        raise ValueError("selection_strength must be non-negative")
    if mutation_events <= 0:
        raise ValueError("mutation_events must be positive")
    if not 0 <= evolutionary_burn_in < mutation_events + 1:
        raise ValueError("invalid evolutionary_burn_in")
    if not 0.0 <= high_payoff_fraction_of_gap <= 1.0:
        raise ValueError(
            "high_payoff_fraction_of_gap must lie in [0,1]"
        )

    rng = Random(seed)
    a_index, b_index = landscape.local_state
    path: list[PairState] = [(a_index, b_index)]
    accepted_a = 0
    accepted_b = 0

    for _ in range(mutation_events):
        mutate_a = rng.random() < 0.5
        if mutate_a:
            mutant = _proposal(
                a_index,
                landscape.lattice,
                rng,
            )
            if mutant != a_index:
                delta = (
                    landscape.growth_a[mutant][b_index]
                    - landscape.growth_a[a_index][b_index]
                )
                fixation = (
                    moran_fixation_probability_from_growth_difference(
                        delta,
                        population_size_a,
                        selection_strength,
                    )
                )
                if rng.random() < fixation:
                    a_index = mutant
                    accepted_a += 1
        else:
            mutant = _proposal(
                b_index,
                landscape.lattice,
                rng,
            )
            if mutant != b_index:
                delta = (
                    landscape.growth_b[a_index][mutant]
                    - landscape.growth_b[a_index][b_index]
                )
                fixation = (
                    moran_fixation_probability_from_growth_difference(
                        delta,
                        population_size_b,
                        selection_strength,
                    )
                )
                if rng.random() < fixation:
                    b_index = mutant
                    accepted_b += 1
        path.append((a_index, b_index))

    threshold = (
        landscape.local_joint_growth
        + high_payoff_fraction_of_gap
        * landscape.accessibility_gap
    )
    return FiniteCoevolutionResult(
        population_size_a=population_size_a,
        population_size_b=population_size_b,
        selection_strength=selection_strength,
        state_path=tuple(path),
        accepted_a=accepted_a,
        accepted_b=accepted_b,
        local_state=landscape.local_state,
        matched_state=landscape.matched_state,
        local_joint_growth=landscape.local_joint_growth,
        matched_joint_growth=landscape.matched_joint_growth,
        high_payoff_threshold=threshold,
        evolutionary_burn_in=evolutionary_burn_in,
        growth_a=landscape.growth_a,
        growth_b=landscape.growth_b,
    )


def finite_coevolution_escape_ensemble(
    landscape: PairGrowthLandscape,
    *,
    population_size: int,
    selection_strength: float,
    mutation_events: int,
    evolutionary_burn_in: int,
    replicates: int,
    seed: int,
) -> FiniteCoevolutionEnsemble:
    if replicates <= 0:
        raise ValueError("replicates must be positive")
    rows = tuple(
        simulate_finite_coevolution_escape(
            landscape,
            population_size_a=population_size,
            population_size_b=population_size,
            selection_strength=selection_strength,
            mutation_events=mutation_events,
            evolutionary_burn_in=evolutionary_burn_in,
            seed=seed + replicate * 1_000_003,
        )
        for replicate in range(replicates)
    )
    return FiniteCoevolutionEnsemble(replicates=rows)
