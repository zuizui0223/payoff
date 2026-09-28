# PAYOFF-B Hoge Veluwe Gate-B result

Date: **2026-09-28**  
Status: **NO_CUE_RESOURCE_REVERSAL — Gate C permanently closed for this lane**

The preregistered environmental-information gate was opened only after the cue
and caterpillar-resource sources had been frozen independently.

## Frozen result

```text
history years       = 1992–2015
connectivity rows   = 24
window              = trailing 8 years, current year excluded
minimum pairs       = 6

best breakpoint     = 1999
linear AICc         = -48.968
segmented AICc      = -59.780
delta AICc          = +10.812 in favour of segmented

pre-break slope     = +0.22790
post-break slope    = +0.02693
registered geometry = FAIL
status              = NO_CUE_RESOURCE_REVERSAL
```

The segmented form fits the time series better than one straight line, but this
is **not** the registered information-loss → information-recovery geometry.
Both fitted slopes are positive. The required pre-break decline is absent, so
the recovery fraction is undefined.

Selected frozen connectivity values illustrate the actual trajectory:

```text
1992  rho = -0.530
1998  rho = +0.703
1999  rho = +0.160
2004  rho = -0.314
2015  rho = +0.413
```

The series is non-monotone, but non-monotonicity alone was explicitly forbidden
from being relabelled as recovery hysteresis.

## Consequence

The registered causal sequence stops here:

```text
Gate A environmental sources = PASS
Gate B decline→recovery       = FAIL
Gate C history test           = NOT RUN
```

Therefore the Marine Data Archive access blocker is no longer relevant to this
registered hypothesis. There is no licensed recovered-information branch on
which a resident–migrant history comparison can be made, so obtaining
flycatcher timing cannot rescue this lane.

## Firewall

During Gate B:

- cue data were opened;
- caterpillar resource data were opened;
- great-tit timing was **not** opened;
- pied-flycatcher timing was **not** opened;
- resident–migrant mismatch was **not** computed;
- Gate C was **not** run.

## Provenance

- workflow run: `36368451182`;
- workflow head: `f8f968d627a01f8545c9a376d224be81f154db41`;
- artifact: `10947973142`;
- artifact SHA256:
  `24d5deab09532151745c0a217dbc3a575918a7f69131fcccb8151d716943a787`;
- connectivity CSV SHA256:
  `36cef859c759599d9a2bc6254e86e2e19b9081be18e29e125ce095cadeafae62`;
- paired annual input SHA256:
  `ced64102567054326f77ff32628c97f0266e6d759257fe1c38fb21cc57c78f6c`.

## Paper-level interpretation

This strengthens the empirical claim ceiling rather than the natural-hysteresis
claim. The current data support separate components of the information-
coordination mechanism, but this strongest same-system prospective assembly did
**not** produce the prerequisite environmental degradation–recovery episode.

The theoretical results on coordination memory and information-seed rescue
therefore remain prospective predictions for natural interaction networks.
