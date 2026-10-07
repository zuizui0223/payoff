# PAYOFF-B racing data contract

Date: **2026-10-07**  
Status: **primary-analysis contract before racing outcome access**

The primary racing mechanism-separation analysis consumes one long-format row
per race × horse × time slice.

Required columns:

| column | meaning |
|---|---|
| split | `train` or `test` |
| race_id | stable race identifier |
| horse_id | stable runner identifier within race |
| time_slice | frozen slice label such as `T-60` or `LAST` |
| decimal_odds | contemporaneous displayed win odds |
| form_probability | frozen public win probability; primary source is training-calibrated JRA-VAN previous-day TM score |
| winner | 1 for official winner, 0 otherwise |

Primary analysis fails closed unless all of the following hold:

1. train and test race ids are disjoint;
2. runner sets do not change across included time slices;
3. the frozen form probability does not change across time slices;
4. the winner flag does not change across time slices;
5. every race in a split has the same complete time-slice panel;
6. train and test contain the same set of time slices.

These rules intentionally exclude late-scratch / field-change races from the
primary pure information-diffusion comparison. Such races can later form a
separate actionability-change analysis.

The market probability at each slice is constructed as

[
m_i(t)
=
rac{1/O_i(t)}{sum_j 1/O_j(t)}.
]

The frozen form forecast and market forecast are combined only after the above
invariants pass.

This contract does **not** establish the provenance of `form_probability`.
The upstream form-model pipeline must separately prove that no contemporaneous
or future odds, result, or post-cutoff covariate entered that model.


## Primary upstream provenance

For the primary route, `form_probability` must be derived from the JRA-VAN
head-to-head data-mining record (TM) with:

    data category = 1  (previous-day forecast)

The raw 0--100 predicted score is converted to a probability by:

1. within-race standardization;
2. a single global softmax scale fitted on training races only;
3. freezing the resulting transformation before test evaluation.

Implementation:

    src/racing_public_score_calibration.py

A TM record with data category 2 (same-day forecast) or 3 (pre-race forecast)
must not be substituted for the primary fixed forecast because doing so moves
the information cutoff and contaminates the market-absorption time comparison.
