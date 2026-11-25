# Wave 19 — nested opportunity and information loss

Separate theoretical development; no biological fit, no primary effect admission, no change to Wave 18 or frozen manuscripts.

For finite environmental states H with prior p, let W(H,a) be net-free performance of a terminal option, and let C(H,a) >= 0 be its correction cost. A fixed initial commitment defines a nonempty feasible subset A(H). To avoid granting a partially informed decision maker knowledge of H, require its signal-dependent action to lie in the intersection of A(H) over states with positive posterior probability. Assume each such intersection is nonempty. The following values refer to the same fixed initial commitment, not optimized different initial policies:

V0 = E[max over all terminal options W0(H,a)] (reference environment payoff, separately defined).
V1 = E[max over all terminal options W(H,a)] (changed environment, unconstrained oracle).
V2 = E[max over a in A(H) (W(H,a)-C(H,a))] (feasible informed oracle).
V3 = E_signal[max over posterior-feasible a E[W(H,a)-C(H,a)|signal]] (actual information policy optimum).

V1 >= V2 >= V3 by set inclusion, nonnegative cost and conditional max inequality. V0-V3 = (V0-V1)+(V1-V2)+(V2-V3). The first term is signed environmental performance change, not necessarily a deficit. The second is feasibility/cost loss; third is information loss conditional on the same feasible action and cost structure. These are nested counterfactuals, not an invariant causal attribution or a game equilibrium decomposition. Strategic coordination requires a separately defined equilibrium and welfare criterion; it cannot be silently added. Signal refinement weakly increases V3 if feasible actions remain posterior-safe (Blackwell refinement); costs of acquiring information are excluded here.

## Exact two-state witness

Equal prior, two options, reference matched performance 1, changed matched performance 0.6, mismatched 0.1, matching correction cost 0.2, mismatching cost 0, both options feasible. Symmetric signal accuracy q in [0.5,1]. V0=1, V1=0.6, V2=0.4, V3=0.1+0.3q. Thus even perfect information leaves 0.6 total loss; improving q from 0.5 to 1 recovers only 0.15. The optimal signal policy follows the signal, with ties at q=0.5. No claim this parametrization is fitted or novel prior art.

A separate warning: a better signal cannot lower optimal expected net performance under unchanged feasible options and costs, but may coexist with worse absolute performance across environments. Cross-environment comparisons do not identify information loss without holding the payoff landscape and feasible options fixed.

## Ecological bridge

Lue Wave 17 observed maxima are descriptive proxies for V1, not true oracles; no signal, correction cost or choice data identify V2/V3. Weir Wave 16 hypothetical held-out policy compares information-dependent selection under fixed measured options, not observed switching. Pardikes Wave 18 remains blocked on original four CSVs; factorial composition contrast can address performance moderation but cannot alone identify V3. No pooling or promotion to primary theta. Next input remains official Dryad ZIP 10.5061/dryad.02v6wwq5k.

Validation: six synthetic ordering checks and three witness values computed in JavaScript; no biological observations, no CI run. This is a deliberately simplified fixed-commitment model, not the full dynamic Bellman or Bayesian game.
