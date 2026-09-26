# PAYOFF-B long-term cue–driver decoupling contract

Frozen: **2026-09-27**

## Why this is a separate lane

Tomotani et al. (2021) already proposed that climate change may have disrupted
the predictive value of environmental cues used by pied flycatchers. PAYOFF-B
therefore does not claim cue–driver decoupling as a new idea.

The new question is narrower: can the longer 1980–2010 Hoge Veluwe fitness
series show a **time-varying** relationship between a biologically prior African
cue and the annual selective driver, without using the known nonlinear selection
trajectory to define the information regimes?

## Driver

The primary annual driver is the standardized directional selection gradient on
egg-laying date using number of local recruits, matching Visser et al. (2015).
The source paper estimated these annually with Poisson models and used linear-only
models in 1981, 1989, 1990, 1991 and 2006 because recruit counts were low.

The published fact that selection intensified through roughly 2000 and weakened
afterwards is **not** used to choose a breakpoint.

## Cue

The primary cue is the Ivory Coast temperature signal defined independently by
the migration-cue study of Tomotani et al. (2021). Their strongest lagged
temperature window was a 20-day window shifted about 60 days before the arrival
risk date.

If this annual cue cannot be reconstructed without using individual arrival
dates or outcome-tuned choices, the lane is marked NOT_ESTIMABLE. No new climate
window will be selected from its correlation with selection.

## Information history

For each year t, predictive connectivity is estimated only from the previous
eight years. Cue and annual selection-gradient series are detrended separately
within the window before their signed correlation is calculated.

A single degradation/recovery breakpoint may be declared only from this
connectivity series. A segmented fit must beat a single trend by AICc >= 4,
the two slopes must have opposite signs, and at least half of the decline must
be recovered by the series endpoint.

If that gate fails, the result is NO_CUE_DRIVER_REVERSAL and no path-dependence
model is fitted.

## Claim ceiling

Even a supported result would be a within-population cue–driver history result,
not evidence that an interaction network stores ecological memory. The full
network-hysteresis claim remains prospective.
