# Memory-aware plasticity and a controller-independent modularity certificate

Date: 2026-10-20. Status: **synthetic mathematical extension; no new biological observation or historical origin test**. This extends PAYOFF PR #338 while retaining its model and source code unchanged. Base read: `5993acd62d459d9403a90d1f5d3b591715b0f998`; original model blob: `e81cac684148cc08bace138deb69fc26417e3811`.

## Main result

Allowing a reversible phenotype to use its history can overturn an apparent advantage of fixed modules. Nevertheless, fixed modules can also be certified as better than **every** single-coordinate response under specified physical switching costs—even a controller supplied with the entire future environmental sequence. These are different results and must not be conflated.

The earlier switching threshold `rho*=0.65625` remains correct **within the original memoryless policy class**. It is not a threshold for unrestricted plasticity or for genetic/historical structural evolution.

## 1. Unchanged biological assumptions

Both quadratic functions remain active in every period. In environment 0 their loss is `a*x^2 + b*(x-Delta)^2`; environment 1 swaps the positive weights `a >= b > 0`. The environment is a symmetric stationary two-state Markov chain with switching probability `rho`. Conditional independent binary cues identify the current state with probability `q >= 1/2`.

Define

```
w = a+b
C = a*b*Delta^2/(a+b)
d = (a-b)*Delta/(a+b)
T = w*d^2/4
```

Every one-coordinate phenotype has instantaneous loss `C + w*(x-z_E)^2`, where `z_E` is the state-specific optimum. The nonresponsive constant phenotype has average loss `S=C+T` and pays no plastic machinery cost. A dynamic shared phenotype pays `B >= 0` per period and `c*abs(x_t-x_(t-1))`, with `c >= 0`. The ideal differentiated architecture coexpresses two independently optimized functional coordinates for loss `K` per period.

Environment and cue parameters are known to the model controllers and identical across the comparisons. Additional memory cost is set to zero unless stated; its permissible positive budget is quantified below. Fitness is the **same per-period log-fitness debit** used in the original model. Lower loss means higher intrinsic value, not demonstrated invasion or fixation.

## 2. Finite cue history: feasible policies rather than universal optima

Let `m_t=E[2E_t-1 | Z_(t-m+1),...,Z_t]`. Consider a feasible phenotype rule

```
x_t = Delta/2 + (d/2)*beta*m_t,  0 <= beta <= 1.
```

Write `R_m=E[m_t^2]` and `V_m=E[abs(m_t-m_(t-1))]`. Adjacent cue windows overlap and are **not independent**. We obtain their moments by exhaustively summing all `2^(m+1)` cue words, using the two-state forward recursion. No Monte Carlo approximation is used; calculations are floating-point evaluations of finite sums. Tests independently enumerate both hidden and observed sequences in exact rational arithmetic for short windows.

The loss of this feasible policy is

```
J_m(beta) = C+T+B+M + T*R_m*(beta^2-2*beta) + c*d*beta*V_m/2
beta* = clip(1 - c*d*V_m/(4*T*R_m), 0, 1)
```

where `M` is an explicit additional memory cost. If `T*R_m=0`, set `beta=0`. For one cue, this reproduces the original memoryless optimum exactly.

This posterior-amplitude policy is not the optimum over all functions of cue history. In particular, better state estimates can increase physical switching; simply following a better estimate need not lower total loss.

### Convex optimization over every mapping of a finite cue window

For `m<=6`, we additionally optimize arbitrary deterministic actions `u_h in [-1,1]` for each cue word `h`, not only posterior-proportional actions. With word probabilities `p_h`, posterior means `m_h`, and adjacent-word edge probabilities `p_e`, the exact stationary objective is

```
J(u)=C+T+B + T*sum_h p_h*(u_h^2-2*m_h*u_h)
                + (c*d/2)*sum_e p_e*abs(u_destination-u_source).
```

This is a convex weighted graph total-variation problem. For edge-incidence operator `D` and dual variables `abs(v_e)<=c*d*p_e/2`, a lower bound **on this finite-window class only** is

```
D(v)=C+T+B-T*sum_h p_h*m_h^2
     + v^T Dm - sum_h (D^T v)_h^2/(4*T*p_h).
```

The solver reports both a feasible primal value and a feasible dual value. Their gap is checked rather than treating the optimizer's success flag as proof. Zero-probability histories are excluded from divisions. SciPy's L-BFGS-B is used only to find a feasible dual point; the bound's algebra does not rely on solver convergence. A primal value is an **upper** bound on unrestricted optimal plasticity, not a lower bound.

Reproducible source for the optimization API: SciPy `optimize.minimize` official documentation, https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.minimize.html. This documentation is implementation provenance, not ecological evidence or a priority claim for the mathematics.

## 3. A policy-independent bound, even granting perfect foresight

For two successive periods whose state optima differ by `d`, minimize the relaxed pair loss

```
(w/2)*[(x-z0)^2+(y-z1)^2]+c*abs(y-x).
```

The exact minimum is

```
psi(c) = c*d - (c*d)^2/(4*T)   if c*d <= 2*T
         T                    if c*d >= 2*T,
```

with `psi=0` when `T=d=0`. If the state does not change, the corresponding minimum is zero. This calculation grants both target states to the controller and minimizes the neighboring actions independently of all other periods. It therefore relaxes, rather than restricts, the problem.

**Finite-path proof.** Summing these pair objectives over periods 2 through n counts every interior squared error once and endpoint squared errors at half weight. The actual total loss includes the remaining nonnegative endpoint half-errors. Thus, for *any* action sequence, deterministic or randomized, causal or supplied with the future,

```
sum_t stage_loss_t + sum_(t>=2) switching_cost_t
    >= n*(C+B) + number_of_environment_switches*psi(c).
```

Take stationary expectation and divide by n; the limit gives

```
J_any_dynamic >= C+B+rho*psi(c).
```

No finite-memory, reaction-norm, parameter-learning or prediction assumption is needed for this inequality. It still assumes one shared coordinate, the stated simultaneous quadratic losses, nonnegative costs, and an exogenous environment.

The dynamic class must also compete against a nonplastic constant architecture that avoids `B`. Hence

```
L = min(C+T, C+B+rho*psi(c))
L <= J_best_nonmodule <= U,
```

where `U` is the best explicitly evaluated feasible policy or constant phenotype. Therefore:

- `K<L`: fixed modules beat **every** alternative in the declared shared-coordinate architecture class.
- `U<K`: at least one explicit nonmodule policy beats fixed modules.
- `L<=K<=U`: unclassified or tied; do not report an exact unrestricted phase boundary.

These are intrinsic value comparisons only. If genetic inaccessibility or a measured frequency-dependent invasion penalty exists, the value ranking alone is insufficient.

## 4. Results: retain the original witness; label new witnesses separately

All quantities below are synthetic, normalized losses. `a=3, b=1, Delta=2, q=.9, B=.05, c=1` throughout, so `C=3`, `T=1`, `d=1`, and `S=4`.

### A. Original parameters, K=3.8

| Environmental switching | Original one-cue policy | Optimized six-cue mapping | Lower bound on all nonmodule policies | Unrestricted conclusion |
|---|---:|---:|---:|---|
| rho=.1 | 3.590316 | 3.460214324 | 3.125 | A feasible plastic policy beats K=3.8 |
| rho=.9 | 3.871916 | 3.867408639 | 3.725 | **Unresolved**, because K=3.8 lies between the bounds |

At rho=.9, fixed modules still outperform every computed finite-window optimum up to six cues. This is not proof that they outperform arbitrary history-dependent control. Conversely, failure to certify global superiority is not evidence that a real plastic strategy with cost below 3.8 exists at rho=.9.

### B. Explicit counterexample to treating memoryless advantage as general: K=3.55, rho=.1

The original one-cue loss `3.590316` exceeds module cost `3.55`. But a two-cue posterior-amplitude policy has loss **3.499824220**, while the optimized two-cue mapping reaches **3.493508431**. Thus the initially apparent fixed-module advantage reverses without changing functions, ecology, cue accuracy, or switching cost—only the available response policy changes.

Even the simple posterior-amplitude rule tolerates an **additional memory cost strictly below 0.050175780 per period** before its advantage disappears. This is a conditional budget, not an empirically measured memory cost. K=3.55 is a new synthetic diagnostic, not a revision of the original K=3.8 evidence record.

### C. Positive result robust to all memory and prediction: K=3.6

Here `psi=0.75`. At slow turnover rho=.1 the original feasible plastic policy has loss **3.590316 < 3.6**, so modules cannot be intrinsically best. At fast turnover rho=.9, **every dynamic shared-coordinate policy** has loss at least `3+.05+.9*.75=3.725`; the constant shared alternative costs 4. Therefore fixed modules with loss **3.6** are better by **at least 0.125**, even against perfect hindsight control.

For these parameters `rho>11/15` is a **sufficient**, not necessary, condition for this controller-independent certificate. It is not a replacement exact phase boundary for 0.65625. K=3.6 is a separately labeled theoretical witness, not fitted to any organism.

### D. Frequent switching is not synonymous with unpredictability

At rho=1 the environment alternates perfectly. For q>1/2, multiplying each observed cue by known time parity gives repeated independent noisy observations of the initial phase. Accumulating this evidence learns that phase with vanishing error. With no additional information-accumulation cost, the pair lower bound is attained asymptotically by the appropriately shrunk alternating phenotype:

```
inf J_dynamic = C+B+psi(c) = 3.8.
```

The original K=3.8 module therefore **ties**, rather than strictly beats, the unrestricted asymptotic response in this endpoint. The original one-cue calculation remains `3.8979` because that policy cannot accumulate phase information. This is not an inference that biological organisms have unlimited cost-free memory.

## 5. What this adds to the SCH–BALANCE–SLK/PAYOFF–BITA synthesis

The more defensible mechanism is not “strong conflict or frequent change automatically creates new structure.” It is **irreducible simultaneous functional demand plus physical response costs can give structural separation an advantage that information alone cannot remove**.

SCH's role remains identifying actual opposed functional demands on one coordinate. BALANCE must compare fixed shared, reversibly adjustable, and genuinely differentiated alternatives on matched fitness/time scales. SLK retains architecture-value and evolutionary-realization ownership. PAYOFF supplies the explicit stochastic extension and bounds. BITA remains the orthogonal mechanism-identification layer; no statistical residual is renamed a switching cost.

No new claim is made about Wurmbea, genetic architecture, origin counts, or transition direction. Fixed two-coordinate coexpression is not automatically equivalent to dioecy among separate individuals. The original Wurmbea observations motivated concern about reversible phenotype states, but neither their response percentages nor their seed-fitness ratios supply these model parameters.

## Reproduce and verification

```
python -m pip install pytest numpy scipy
python -m pytest -q tests/test_history_aware_compromise.py
python scripts/audit_history_aware_compromise.py --out /tmp/history_robustness.json
```

Thirty added local tests passed, including three independent Fraction-based hidden/observed sequence enumerations, the pointwise pair bound, one-cue reproduction, finite-window primal–dual gaps, information/cost edge cases, explicit memory-cost budget, and the known-environment endpoint theorem. No original manuscript, empirical data, or earlier memoryless result is overwritten. The check remains a model validation, not an experiment.
