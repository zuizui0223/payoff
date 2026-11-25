# Wave 22 — costly information strategies, adaptive cascades and joint-payoff loss
2026-11-26. Extends Wave 21 on a separate draft branch. All results below are exact model consequences or synthetic computations, not biological estimates.

## 1. Evolving objects and scope

Two independently well-mixed species populations interact through random interspecific encounters. H is an equally likely binary environment. Each species has two inherited policies: C = retain the same fixed calendar action 0, at zero information cost; F = acquire a symmetric private signal of fixed accuracy q_i in [0.5,1] and follow it, at cost c_i >= 0. Signals conditionally independent given H. Reward per interaction is 1 for matching H and k >= 0 for matching the partner; subtract own acquisition cost for F. These are assumed expected fitness proxies in common additive units, not measured population growth or life-history fitness. This is binary policy evolution, not evolution of continuous precision. The historical calendar convention is fixed; arbitrary alternate calendars, public signals, reaction norms, information acquisition with signal-contingent ignoring, mutation, and finite population sampling are not included in the dynamical model.

Write a_i=q_i-0.5, b_i=a_i-c_i, m=0.5-2*a_1*a_2 and J=k*(1-m). Expected payoff pairs:

C,C: (0.5+k,0.5+k)
F,C: (q_1-c_1+k/2,0.5+k/2)
C,F: (0.5+k/2,q_2-c_2+k/2)
F,F: (q_1-c_1+k*(1-m),q_2-c_2+k*(1-m)).

Mismatch probabilities 0, 0.5, 0.5, m respectively. With p_i frequency of F, selection difference (F minus C) is Delta_i(p_j)=s_i+J*p_j, s_i=b_i-k/2. Positive J is a strategic complementarity in this particular restricted game, not a general claim about acquisition games. The continuous-time two-population replicator system is dp_i/dt=p_i*(1-p_i)*Delta_i(p_j). For J>0 an interior threshold p_j*=-s_i/J exists when s_i<0<s_i+J. Strict local stability of C,C requires s_1,s_2<0 and of F,F requires s_1+J,s_2+J>0. Both stable corners can coexist. Potential Phi=s_1*p_1+s_2*p_2+J*p_1*p_2 has time derivative sum_i p_i*(1-p_i)*Delta_i^2>=0. This potential is NOT sum of payoffs.

## 2. Exact adaptive cascade with a joint payoff decrease

Species 1 invades C,C when b_1>k/2. Species 2 subsequently invades F,C when b_2>-2*k*a_1*a_2. Their sequential strict unilateral improvements do not imply joint benefit. Compared to C,C, F,F changes each payoff by b_i-k*m and the equally weighted sum by b_1+b_2-2*k*m. Thus sufficient strict conditions for the sequential adaptive cascade and a final sum loss are

b_1>k/2;
b_2>-2*k*a_1*a_2;
b_1+b_2<2*k*m.

When these hold, species 1 gains relative to C,C (because m<=0.5) and species 2 loses. At F,F neither single policy change is advantageous. In the restricted deterministic model with both initial F frequencies strictly positive and <1, the first condition gives p_1 -> 1 and the second eventually makes Delta_2 positive and bounded away from zero; hence p_2 -> 1. If p_2 starts at zero it remains zero without mutation. This is not finite-population accessibility. Welfare is an illustrative equal-weight sum in common payoff units; no invariant cross-species aggregation or population viability claim.

Witness q1=.9,q2=.6,k=.5,c1=c2=.12: m=.42, J=.29, s1=.03, s2=-.27. C,C=(1,1), F,C=(1.03,.75), F,F=(1.07,.77). Sum 2 -> 1.78 -> 1.84. Species 2's invasion threshold p1=.27/.29=.93103448. Each step benefits the focal changing species; the eventual pair has a lower sum than the initial pair. The potential strictly increases on both steps (.03 then .02), whereas the sum does not. Under deterministic replicator dynamics with initial p1=p2=.01, species 2's F strategy initially declines to about 1.25e-19 at time 239.6, then returns, reaching .999983 at t=3000. Time is in arbitrary selection units. This illustrates the possibility of a severe rare-variant bottleneck; actual fixation, extinction of a strategy, mutation waiting times and finite-N accessibility require separate tests. No population extinction prediction.

## 3. Reproducible synthetic audit

scripts/payoff_b_costly_information_evolution_wave22_20261126.mjs independently enumerates eight joint environment/signal states for each of four policy pairs and compares analytic payoffs, mismatch and invasion expressions for 146,410 combinations: q1,q2=.5 to 1 in .05 steps; c1,c2=0 to .5 in .05 steps; k=.1 to 1 in .1 steps. Strict comparisons use 1e-10 tolerance. All comparisons passed. 11,639 labeled combinations have the ordered two-step strict invasion path 1 then 2; 611 of those also have negative final summed payoff change; 31,330 have both strict C,C and F,F local attractors. Counts are conditional on this arbitrary grid and not prevalence estimates. RK4 on log odds, with dt=.1 and .05 over t=4000, independently reproduced the minimum timing and final strategy frequencies to stated numeric tolerances. No finite-N simulations. Executed pure JS functions in an isolate, saved exact results to data/payoff_b_costly_information_evolution_wave22_result_20261126.json; no Node CI run. The path count and result should not be relabeled as actual data.

## 4. Novelty and next gate

Information-acquisition inefficiency and equilibrium multiplicity are already established research topics in economics: Yang 2015, Coordination with flexible information acquisition (10.1016/j.jet.2014.11.017); Szkup and Trevino 2015, Information acquisition in global games of regime change (Journal of Economic Theory 160:387–428); Szkup and Trevino 2026, Selection through information acquisition in coordination games (10.1007/s00199-025-01658-0). Phenological mismatch with multiple fitness components also has explicit ecological prior art (Visser and Gienapp 2019, 10.1038/s41559-019-0880-8). A targeted abstract/title screen, not a systematic novelty audit, means no claim that welfare-reducing information acquisition or multiple equilibria are newly discovered. Ecological candidate contribution is a testable model tying independently costly cue strategies to partner-specific phase loss, rare-variant accessibility and measurable absolute fitness, not simply importing these general game-theory results.

Next: test whether these strict invasion-path predictions survive finite N with mutation and continuous/shared cue alternatives, explicitly separate elapsed evolutionary time from population persistence, and avoid claiming ecological confirmation without direct joint measurements. Pardikes original-file HOLD and primary meta-analysis count zero unchanged. No previous manuscript or main modification.
