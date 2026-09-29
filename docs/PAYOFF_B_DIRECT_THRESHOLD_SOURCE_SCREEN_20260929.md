# PAYOFF-B source screen for a direct natural deadline-threshold test

Date: **2026-09-29**  
Status: **screen complete; no located source currently satisfies the full direct-test contract**

## Qualification target

A direct natural test of the pairwise information-deadline mechanism requires all of the following in the same system:

| quantity | required role |
|---|---|
| pre-commitment cue reliability q | environmental information quality |
| effective delay/opportunity cost D_eff,i | independent fitness cost of postponing commitment after optimal feasible compensation |
| C_F, C_M, pi or equivalent state-loss scale | converts D_i to predicted q_i |
| observed cue use | distinguishes commit-now from wait/use-cue |
| repeated q support | must cross below, within and above the predicted asynchronous window |

## Candidate 1 — Greater snow goose same-system perturbation-cost + q composite

Grandmont et al. (2023), *Functional Ecology*  
DOI: 10.1111/1365-2435.14256  
Dryad: 10.5061/dryad.cjsxksn6t

Reséndiz-Infante & Gauthier (2024), *Frontiers in Bird Science*  
DOI: 10.3389/fbirs.2024.1307628

This is currently the closest located same-system route because both studies
concern the greater snow goose migration from the St. Lawrence spring staging
area toward the Bylot Island breeding system.

### Independent perturbation-cost evidence

Grandmont et al. experimentally held female greater snow geese during spring
migration for up to 4 days before release. Increasing time in captivity reduced
breeding propensity / reproductive output, with strong reductions in two of
three study years. This is substantially closer to the theorem's deadline-cost axis than migration
distance or route progress because perturbation duration itself was experimentally
manipulated before reproduction. However, captivity combines elapsed time with
capture, handling and confinement stress, and the source authors interpret the
carry-over effect as a stress-inducing perturbation.

The experiment therefore provides an **independent D-like perturbation-cost
anchor**, not a clean measurement of the PAYOFF-B opportunity cost D. It must
not be inserted into the exact q_wait formula as if pure waiting time had been
isolated.

### Independent q-like information evidence

Reséndiz-Infante & Gauthier reconstructed temperatures along the same migration
system from the St. Lawrence Valley through Nunavik and Baffin Island to Bylot
Island over 1979-2018. Temperature correlations between successive locations
were generally weak at long distances and increased only near the breeding
site. Temperature during the Bylot arrival/pre-laying period predicted laying
date, whereas temperatures at southern stopovers did not provide a strong
breeding-site predictor.

This supplies a source-backed **pre-commitment information-quality gradient**
along the same ecological system.

### Independent compensation evidence

Bêty, Giroux & Gauthier (2004; DOI 10.1007/s00265-004-0840-3)
radio-tracked female greater snow geese between southern Quebec and Bylot
Island. Across all females, later departure was associated with shorter
migration duration (Spearman r = -0.35), departure and arrival date were only
weakly related (r = 0.14), and migration duration strongly tracked arrival
(r = 0.81).

This means raw departure delay cannot be substituted for the theorem's waiting
cost. The relevant quantity is the fitness loss that remains after feasible
downstream compensation:

[
D_{eff}=\min_c[K(c)+M(\delta-c)].
]

The tracking study demonstrates the existence of compensation-like timing
adjustment but does **not** identify (C), (K), (M), or numerical
(D_{eff}).


### Why this still does not close the theorem empirically

The 2024 study explicitly notes that individual migration chronology linked to
subsequent reproductive performance exists only for few years and few
individuals. The two source programmes therefore do not currently provide a
dense actor-level series in which the same individuals experience measured q,
an independently calibrated D_eff, and repeated cue-use decisions spanning a switch
threshold.

Qualification:

- same species and migration/breeding system: **YES**
- independently manipulated perturbation duration: **YES**
- fitness consequence of perturbation duration: **YES**
- q-like environmental predictability: **YES**
- downstream compensation evidence: **YES**
- independent exact D_eff in PAYOFF-B loss units: **NOT YET**
- actor-level cue-use threshold: **NO**
- repeated q support crossing q1 and q2: **NO**
- direct asynchronous-use window: **NO**

Classification: **STRONGEST_COMPOSITE_D_LIKE_AND_Q_CANDIDATE_NOT_DIRECT_THRESHOLD**

This candidate upgrades the source screen materially: the earlier problem was
that no promising q system had an independent delay-cost anchor. Greater snow
goose supplies a D-like perturbation axis and q-like predictability in one
ecological lineage. The remaining bottlenecks are **clean effective information-waiting D_eff identification after compensation**, **a prespecified mapping of the continuous two-sided fitness surface to binary C_F/C_M**, and **actor-level threshold identification**.

### Independent two-sided fitness-loss anchor

Reséndiz-Infante & Gauthier (2020), *Scientific Reports*  
DOI: 10.1038/s41598-020-78565-y

The long-term Bylot reproductive-success surface adds a separate theorem-scale
ingredient. At the beginning of the study, expected reproductive success was
0.03 young reaching age one at relative Day -10, peaked at 0.52 on Day -4 and
fell to <0.01 by Day +10 (published average post-peak decline 0.036
young/day). By the end of the study, peak success was 0.74 on Day -6 and
declined to 0.01 by Day +10 (0.046 young/day).

The same paper gives a condition-dependent waiting example: a five-egg female
on Day -4 could delay about 1.6 days to acquire nutrients for an additional
egg, whereas a delay of >=2 days made waiting worse than laying the smaller
clutch immediately.

Qualification:

- natural two-sided timing-loss surface: **YES**
- independent finite waiting-deadline example: **YES**
- exact binary PAYOFF-B C_F/C_M: **NO — requires a prespecified state/action mapping**
- information-acquisition D: **NO — waiting acquires nutrients, not information**
- actor-level cue-use threshold: **NO**

Classification: **FITNESS_LOSS_AND_WAITING_DEADLINE_ANCHOR_NOT_DIRECT_INFORMATION_TEST**

This means the greater-snow-goose route no longer lacks evidence that seasonal
timing errors and waiting itself can carry large fitness costs. The remaining
problem is identifying those quantities on the declared information-game scale
and observing the cue-use switch.

### Next gate for greater snow goose

Before any threshold claim:

1. estimate raw information-waiting delay separately from captivity/handling stress and quantify how much of that delay is recovered downstream, including the cost of compensation;
2. reconstruct pre-outcome rolling temperature predictability q for the exact
   St. Lawrence -> Arctic decision contexts without using focal behavioural
   outcomes;
3. identify an individual movement dataset in the same population with
   departure/stopover decisions across enough years to expose q variation;
4. define cue use before inspecting its relationship with q;
5. estimate early and late state-loss terms independently;
6. only if steps 1-5 succeed, test whether the observed switch interval contains the predicted q_wait(D_eff).

If step 3 fails, retain this as a composite same-system bridge rather than a
direct threshold test.

---

## Candidate 2 — Barnacle goose predictability system

Kölzsch et al. (2015), *Journal of Animal Ecology*  
DOI: 10.1111/1365-2656.12281

Public tracking sources include Movebank datasets from the original study.

What it supplies:

- 40 tracked barnacle geese across Greenland, Svalbard and Barents Sea routes;
- 16 combined stopover regions;
- environmental predictability between consecutive stopovers;
- observed arrival timing;
- published evidence that arrival at stopovers was more closely tied to local spring onset where predictability was higher.

Qualification:

- q-like information quality: **YES**
- behaviour linked to q: **YES, continuous timing response**
- independent D_eff: **NO**
- binary wait/use-cue decision: **NO**
- exact q1 < q <= q2 window: **NO**

Classification: **NEAR_DIRECT_INFORMATION_USE_LANE**

This is substantially closer to the theorem than the current wigeon post-error-correction lane because the response concerns timing relative to environmental predictability rather than correction after phase error.

## Candidate 3 — Barnacle goose breeding / fitness extension

Boom et al. (2023), *Journal of Animal Ecology*  
DOI: 10.1111/1365-2656.14020  
Dryad: 10.5061/dryad.m63xsj47x

The public dataset contains 96 adult female barnacle geese, some repeated over years, spanning 2008–2020. It provides nest/potential-nest locations, breeding status, nesting success, arrival date and local GDD-based spring onset, plus raw tracking data for records not already hosted on Movebank. The source also incorporates 11 tracks from the Kölzsch et al. lineage.

What it adds:

- breeding propensity;
- nesting success;
- arrival date relative to spring onset;
- broad life-history tactics from long-distance migrants to residents;
- raw tracking support for many tracks.

Important boundary:

Breeding propensity or nesting success is a fitness consequence, not automatically the opportunity cost D of waiting one decision interval. Estimating D from these outcomes would require a prespecified causal/decision model for how a marginal delay changes expected fitness. It cannot be read off from Breeding or Nesting_success.

Qualification:

- q-like information quality: **potentially reconstructable**
- fitness consequence: **YES**
- independent D_eff: **NOT YET**
- cue-use threshold: **NOT YET**
- exact asynchronous window: **NO**

Classification: **INFORMATION_USE_CANDIDATE_D_GATE_NOT_IDENTIFIED**

### Post-screen D-identification gate

The published Boom et al. analysis does not provide a clean marginal delay
cost. Relative arrival (arrival date minus local spring onset) was explicitly
tested as a predictor of breeding propensity, but models containing local
spring onset outperformed models based on relative arrival. The best reported
breeding-propensity model used latitude, spring onset and their interaction,
not a stable per-day arrival penalty.

This matters directly for PAYOFF-B: a state-dependent association between
spring timing and breeding probability cannot be relabelled as the theorem's
opportunity cost D. In this source, D is therefore **not identified** under the
current simple model.

Barnacle goose remains valuable for the information-quality -> timing-response
edge, but the direct D -> q threshold route is stopped unless an independent
delay-cost experiment or fitness model is introduced.

## Candidate 4 — American redstart delay-cost anchor

Dossman et al. (2023), *Ecology*  
DOI: 10.1002/ecy.3938

The study reports that birds departing 10 days later migrated about 43% faster and had about a 6.3% reduction in apparent annual survival. The paper also cites prior evidence that an approximately 10-day arrival difference was associated with a substantial reduction in fledging success.

What it supplies:

- a concrete ecological cost associated with migratory delay;
- an empirically grounded time-pressure / deadline axis.

What it lacks for the theorem:

- a controlled or reconstructed cue-reliability sweep q;
- an observed switch in use of a later cue;
- a shared-cue interacting pair.

Classification: **DELAY_COST_ANCHOR_ONLY**

## Decision

No screened source currently licenses the sentence:

> measured D_eff,2-D_eff,1 predicts measured q2-q1, and the interval q1 < q <= q2 contains observed asynchronous cue use.

The strongest development path is now the greater-snow-goose St. Lawrence -> Bylot lineage because an experimental perturbation-duration manipulation and an independent route-predictability reconstruction exist in the same ecological system. Barnacle goose remains the strongest tracking-based information-use candidate.

However, PAYOFF-B should **not** promote that system to a direct theorem test unless D_eff can be estimated independently of the cue-use outcome.

## Next analysis gate for the barnacle-goose lineage

Before opening any new response model:

1. reconstruct consecutive-stopover predictive connectivity from historical spring-onset series;
2. define the decision event at each stopover without using the focal response;
3. determine whether an independent fitness model can identify the effective marginal waiting cost D_eff after downstream compensation;
4. verify that q spans enough range to bracket an actor-specific threshold;
5. only then register a cue-use threshold analysis.

If step 3 fails, retain barnacle goose as a strong information-use bridge, not a direct D_eff -> q test.

## Claim ceiling after this screen

The correct current statement is:

> The deadline-to-threshold-to-asynchrony mapping is exact and implementation-verified in the declared model. Existing natural systems support information quality, timing dependence, response asymmetry and fitness costs of delay separately, but no located dataset yet identifies the full pairwise deadline-threshold mechanism in one natural system.
