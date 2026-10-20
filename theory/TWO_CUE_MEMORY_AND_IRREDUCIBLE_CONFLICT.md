# Two-cue memory, re-entrant plasticity, and an irreducible simultaneous-conflict floor

Date: 2026-10-20. **Status: exact conditional mathematical model and synthetic robustness counterexamples; NOT an observed evolutionary transition, a Wurmbea parameter fit, or an original universal theorem in plasticity theory.** This is a supplemental result to PAYOFF PR #338. The original memoryless source, its pre-existing manuscript scope, and the sister-repository ownership contract are unchanged.

## 1. What question was tested

Does higher environmental switching always move advantage from plastic sharing toward fixed modular differentiation? **No, not once prediction from past cues is allowed.** In a symmetric binary Markov environment with switch probability rho, lag-one environmental correlation is r=1-2rho and the environmental entropy rate is H2(rho). At rho=0.5, the next environment is maximally unpredictable from the last *true* environmental state; as rho approaches one, rapid changes become nearly deterministic alternation.

This new model never gives the organism the hidden true state. It allows a deterministic, stationary phenotype response to the current and immediately previous **noisy cues** with accuracy q and optional extra memory cost M. The source cue process and per-unit phenotype-change cost are retained from the existing PAYOFF architecture comparison.

## 2. Original same-coordinate conflict is held fixed

There are two simultaneously operating functions with distinct optima 0 and Delta. The quadratic loss in state 0 is F0(x)=a*x²+b*(x-Delta)²; in state 1 the weights (a,b) are swapped. Assume a>=b>0 and Delta>=0. Completing squares:

    C = ab*Delta²/(a+b)                 unavoidable same-time functional conflict
    d = (a-b)*Delta/(a+b)               shift between environment-specific optima
    T = (a+b)*d²/4                      added loss of unresponsive compromise
    F_state(x) = C + (a+b)*(x-x_state_star)²  >= C.

The stationary SHARED comparator has loss S=C+T. The original ideal differentiated two-coordinate module simultaneously realizes both optima, with per-period log-fitness debit K. **It is not biologically equivalent to male and female functions divided among separate individual plants without a separate mating/population model.** The shared optimum, module comparison and their fitness horizon remain unchanged here.

## 3. Exact unrestricted map of two binary cues

Write hidden environment sign as +/-1 and normalized phenotype as x=Delta/2+(d/2)*y. There are four possible observed cue pairs. By quadratic convexity and cue/fitness complement symmetry, at least one global optimum over all stationary deterministic maps of these **two cues** can be written

    y(00) = -u ; y(01) = v ; y(10) = -v ; y(11) = u,

with 0<=u,v<=1. This is not a restriction to monotonic response to the present cue: v may exceed u when almost-alternating environments make past information useful. Clipping amplitudes cannot raise convex state mismatch or the absolute phenotype-switch penalty.

Let g=2q-1 and r=1-2rho; define

    ps = (1+g²r)/2 ; pd = (1-g²r)/2
    ks = g*(1-rho) ; kd = g*rho
    w  = (1-g²r²)/4
    t  = (1-2g²r+g²r²)/4.

The independent 64-path enumerator verifies these moments against all possibilities for three successive environments and three emitted cues. With baseline plastic running cost B, per-unit phenotype switch cost c, and cd=c*d, the exact stationary loss of the two-cue policy is

    J2(u,v)
     = C+T+B
       + T*(ps*u² + pd*v² - 2ks*u - 2kd*v)
       + cd*[w*(|u+v|+|u-v|)/2 + t*|v|].

The bracket equals w*max(|u|,|v|)+t*|v|, producing two convex quadratic regions separated by u=v. Their feasible interior minima are found by clipping the following candidates and keeping only those meeting their corresponding inequality:

    region u>=v:
      u=(ks-cd*w/(2T))/ps, v=(kd-cd*t/(2T))/pd.
    region v>=u:
      u=ks/ps,            v=(kd-cd*pd/(2T))/pd.
    diagonal u=v:
      alpha = clip(g-cd*pd/(2T),0,1).

If one region's unconstrained optimum violates its ordering, that constrained region's optimum lies on the diagonal. The implementation explicitly evaluates the feasible regions and the diagonal; zero-probability cue events and T=0 are handled separately. This is **an exact optimum for the declared two-cue policy class**, not for arbitrary policies with latent internal state or unlimited history.

Additional memory cost M is charged only to PLASTIC_MEMORY. Four competitors are compared on the same per-period loss scale: SHARED, PLASTIC_MEMORYLESS, PLASTIC_MEMORY and FIXED_MODULES. Lower loss is favorable. Architectural preference is not an identified genotype invasion rate.

## 4. The original turnover example survives, but monotone generalization fails

The original synthetic parameters a=3, b=1, Delta=2, q=0.9, B=0.05, c=1 have C=3, T=1. With original module K=3.8, memory-optimized plasticity wins at rho=0.1 (3.493508431) and fixed modules win at rho=0.9 (fixed 3.8 versus memory 3.869056206). This preserves the original example classification.

A different **exploratory robustness** setting modifies only K from 3.8 to 3.87, retaining the other values:

| rho | Memoryless optimized plastic | Two-cue optimized plastic | Fixed modules K | Intrinsic winner |
| --- | ---: | ---: | ---: | --- |
| 0.90 | 3.871916 | **3.869056206** | 3.870 | Memory plasticity |
| 0.95 | 3.885164 | 3.872457906 | **3.870** | Fixed modules |
| 0.99 | 3.895393760 | **3.867283201** | 3.870 | Memory plasticity |

There are two numerically bracketed crossings, approximately rho=0.9066209383 and 0.9765403818; the relevant polynomial coefficients in descending order are [131072, -193024, 14720, 47637]. The brackets are verified by direct evaluation of the piecewise objective, **not interval-arithmetic root certification**. Choosing K=3.87 after examining robustness is not preregistered biological evidence.

At rho=0.99 the optimal two-cue response discounts agreeing cues (u about 0.04291845) but amplifies differing cues (v about 0.47345133), extracting information from the near-alternating regime. Its value edge over fixed K=3.87 is only about 0.002716798967; memory costs M=0.001 preserve that advantage, but M=0.004 remove it.

**New mechanism:** high turnover rate cannot be substituted for environmental unpredictability. The original fixed-architecture advantage at high turnover is an exact result for a *memoryless* controller but is not universal over cue-history-based reversible phenotypes.

## 5. The strong result that survives unlimited memory

For every environmental state and every scalar shared phenotype,

    F_state(x) = C + (a+b)*(x-x_state_star)² >= C.

This is a **pathwise lower bound**, prior to averaging over environments, observing cues or choosing a phenotype. With nonnegative acquisition, response and memory costs, every one-coordinate plastic policy—including a hypothetical clairvoyant policy—has average loss at least C. Therefore **K<C is sufficient for a separately viable ideal coexpressing two-coordinate architecture to outperform every shared-coordinate policy** in this declared cost-comparison world. This guarantee does not claim that K is biologically measured or that the new module can invade.

For the perfect-cue example a=3, Delta=2, K=1, one finds C(b)=12b/(3+b), crossing at b*=3/11. Above that strict concurrent-demand boundary, ideal modules outperform all one-coordinate plasticity even with arbitrary memory; below it, cost-free perfect plasticity attains C<K. Strategies that avoid *simultaneous* exposure or genuinely increase structural dimension are alternative biological architectures; the lower bound does not apply to those under the same scalar phenotype restriction.

## 6. Cross-repository interpretation and empirical limits

SCH: first identify whether pure function optima actually oppose each other on the *same phenotypic coordinate* and whether those demands operate simultaneously.
BALANCE: compare optimized common-fitness-scale SHARED, PLASTIC and accessible differentiated worldlines; do not assign construction cost K from an unmeasured fitness residual.
SLK: retains ownership of architecture value Phi=R-K, heritable accessibility, invasion, fixation and occupancy.
PAYOFF: supplies this model-specific two-cue memory robustness and environmental cost/turnover mechanisms.
BITA: identify route-specific ecological fitness mechanisms; observed trait interaction and phenotypic response do not prove structural origin.

The Wurmbea observations (marked plants changing sex expression over years, resource-dependent expression 66% vs 42%, and relative female seed advantage 3.7 vs 1.4) do NOT estimate q, rho, C, T, c, M or K. Also, the sex-system split between plants in dioecy is not the model's single coexpressed two-coordinate module. GenBank plastid proximity, including the corrected MR2/MR3 voucher HOLD, does NOT establish a change in heritable nuclear sex architecture.

The legitimate ecological next test measures simultaneous functional overlap separately from environmental predictability, phenotypic reversibility/switching cost and structural formation cost. A reconstruction of historical trait origin remains a distinct later causal gate.

## 7. Verification and claim ceiling

Additive implementation: src/plastic_compromise_memory.py
Tests: tests/test_plastic_compromise_memory.py (37 tests, including direct 64-path enumeration, two-regime regional optima, units, memory-cost and reproducibility controls).
Runner: scripts/run_plastic_compromise_memory.py.

    python -m pytest -q tests/test_plastic_compromise_memory.py
    python scripts/run_plastic_compromise_memory.py --out /tmp/payoff-memory.json

All numerical results are stamped synthetic and do not assert a real biological origin. Prior literature on temporal autocorrelation, information and plasticity includes Lande (2014), DOI 10.1111/jeb.12360, and Mayer et al. (2017), DOI 10.1103/PhysRevE.96.032412. This source-specific robustness extension is not claimed as general novelty over those literatures.
