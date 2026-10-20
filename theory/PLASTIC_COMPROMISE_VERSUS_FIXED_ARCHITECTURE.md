# Plastic compromise versus permanent modular architecture under ecological turnover

**Version:** 2026-10-20
**Status:** exact mathematical consequence of a newly declared restricted model. NOT a biological finding, not a novel priority claim against the literature, not source-calibrated to *Wurmbea*. The manuscript hierarchy and ownership contracts of SCH / BALANCE / SLK / BITA remain unchanged.

## Research question

> A measured same-coordinate functional trade-off can be handled by a constant compromise, a reversible adjustment of the shared phenotype, or a permanently differentiated architecture. When does ecology reward each, and when might value fail to become an invasion or historical transition?

Earlier PAYOFF [modularization barriers](DISCONTINUOUS_MODULARIZATION_BARRIER.md) and [frequency feedback](../docs/CLAIM_BOUNDARY.md) correctly show that positive global architecture value does not guarantee an accessible evolutionary step. Here we add **a third candidate: reversible plasticity**, explicitly retaining the loss imposed by two *simultaneously active* functions. This is not a reinterpretation of PAYOFF-B migration timing or the unrelated measurement-budget route.

## Two active functions and two ecological regimes

Let the two biological functions both be active, with true same-coordinate optima `theta_1=0` and `theta_2=Delta>0`. In regime 0, weights are `(a,b)`, while regime 1 swaps them to `(b,a)`; assume `a>=b>0`.

The single-phenotype fitness *loss* is

```text
state 0: F0(x) = a*x² + b*(x-Delta)²
state 1: F1(x) = b*x² + a*(x-Delta)².
```

Both regimes still contain functional conflict even when one weight is dominant. Each regime's optimized same-coordinate loss is

```text
C = ab/(a+b)*Delta²
```

and its optimized phenotype is `x0*=b*Delta/(a+b)` or `x1*=a*Delta/(a+b)`.

Separate `C`, the **unavoidable simultaneous conflict floor** when both functions must use one coordinate, from

```text
d = (a-b)*Delta/(a+b)
T = (a-b)²*Delta²/[4(a+b)].
```

Here `d` is the physical distance between regime-optimal shared phenotypes, and `T` is the additional cost of maintaining the same stationary compromise across both regimes. Under stationary regime probability 1/2, the optimized constant shared phenotype is `x=Delta/2`, with expected log-fitness debit:

```text
LOSS_SHARED = C + T.
```

**Important**: `C` is a model-generated same-coordinate loss, not an empirically identified SCH `L`. `T` is a separate *cross-environment* mismatch term and is **not** another instance of simultaneous functional conflict. The identity `R=sL` in the SCH–SLK quadratic residual-coupling bridge is not asserted here.

## Explicit environmental turnover and noisy cue

True ecological regime `E_t in {0,1}` follows a stationary, symmetric Markov chain with a switch on each step with probability `rho`. The observed binary cue `Z_t` has independent per-step errors conditional on the ecological regime:

```text
P(Z_t = E_t | E_t) = q,   1/2 <= q <= 1.
u = 2q-1.
```

One can verify by enumerating 16 pairs of true/observed states that the *cue*, rather than the true environment, switches between adjacent observations with probability

```text
h(rho,q) = 2q(1-q) + rho(2q-1)².
```

Consequently, a plastic organism can pay switching costs even if the true ecology remains unchanged, because noisy cues occasionally reverse.

The reversible architecture uses the explicitly restricted **memoryless symmetric policy**

```text
x_t = Delta/2 + [alpha*d/2] * (2Z_t-1),   0 <= alpha <= 1.
```

The plastic machinery has a fixed per-step running cost `B>=0`, and a linear switching cost `c>=0` per unit absolute phenotypic change. The resulting *stationary long-run expected log-fitness debit* is

```text
LOSS_PLASTIC(alpha)
  = C + T[1+alpha²-2alpha*u] + B + c*abs(d)*alpha*h(rho,q).
```

The exact within-policy-class optimum is

```text
alpha* = clip( u - c*abs(d)*h/(2T), 0, 1 )   when T>0;
alpha* = 0                                  when T=0.
```

At its interior optimum this simplifies to

```text
LOSS_PLASTIC* = C+T+B - T*(alpha*)².
```

At the lower clipped boundary `alpha*=0`, the same formula applies, but the unused plastic machinery `B` is dominated by the separate SHARED architecture when `B>0`. Because `0<=u<=1` and all costs are nonnegative, the upper clip cannot bind except at a cost-free perfect-cue boundary.

### The critical ecological result

Even when `q=1`, `c=0`, and `B=0`, the fully adjusted plastic policy has

```text
LOSS_PLASTIC* = C > 0  (if Delta>0).
```

**Perfect plastic adjustment removes the *environmental switching mismatch*, not the intrinsic conflict of two simultaneously active functions constrained to one coordinate.**

The only module that entirely removes both terms in the idealized model has two independent coordinates held at the distinct optima across regimes and pays its per-step construction/maintenance debit `K`:

```text
LOSS_FIXED_MODULES = K.
```

A permanently differentiated architecture is intrinsically best in this restricted three-strategy comparison only when

```text
K < min(LOSS_SHARED, LOSS_PLASTIC*).
```

This is a model-specific static fitness statement; it is **not** evidence that a new genetic architecture is accessible or can invade when rare. The full SLK architecture-value, topology, frequency-penalty and heritability checks still follow.

## Separate prediction: simultaneous functional overlap defeats even perfect plasticity

The turnover boundary is not the only way permanent structural separation can become advantageous. A second, mathematically distinct scenario follows by setting **perfect cue information** `q=1`, **zero switching cost** `c=0`, and **zero plastic machinery cost** `B=0`. The best reversible shared-coordinate allocation still has loss

```text
LOSS_PLASTIC*=C=ab/(a+b)*Delta².
```

For fixed `a>0`, fixed trait-optimum separation `Delta>0`, and fixed two-axis cost `K>0`, strengthening the weaker *simultaneously active* function (increasing `b` toward `a`) raises this irreducible plastic loss:

```text
dC/db = a²*Delta²/(a+b)² > 0.
```

The perfect-cue plastic versus permanent-module boundary occurs when `C(b)=K`. In the strict interior of the allowed `0<b<a` model this yields

```text
b* = K*a/(a*Delta²-K).
```

This requires `0<K<a*Delta²/2` and no other hidden costs. It is not present for every admissible parameter set.

A second normalized **model-only** counterexample holds cue quality, environmental turnover, all architectural costs and both function optima fixed:

```text
a=3, Delta=2, q=1, c=0, B=0, K=1, rho=0.2
b*=3/11 = 0.2727272727...
```

| Weaker co-occurring function weight b | Unavoidable loss with optimal plasticity C | Fixed-module loss K | Intrinsically favored option |
| --- | ---: | ---: | --- |
| **0.10** | **0.3870968** | 1.0 | PLASTIC |
| **3/11** | 1.0 | 1.0 | PLASTIC = FIXED |
| **0.60** | 2.0 | **1.0** | FIXED |

Thus **simultaneous overlap of conflicting function demands**, rather than just contrasting selection gradients across seasons, can create a selective incentive for different coordinates. Temporal switching with perfect feedback cannot eliminate `C`; true structural separation could do so at `K`. As `b->0`, the simultaneous conflict floor approaches zero and nearly perfect plasticity can suffice.

This ecological interpretation is restricted to the declared co-active two-function model. It does not demonstrate that sex-separated individuals simultaneously deliver both female and male payoffs, and does not tell us the actual overlap parameter `b` in Wurmbea or any plant. The two thresholds (`rho*` for turnover and `b*` for overlap) concern **different controlled parameter slices** and are not interchangeable empirical results.

## Proposition: sufficiently rapid ecological turnover can change the favored architecture

For `T>0, q>1/2, c>0`, `h` increases with the true flip probability `rho` as

```text
d h / d rho = (2q-1)² >= 0.
```

As the switching-cost term grows, optimal `alpha*` is nonincreasing in `rho`; consequently `LOSS_PLASTIC*` is nondecreasing, while `LOSS_SHARED` and `K` are unchanged. A strict PLASTIC→FIXED transition occurs when the two costs cross and `K<LOSS_SHARED`. Where it is interior, put

```text
alpha_cross = sqrt((C+T+B-K)/T)
rho_cross  = [ 2T(u-alpha_cross)/(c*abs(d)) - 2q(1-q) ]/u².
```

This is admissible only if `0<rho_cross<1`, the plastic option wins at `rho=0`, and the fixed alternative beats it at `rho=1`. Do not claim a universal threshold when those conditions fail. The result concerns the declared, **memoryless** cue-response policy only. Better multi-season inference or predictive controllers could outperform it.

### Fully specified synthetic witness

Use arbitrary normalized log-fitness cost units:

```text
a=3, b=1, Delta=2, q=0.9,
B=0.05, c=1, K=3.8.
```

Then `C=3`, `T=1`, `d=1`, `LOSS_SHARED=4`, and

```text
h = 0.18 + 0.64*rho
alpha* = 0.71 - 0.32*rho
LOSS_PLASTIC* = 4.05 - (0.71 - 0.32*rho)²
LOSS_FIXED_MODULES = 3.8.
```

| Environmental switch probability rho | Optimal plastic response alpha* | Shared loss | Plastic loss | Fixed-module loss | Best intrinsic response |
| --- | ---: | ---: | ---: | ---: | --- |
| **0.10** | 0.678 | 4.000 | **3.590316** | 3.800 | PLASTIC |
| **0.65625** | 0.500 | 4.000 | 3.800000 | 3.800 | PLASTIC = FIXED |
| **0.90** | 0.422 | 4.000 | 3.871916 | **3.800** | FIXED |

The stationary simultaneous functional conflict `C`, baseline architecture costs, cue fidelity, and two function optima are **unchanged** across these three cases. Only environmental turnover changes.

This provides a concrete *mechanistic prediction*, not a new observation about plant evolution: changing turnover alone can favor a permanent differentiated module over the best response in a constrained plastic policy class.

## Frequency and evolutionary-realization gates are still separate

Suppose a **separately justified** positive architecture coordination penalty `eta>=0` reduces rare FIXED invasion relative to the resident phenotype. Then the hypothetical game margin is

```text
I_D = min(LOSS_SHARED, LOSS_PLASTIC*) - K - eta.
```

At `rho=0.9` for the witness, `min(S,P*)-K = 3.871916-3.8=+0.071916`. With hypothetical `eta=0.08`, `I_D=-0.008084`: the fixed architecture is intrinsically best but cannot invade under this declared coordination assumption. `eta` must be measured by frequencies of actual heritable architectures; it cannot be inferred from sex morph prevalence alone.

The declared model also assumes that **D operates its two functional coordinates simultaneously without cues or residual coupling**, which need not hold for sex separation **among individuals**. Dioecy at individual level is a population-level mating/sex allocation state, not an individual that simultaneously performs both sex functions. Consequently this mathematical result is a general structural comparator and **must not be mechanically transplanted onto a Wurmbea female/male fitness ratio**.

## Empirical status and testable predictions

The relevant independent Wurmbea biological receipts are in [BALANCE's voucher-matched genetic and plasticity audit](https://github.com/zuizui0223/balance/blob/analysis/wurmbea-genbank-history-20261019/docs/BALANCE_WURMBEA_CASE2008_REAL_GENBANK_VOUCHER_QC_RESULT_20261019.md). Source-published information includes:

- *W. dioica*: approximately half of returning male-expressing marked individuals developed hermaphroditic flowers in the following observed season (1981/1983). That is **within-individual phenotypic change**, not a new nuclear sexual genotype;
- *W. dioica*: high/low resources gave 66% versus 42% perfect-flower expression among subdioecious males; resource variation can change expressed phenotype without demonstrating genetic turnover;
- source-published female seed-fitness advantage 3.7 versus 1.4 under increased outcrossing of fruiting males, **not** a complete two-sex lifetime fitness comparison;
- genotype source-status: Case et al. (2008) plastid vouchers and 21/23 source-voucher-concordant focal loci; MR2/MR3 `psbBTNH` conflict is currently held; plastid similarity is not nuclear sexual genotype identity.

**Additional source-recovered biological contrast** ([BALANCE source-specific original-study extraction](https://github.com/zuizui0223/balance/blob/analysis/wurmbea-genbank-history-20261019/docs/BALANCE_WURMBEA_FUNCTIONAL_COST_HETEROGENEITY_V1.md)): Vaughton & Ramsey, DOI 10.1093/aob/mcr163, report that *subdioecious W. dioica* phenotypic males produce approximately **twice** the pollen per flower of hermaphrodites, whereas *cosexual and gynodioecious W. biglandulosa* males produce about **40% less** than hermaphrodites. The partial association of the number of perfect flowers with pollen/flower diameter is negative only in the subdioecious system, versus nonnegative/positive in the other source populations. Pollen grains are **not pollen siring fitness**, these are **one study's populations**, resource/plant-size confounding persists, and a partial correlation is **not a measured machinery switching debit c or a source-derived SCH conflict floor C**. Nevertheless, the result is a real demonstration that a simple *same source* plastic-male cost proxy cannot be assigned the same biological sign in every sexual-system context.


**None of these measurements identify model parameters `a,b,Delta,q,rho,B,c,K` or an inherited invasion parameter `eta`.** Even the 66% versus 42% response cannot be treated as cue accuracy `q`, and the 1981→1983 marked-plant transition cannot be treated as the Markov *environmental* switch rate `rho`.

A credible empirical test, whether in *Wurmbea*, flowering plants or unrelated multifunctional systems, requires **separately**:

1. Same-coordinate *simultaneous* functional gradient/reaction-norm tests for `a,b,Delta`, with a measured `C` rather than an assumed co-occurrence;
2. Repeated environment-and-cue time series, measuring cue reliability and the true environmental turnover rate, plus within-individual phenotype switching and its attributable cost;
3. Matched shared/plastic/differentiated genetic architectures on a common reproductive-fitness and temporal scale, with independently measured module cost;
4. Heritability, genetic access and mutation/crossing evidence, actual architecture-frequency fitness, and nuclear/plastid phylogenetic replication before **historical-origin** inference.

An observed threshold or even all three verified fitness surfaces does not demonstrate that the differentiated structure originated in response to the ecological conflict. The lineage-level temporal order and alternatives (exaptation, drift, ecological sorting, plasticity, introgression) remain independent tests.

## Execution and source ownership

```bash
python -m pytest -q tests/test_plastic_compromise_architecture.py
python scripts/run_plastic_compromise_boundary.py --out /tmp/plastic-compromise-receipt.json
```

- Exact model: [`src/plastic_compromise_architecture.py`](../src/plastic_compromise_architecture.py).
- Verification: [independent 16-case state/cue enumeration tests](../tests/test_plastic_compromise_architecture.py).
- Readout: [script](../scripts/run_plastic_compromise_boundary.py); every result is stamped `EXACT_MODEL_WITNESS_NOT_REAL_BIOLOGICAL_DATA`.
- **SLK** remains the owner of architecture-value generalities and the flagship integration.
- **PAYOFF** supplies this bounded stochastic/ecological plasticity-vs-structure mathematical result and invasion-gate parameterization.
- **SCH** owns causal identification of the pure-function shared-axis conflict.
- **BALANCE** owns direct matched source worldlines and persistence.
- **BITA** owns ecological mechanism identification after trait interactions, not `K` or genetic origin.

**Claim ceiling:** under *these* assumptions, simultaneous functional conflict creates a floor that perfect temporal plasticity cannot avoid, while high ecological turnover and switching cost can make permanent modular architecture the intrinsic optimal alternative. The result is neither a universality theorem over all forms of plasticity nor an empirical Wurmbea evolutionary-origin result.
