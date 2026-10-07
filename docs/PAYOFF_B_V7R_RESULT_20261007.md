# PAYOFF-B V7R result — direct recourse × predictability

Date: **2026-10-07**  
Status: **PRIMARY OPENED — NULL**

## Primary result

The frozen model was

[
C_e
=
alpha_{m flyway}
+
eta_Q Q_e
+
eta_R R_e
+
eta_{QR} Q_eR_e
+
epsilon_e,
]

with

[
C_e=1-|lambda_e|.
]

The directional prediction was

[
eta_{QR}>0.
]

Observed:

[
hateta_{QR}=1.37334.
]

The sign is positive, but the exact within-flyway permutation result is

[
p_{m perm}=0.56994
]

from all **2880/2880 valid permutations**.

Therefore:

[
oxed{	ext{V7R primary prediction not supported.}}
]

## Outcome audit

Nine of the ten focal transitions already had Stage-3 controller lambda values.
Recomputing the same within-transition OLS slope from row-level phase pairs
reproduced all nine to machine precision.

Maximum absolute discrepancy:

[
5.6	imes10^{-17}.
]

The tenth transition, Barents R5→R7, had no prior controller row and was opened
with the same slope definition:

[
lambda_{R5	o R7}=0.832858.
]

## Why the positive coefficient is not suggestive evidence

The permutation distribution of (eta_{QR}) had:

- minimum: −1.669
- median: **1.633**
- maximum: 10.424

The observed coefficient, 1.373, is actually below the permutation median.

Thus a positive interaction coefficient is common under within-flyway
relabeling of environmental predictability.

The direct descriptive association is also weak:

[
mathrm{corr}(Q_eR_e,C_e)=0.111
]

across all ten transitions, and only

[
0.006
]

within the six Barents transitions.

This is not an “almost significant” pattern.

## Prespecified sensitivities completed

| Analysis | beta_QR | exact permutation p |
|---|---:|---:|
| Primary | 1.373 | 0.570 |
| weighted by transition n | 0.906 | 0.656 |
| signed phenology r | 1.371 | 0.570 |
| phenology r² | 1.088 | 0.607 |
| exclude Barents R5→R7 low-individual-support row | 1.436 | 0.549 |
| recourse envelope Q20–Q80 | 1.151 | 0.530 |
| lambda endpoint, descriptive | 0.008 | 0.568 |

Leave-one-transition-out inference also remained unsupported. The smallest LOO
permutation p was 0.121 after removing Barents R1→R2.

## Interpretation

The current data do **not** support the simple transition-level prediction:

> independently high environmental predictability and a broad remaining
> temporal route window jointly produce stronger phase correction.

This does not refute PAYOFF-B's general information/actionability distinction.

It does reject one concrete operationalization:

- (Q): historical spring-onset predictability;
- (R): population-envelope remaining arrival-time window;
- response: transition-level phase-retention correction.

## Biological implication

A broad remaining route-time window is apparently not enough to identify the
recourse that animals actually use.

That is informative because the competitive-information audit had already shown
that usable information cannot be decomposed from timing trajectories alone.
V7R attempted an independent movement-based recourse proxy, but the proxy does
not explain cross-transition phase correction in the predicted way.

The next useful move should therefore be **actuator-specific**, not another
generic route-position proxy.

Candidate direct actionability quantities are:

- capacity to shorten the *current* stopover if late;
- capacity to extend the current stopover if early;
- attainable movement-speed increase on the immediately following segment;
- route alternatives that are actually available from the current state.

These are direction-specific. A symmetric remaining-window (R) may average
together biologically different “speed up” and “slow down” capacities.

## Claim boundary

Safe:

> A preregistered transition-level test using independently reconstructed
> environmental predictability and a population-envelope route-time recourse
> proxy did not detect the predicted interaction across ten barnacle-goose
> transitions.

Safe:

> The null was stable to transition weighting, alternative predictability
> coordinates, removal of the lowest-individual-support transition, and a
> narrower recourse envelope.

Not licensed:

- recourse does not matter;
- environmental information does not matter;
- the PAYOFF information/actionability idea is false;
- the route-window proxy is direct physiological actionability.

## Stop rule

Do not tune the remaining-window definition further to rescue V7R.

Any next analysis must change the biological estimand from **symmetric route
window** to a separately motivated **direction-specific actuator capacity**,
and it must be labeled as a new route rather than a sensitivity of V7R.
