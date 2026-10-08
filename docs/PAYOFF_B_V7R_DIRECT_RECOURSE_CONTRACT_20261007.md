# PAYOFF-B V7R prospective contract — direct recourse × environmental predictability

Date: **2026-10-07**  
Status: **PREOUTCOME FOR THE NEW Q×R COMBINATION**

This route does not alter the frozen V7 predictability × geometry-urgency
contract or any frozen PAYOFF-B manuscript.

## 1. Question

The competitive-information audit exposed an identification problem:

    observed usable information
        = information quality
        × retained usability.

A timing pattern alone cannot show that usability declined because biological
recourse was lost.

V7R therefore asks a stronger ecological question:

> **Across migration transitions, is phase correction strongest where
> independently estimated environmental predictability and independently
> estimated remaining temporal recourse are both high?**

## 2. Fixed source objects

Use the already frozen Stage-3 barnacle-goose artifacts from the three
Kölzsch et al. flyways.

Movement / transition artifacts are pre-existing PAYOFF-B outputs. Their
transition-specific phase-retention slopes have already been exposed in prior
work; the new unopened outcome is the **cross-transition relationship between
those slopes and the newly defined direct-recourse coordinate**.

Environmental predictability is reconstructed independently from the
historical spring-onset series and does not use goose timing.

## 3. Environmental information coordinate Q

For transition e from region j to k, primary information strength is

    Q_e = abs(corr(S_j,y, S_k,y)),

where S is the 30-year spring-onset anomaly series.

Q is in [0,1].

The absolute value is used because this route treats predictability as
information strength: a stable inverse relation is still predictive if its
direction is known.

Mandatory sensitivities:

1. signed Pearson correlation r;
2. r^2;
3. proportionality / slope-based coordinate where available;
4. ERA5-reconstructed predictability where the frozen source exists.

## 4. Direct recourse coordinate R

### 4.1 Edge duration

For every observed route transition j -> k, define

    D_jk
      =
    origin stopover duration
      +
    transit duration to k.

D uses movement timing only. It does **not** use spring onset, phase error,
phenology predictability, or phase-retention lambda.

### 4.2 Route graph

Within each flyway:

- use directed region transitions that progress toward the breeding region;
- an edge enters the recourse graph only when it has at least 3 observed
  transition rows;
- terminal breeding nodes are fixed before outcome combination:
  - Greenland R4
  - Svalbard R4
  - Barents Sea R7.

For each admitted edge, define empirical duration bounds

    d^-_jk = Q10(D_jk)
    d^+_jk = Q90(D_jk).

These are empirical population envelopes, not physiological hard limits.

### 4.3 Remaining arrival window

At terminal node b:

    E_b = 0
    L_b = 0.

For any upstream region j:

    E_j
      =
    min_{j->k}
    [d^-_jk + E_k],

    L_j
      =
    max_{j->k}
    [d^+_jk + L_k].

Thus route choice itself contributes to remaining recourse when multiple
downstream paths are observed.

Define the remaining temporal window

    W_j = L_j - E_j.

Normalize within flyway by the initial-route window:

    R_j = W_j / W_start.

Therefore:

    0 <= R_j <= 1,

and the breeding terminal has R=0.

R is a **population-envelope actionability proxy**. It is not claimed to be an
individual physiological capacity or the exact theoretical r(t).

## 5. Primary transition admission

A focal transition must have:

1. at least 5 observed transition rows;
2. at least 3 distinct individuals where possible; if exactly 3, retain but
   flag as LOW_INDIVIDUAL_SUPPORT;
3. an independently estimated Q value;
4. a finite R value at its origin;
5. an existing or reproducible fixed-transition phase-retention slope.

The source-only precheck currently yields exactly 10 transition types:

Greenland:
- R1 -> R2
- R2 -> R3

Svalbard:
- R1 -> R2
- R2 -> R4

Barents Sea:
- R1 -> R2
- R1 -> R5
- R2 -> R3
- R3 -> R5
- R4 -> R5
- R5 -> R7

No transition is added after the Q×R outcome is opened.

## 6. Primary response

For each admitted transition e, fit or recover

    E_destination
      =
    a_e + lambda_e E_origin + error.

Only the within-transition slope matters; arbitrary region-specific phase
offsets are absorbed by a_e.

Define correction score

    C_e = 1 - abs(lambda_e).

Interpretation:

- C=1: zero phase retention;
- C=0: magnitude preserved;
- C<0: amplification / overshoot in absolute phase magnitude.

This definition does not reinterpret negative lambda as automatically
beneficial.

## 7. Primary meta-model

Transition is the unit of analysis.

Fit the unweighted model

    C_e
      =
    alpha_flyway
      + beta_Q Q_e
      + beta_R R_e
      + beta_QR Q_e R_e
      + epsilon_e.

The focal coefficient is

    beta_QR.

Directional PAYOFF prediction:

    beta_QR > 0.

Interpretation:

> Predictive environmental information is associated with stronger phase
> correction when more downstream temporal recourse remains.

## 8. Primary inference

Because only 10 transition types are expected, asymptotic row-level inference
is not primary.

Use an exact within-flyway permutation test:

- hold C and R fixed;
- permute Q labels only among transitions within the same flyway;
- refit the same flyway-fixed-effect model;
- enumerate all unique permutations.

With 2 Greenland, 2 Svalbard and 6 Barents transitions, the maximum complete
permutation space is

    2! × 2! × 6! = 2880.

Primary one-sided P value:

    p_perm
      =
    (1 + count(beta_QR_perm >= beta_QR_obs))
    / (1 + N_perm).

Report the full permutation distribution and the observed rank.

## 9. Mandatory sensitivities

1. weighted meta-regression using transition n;
2. leave-one-transition-out beta_QR;
3. Q20-Q80 instead of Q10-Q90 duration envelopes;
4. local one-step duration-window width instead of remaining-route window;
5. signed phenology r instead of abs(r);
6. r^2;
7. exclude LOW_INDIVIDUAL_SUPPORT transitions;
8. use lambda rather than 1-|lambda| as a descriptive secondary endpoint;
9. ERA5 Q where available;
10. rebuild lambda from row-level transition pairs and verify identity with
    frozen Stage-3 lambda where an existing receipt is available.

No sensitivity can replace the primary result.

## 10. Admission gate before outcome combination

Proceed only if all are true:

- >= 10 admitted focal transitions;
- all three flyways represented;
- Q and R correlation across focal transitions satisfies |corr(Q,R)| < 0.90;
- every flyway has a valid route from its admitted upstream nodes to the fixed
  terminal under the >=3-row graph rule;
- no phase or lambda value was used to construct Q or R.

If any gate fails:

    V7R_PRIMARY = NOT_ESTIMABLE.

Source-only precheck before the Q×R outcome is opened:

    focal transitions = 10
    corr(Q,R) approximately -0.16 using signed r
    all three flyways represented

The exact primary abs(r) correlation is computed and frozen in the source
receipt before lambda is joined.

## 11. Claim ceiling

If beta_QR is positive and permutation-supported, safe claim:

> Across ten barnacle-goose migration transitions, phase correction was
> strongest where independently reconstructed environmental predictability and
> independently reconstructed remaining temporal recourse were jointly high.

Not licensed:

- birds consciously calculate Q or R;
- R is exact physiological capacity;
- causal manipulation of recourse;
- universal migration optimal-stopping theory;
- fitness benefit;
- horse-racing evidence as biological validation.

## 12. Stop rule

This route is intended to answer the recourse-identification problem exposed by
the competitive-information boundary case.

Do not add more taxa or tune graph thresholds after opening beta_QR.
