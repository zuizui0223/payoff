# PAYOFF-B Aikens pixel-year clustered support sensitivity

Frozen: 2026-09-22

Status: **pixel-year-correlated environmental-validity sensitivity frozen before lambda outcome**.

This analysis uses the same frozen fixed 24 h GPS targets as the canonical
pre-environment support ceiling and IID target-validity envelope.

It does not use MODIS values, reconstructed IRG, phase values, or lambda
outcomes.

## 1. Why this sensitivity was added

The exact IID target-validity envelope assumes that every selected target has an
independent probability p of obtaining valid environmental phase.

The frozen target geometry contains repeated use of the same MODIS pixel-year:

    large-development:
        1,114 targets
        910 unique pixel-years
        about 30.8% of targets belong to reused pixel-years

    small-development:
        4,596 targets
        3,400 unique pixel-years
        about 41.8% of targets belong to reused pixel-years.

Therefore target-level independence is not a realistic upper description of
all missingness dependence.

The present sensitivity instead assigns one Bernoulli validity state to each

    pixel_id x target_year

cluster. All frozen targets in the same pixel-year share that state.

Different pixel-years remain independent in this declared sensitivity model.

## 2. Frozen design

Fixed target source:

    artifact:
        10676913354

    artifact sha256:
        ab88ade2ec53c8f91b1a2099d58ad210ad57ab80d826375938c94bfe8689efa2

Registered final support threshold per development group:

    >=10 animals
    >=100 adjacent valid phase pairs.

Sensitivity grid:

    p =
        0.32
        0.33
        0.335
        0.34
        0.345
        0.35.

Monte Carlo:

    10,000 replicates per p
    base seed 20260922.

Total pixel-year clusters:

    4,304.

Support probabilities are reported with Wilson 95% intervals.

## 3. Result

### p = 0.32

Joint support probability:

    0.7975

95% interval:

    0.7895 .. 0.8053.

Large-development:

    support probability:
        0.7975

    mean valid adjacent pairs:
        111.5

    mean animals with valid pairs:
        32.74.

Small-development:

    support probability:
        1.0

    mean valid adjacent pairs:
        498.2

    mean animals with valid pairs:
        69.14.

### p = 0.33

Joint support probability:

    0.9031

95% interval:

    0.8971 .. 0.9087.

### p = 0.335

Joint support probability:

    0.9348

95% interval:

    0.9298 .. 0.9395.

This does not reach the 0.95 support target.

### p = 0.34

Joint support probability:

    0.9619

95% interval:

    0.9580 .. 0.9655.

Large-development:

    mean valid adjacent pairs:
        125.41

    mean animals with valid pairs:
        34.11.

Small-development:

    support probability:
        1.0

    mean valid adjacent pairs:
        558.56

    mean animals with valid pairs:
        71.13.

Thus the 95% joint-support transition is bracketed by

    0.335 < p* <= 0.34

under this pixel-year-clustered validity model.

### p = 0.345

Joint support probability:

    0.9786

95% interval:

    0.9756 .. 0.9813.

### p = 0.35

Joint support probability:

    0.9876

95% interval:

    0.9852 .. 0.9896.

## 4. Comparison with the exact IID target envelope

Exact IID target-level result:

    p_95
        = 0.34198.

Pixel-year clustered sensitivity:

    95% support transition
        between 0.335 and 0.34.

Therefore introducing the observed pixel-year sharing structure does **not**
move the support requirement into a qualitatively different coverage regime in
this declared model.

Both analyses place the transition near

    one-third environmental validity.

The reason is not that clustering is irrelevant. Under pixel-year clustering,
same-pixel-year adjacent edges have expected validity p rather than p^2, which
can increase the expected number of valid pairs. The present sensitivity is
therefore not automatically more conservative than IID target-level
missingness.

## 5. Interpretation

The combined outcome-blind support analysis now says:

1. the registered support gate is possible at full environmental coverage;
2. under exact IID target validity, approximately p=0.342 gives 95% joint
   support;
3. under a fixed-seed pixel-year-correlated sensitivity, the 95% transition
   remains near p=0.34;
4. the large-development group remains the limiting support unit.

This materially reduces concern that the registered Aikens test requires
near-complete environmental reconstruction.

It does not resolve actual AppEEARS / IRG coverage.

## 6. Why this is still only a sensitivity

The model assumes:

    independent pixel-years.

Real environmental reconstruction can exhibit broader dependence through:

- spatially neighboring MODIS pixels;
- repeated quality/snow states;
- shared dates;
- sensor/scene quality;
- population-specific geography;
- persistent problematic pixel-years.

Therefore this receipt does not replace the final observed support gate.

It only shows that one plausible correlated missingness unit does not destroy
the support feasibility established by the frozen target design.

## 7. Provenance

Workflow:

    payoff-b Aikens pixel-year clustered support

Run:

    35689632962

Head:

    b8a00eb30c502cf2e5802f8b473215a7b7dc611e

Artifact:

    10678357377

Artifact sha256:

    7e5722aee567a484ef1724476e06a77156f7973e512bfb3aa3e233d3ce96f38d.

## 8. Claim ceiling

Licensed:

- the 95% support transition under the declared pixel-year-clustered sensitivity
  is bracketed by p=0.335 and p=0.34;
- the large-development group remains support-limiting;
- the support transition remains close to the exact IID target-level result.

Not licensed:

- the true environmental-validity process is pixel-year independent;
- real AppEEARS / IRG coverage will exceed 34%;
- the registered lambda contrast will be estimable;
- any change to the frozen support threshold or target-selection contract.

The lambda outcome remains unopened.
