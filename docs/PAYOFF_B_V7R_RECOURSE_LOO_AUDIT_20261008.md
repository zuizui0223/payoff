# PAYOFF-B V7R — recourse-proxy individual-exclusion audit

Date: **2026-10-08**  
Status: **POST-OUTCOME SOURCE-ONLY DIAGNOSTIC; V7R PRIMARY UNCHANGED**

## Question

The original V7R retained recourse \(R\) was the range of possible arrival
times inferred from a **population envelope of observed stopover and transit
durations**. It used no spring-onset or phase-error values, but those durations
are still *behaviors from the same tagged population*. They are not measured
physiological capabilities.

Question: **Does the estimated remaining-route recourse survive when the
focal animal's own behavioral records are entirely excluded?**

This is a robustness check on the predictor's source support, **not** a new
test of the exposed \(Q\times R\) hypothesis.

## Source and exact frozen construction

Use the same 2026-09 Stage-3 ZIPs:

- Greenland / Barents: SHA256
  \`8e720be44e0ef2e3e497786c9241c6625b4b14c46506fbb30ea027dcdf36749f\`
- Svalbard: SHA256
  \`29558f9b8b43a7375b3922118a77b74464558f4869a7722472570a32745f2856\`

Retain the V7R rules:

- directed region graph;
- at least **3 transition records** to admit an edge;
- empirical **10–90% duration envelopes**;
- original terminal region for each flyway;
- remaining arrival-time window normalized by the initial-route window;
- the original **10 focal transition types**.

For each focal transition and each distinct tagged individual on that
transition, remove **all observations by that individual in the flyway**,
reconstruct the entire population route envelope, and inspect \(R\) at the
focal origin. Do not lower the 3-row gate when a path becomes unsupported.

Do not use \(Q\), \(\lambda\), \(\mathrm{phase\ error}\), or downstream outcomes
to choose the graph or compute \(R\).

## Source-only result

**70 of 76** individual-removal trials leave \(R\)
estimable; **6 of 76** do not.

All six non-estimable cases occur on Greenland focal transitions, because
removing an animal eliminates sufficient support for an edge needed to connect
to the breeding terminus.

| Flyway / focal transition | Individual-removals successful | Full \(R\) | Largest absolute change |
|---|---:|---:|---:|
| Barents R1→R2 | 8/8 | 1.000 | 0.000 |
| Barents R1→R5 | 6/6 | 1.000 | 0.000 |
| Barents R2→R3 | 4/4 | 0.440 | 0.099 |
| Barents R3→R5 | 4/4 | 0.287 | 0.053 |
| Barents R4→R5 | 6/6 | 0.144 | 0.027 |
| Barents R5→R7 | 3/3 | 0.122 | 0.042 |
| Greenland R1→R2 | 4/7 | 1.000 | 0.000 |
| Greenland R2→R3 | 3/6 | 0.631 | 0.120 |
| Svalbard R1→R2 | 17/17 | 1.000 | 0.000 |
| Svalbard R2→R4 | 15/15 | 0.175 | 0.086 |

Important: all first-stage \(R=1\) values remain 1 *by definition* whenever
the initial-stage route remains estimable. Their zero change is **not
independent evidence that the behavioral envelope is stable**.

For the interior Greenland R2→R3 proxy, removing different animals yields
values from about **0.570 to 0.752** where the route still exists, compared
with the full-sample 0.631. The largest absolute difference is about 0.120.

## Interpretation and boundary

1. The source-derived \(R\) is feasible to compute at most route stages but
   depends on which individuals happen to have been tracked.
2. For Greenland, some individual exclusions remove the entire admissible
   route to the terminal; no numerical recourse estimate is then licensed.
3. Even among successful exclusions, population-duration envelopes mix
   the animals' **choices** with their genuinely **feasible** movement and
   stopping options.
4. The \(Q\times R\) interaction remains non-supported:
   \(\widehat\beta_{QR}=1.3733\), one-sided enumerated \(p=0.56994\).
5. This diagnostic does not identify environmental cue use, feedback gain,
   body condition, fitness, or a causal constraint on recourse.

## What must change in the next confirmatory study

For \(r(t)\), prefer an independently defined feasible **action set**:
reachable downstream sites and stage-specific maximum correction time
derived from geometry, migration biomechanics, and physically imposed
constraints **before observing the focal animal's response**.

For \(q_B(t)\), measure the reliability of *actual checkpoint-local cues*,
rather than treating historical between-site correlation \(q_F\) as if it
were knowledge of the bird's current phase mismatch.

Record, before analysis, which portion of correction capacity is:

- physical possibility;
- required travel time;
- optional waiting/stopping time;
- local environmental information;
- an observed behavioral decision.

This is a **prospective measurement requirement**, not a post-hoc route for
reinterpreting the exposed V7R outcomes.

## Reproducibility

- \`src/v7r_recourse_loo.py\`
- \`scripts/audit_v7r_recourse_loo.py\`
- \`tests/test_v7r_recourse_loo.py\`
- \`data/payoff_b_v7r_recourse_loo_diagnostic_20261008.json\`

The canonical V7R contracts, opened result, and previously archived
sensitivity receipts are **unchanged**.
