# PAYOFF-B dual-use information novelty audit

Date: **2026-10-01**  
Status: **literature-boundary audit; no empirical claim change**

## Question

What part of the dual-use information theorem is actually new enough to claim,
and what is already established in decision theory, value-of-information
theory, migration ecology and strategic information acquisition?

## Established territory

| Established idea | Representative source | Consequence for PAYOFF-B |
|---|---|---|
| Sequential information can have endogenous value because one observation changes whether more information should be acquired | Miller 1975 | Do not claim novelty for sequential VOI |
| VOI from multiple uncertainty sources is generally non-additive | Samson, Wirth & Rickard 1989 | Do not claim generic additivity; PAYOFF-B's additive split requires the declared separable loss structure |
| Stopping/waiting problems can have information-dependent threshold policies | Bhattacharjya & Deleris 2014; Lehrer & Wang 2024 | Do not claim novelty for wait-versus-act thresholds |
| VOI with multiple downstream decisions has a general graphical theory | van Merwijk, Carey & Everitt 2022 | Do not claim novelty for information affecting several decisions |
| Ecological VOI and fitness value of information are established | Donaldson-Matasci et al. 2010; Williams et al. 2011; Canessa et al. 2015 | Do not claim a new general ecological VOI concept |
| Information acquisition can interact with strategic coordination | Liao & Szkup 2026 | Do not claim novelty for “information acquisition × coordination failure” in general |
| Stopover sites can be information sources | Winkler et al. 2014 | Do not claim novelty for information gathered during migration |
| Route predictability changes optimal migration progression | Bauer et al. 2020 | Do not claim novelty for predictive connectivity affecting migration timing |
| Migrants can compensate en route by changing speed and stopover use | Ortega et al. 2023 | Do not claim novelty for temporal compensation during migration |

## Narrow candidate contribution

The defensible candidate contribution is the **information-deadline geometry of
a self-created downstream compensation burden**.

The focal seasonal cue is acquired only by waiting. Waiting creates a
downstream compensation problem. The same cue can also improve the choice of
compensation. Therefore cue quality affects both sides of the waiting
inequality:

[
V_A(q)>J+R_C(q).
]

Equivalently,

[
V_A(q)+V_C(q)>J+R_{C0}.
]

The candidate contribution is not the sum itself. It is the ecological
construction and its deadline-specific exact consequences:

1. **cue-dependent effective deadline cost** — the focal cue lowers the cost
   created by waiting for that cue;
2. **no pure self-rescue** — compensation information alone cannot rationally
   justify creating the delay that generates the compensation problem;
3. **irreducible direct waiting cost** — perfect dual-use information cannot
   overcome (Jge R_{A0});
4. **exact rescue interval** — action information alone can be never-wait while
   dual-use information yields a finite threshold for
   (Jin[max(0,R_{A0}-R_{C0}),R_{A0}));
5. **fixed-(D_{eff}) applicability condition** — the original closed-form
   information deadline is valid only when the focal cue does not materially
   change the downstream compensation policy or when a cue-independent
   (D_{eff}) has already been identified.

## Strongest safe novelty sentence

> Existing theory establishes sequential value of information, multi-decision
> information value, stopping thresholds and strategic information acquisition.
> PAYOFF-B's narrower contribution is to place a compensation decision inside
> the ecological cost of waiting for a seasonal cue and derive the resulting
> information-deadline geometry, including a cue-dependent effective waiting
> cost, a no-self-rescue condition and an exact regime in which compensation
> information converts never-wait into a finite cue-use threshold.

## What should not be claimed

Do not write that PAYOFF-B introduces:

- value of information;
- sequential information acquisition;
- multi-decision information value;
- information-dependent stopping thresholds;
- information acquisition in coordination games;
- information use at migratory stopovers;
- en-route compensation.

Those claims would be too broad.

## References

- Miller AC (1975) The Value of Sequential Information. *Management Science*
  22:1–11. DOI: 10.1287/mnsc.22.1.1.
- Samson D, Wirth A, Rickard J (1989) The value of information from multiple
  sources of uncertainty in decision analysis. *European Journal of
  Operational Research* 39:254–260. DOI: 10.1016/0377-2217(89)90163-X.
- Bhattacharjya D, Deleris LA (2014) The Value of Information in Some
  Variations of the Stopping Problem. *Decision Analysis* 11:189–203.
  DOI: 10.1287/deca.2014.0298.
- Lehrer E, Wang T (2024) The value of information in stopping problems.
  *Economic Theory* 78:619–648. DOI: 10.1007/s00199-023-01543-8.
- van Merwijk C, Carey R, Everitt T (2022) A Complete Criterion for Value of
  Information in Soluble Influence Diagrams. *AAAI* 36:10034–10041.
  DOI: 10.1609/aaai.v36i9.21242.
- Donaldson-Matasci MC, Bergstrom CT, Lachmann M (2010) The fitness value of
  information. *Oikos* 119:219–230. DOI: 10.1111/j.1600-0706.2009.17781.x.
- Williams BK, Eaton MJ, Breininger DR (2011) Adaptive resource management and
  the value of information. *Ecological Modelling* 222:3429–3436.
  DOI: 10.1016/j.ecolmodel.2011.07.003.
- Canessa S et al. (2015) When do we need more data? A primer on calculating
  the value of information for applied ecologists. *Methods in Ecology and
  Evolution* 6:1219–1228. DOI: 10.1111/2041-210X.12423.
- Liao X, Szkup M (2026) Coordination with sequential information acquisition.
  *Theoretical Economics* 21:132–166. DOI: 10.3982/TE5938.
- Winkler DW et al. (2014) Cues, strategies, and outcomes: how migrating
  vertebrates track environmental change. *Movement Ecology* 2:10.
  DOI: 10.1186/2051-3933-2-10.
- Bauer S, McNamara JM, Barta Z (2020) Environmental variability, reliability
  of information and the timing of migration. *Proceedings of the Royal
  Society B* 287:20200622. DOI: 10.1098/rspb.2020.0622.
- Ortega AC et al. (2023) Migrating mule deer compensate en route for
  phenological mismatches. *Nature Communications* 14:2008.
  DOI: 10.1038/s41467-023-37750-z.
