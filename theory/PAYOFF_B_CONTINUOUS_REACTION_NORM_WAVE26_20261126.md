# Wave 26 — continuous reaction norms expose a boundary of the binary cascade
2026-11-26. Design registered before execution at e5075141e5549f8ee4ba0bb118a766b5963caa86. Synthetic theoretical robustness analysis only; no primary empirical admission or changes to earlier branches.

## 1. Continuous model and exact potential

H is 0 or 1 with equal probability. S_i in {0,1} is a symmetric private cue correct with probability q_i. Given H, joint correctness probability P(both correct)=q_A*q_B+lambda*(min(q_A,q_B)-q_A*q_B), lambda in [0,1]. The cue sign correlation rho=E[(2S_A-1)(2S_B-1)]=4*P(both correct)-2*q_A-2*q_B+1. The coupling parameter is not itself correlation; it interpolates independence to maximal positive coupling given fixed marginal accuracies. At lambda=0, rho=(2*q_A-1)*(2*q_B-1). Cue sharing is an exogenous sensitivity, not an evolved strategy or evidence of perception.

Continuous action a_i in [0,1], payoff U_i=E[1-(a_i-H)^2+k*(1-(a_i-a_j)^2)]-C_i(r_i), response strength r_i in [0,1]. This replaces binary 0/1 match rewards by squared timing loss for intermediate phenotypes. It is one smooth interpolation of the old game, not a uniquely identified biological utility.

Anchored historical timing a_i=r_i*S_i:
U_i=.5+k+q_i*r_i-(1+k)*r_i^2/2+k*(1+rho)*r_i*r_j/2-k*r_j^2/2-C_i(r_i).
At r_i in {0,1}, lambda=0 and C_i(1)=c_i,C_i(0)=0, these are EXACT Wave 22 payoffs; no endpoint payoff was changed.

Centered a_i=.5+r_i*(S_i-.5):
U_i=.75+k+(q_i-.5)*r_i-(1+k)*r_i^2/4+k*rho*r_i*r_j/2-k*r_j^2/4-C_i(r_i).
Baseline r_A=r_B=0 now corresponds to a constant intermediate date, not Wave 22 constant 0. Report changes relative to its own baseline. Squared timing difference M=E[(a_A-a_B)^2] is not binary mismatch probability except for binary dates.

For unrestricted timing intercept a_i=d_i+r_i*(S_i-.5), d_i in [r_i/2,1-r_i/2], add -(d_i-.5)^2-k*(d_i-d_j)^2 to the centered payoff. This follows because the cue and environmental deviations have zero mean. The intercept part of the exact potential is -sum_i(d_i-.5)^2-k*(d_A-d_B)^2; strictly concave and uniquely maximized at d_A=d_B=.5, feasible for every strength. At any Nash equilibrium, holding r fixed, neither player can improve its own intercept; the conditional concave intercept game therefore requires both intercepts .5. Thus centered model is the equilibrium response problem when intercepts can freely adjust without costs; this says nothing about the evolutionary time required for intercept adjustment.

In both models write L_i (q_i or q_i-.5), D ((1+k)/2 or /4), J (k*(1+rho)/2 or k*rho/2), E (k/2 or /4). U_i=base+L_i*r_i-D*r_i^2+J*r_i*r_j-E*r_j^2-C_i(r_i). Exact potential Phi=sum_i(L_i*r_i-D*r_i^2-C_i(r_i))+J*r_A*r_B, because payoff differences under unilateral changes coincide. Not summed welfare. With linear or quadratic nonnegative cost, Hessian has negative diagonal and positive determinant: 2D>abs(J), and convex cost cannot destroy strict concavity. Hence unique constrained Nash equilibrium (= potential maximizer). Smooth local best response is clip((L_i - c_i + J*r_j)/(2D),0,1) for linear cost and clip((L_i+J*r_j)/(2(D+c_i)),0,1) for quadratic cost. For anchored/linear the derivative at zero q_i-c_i+J*r_j is positive for all tested q_i,c_i,r_j; no negative local selection on a newly increased infinitesimal response. Anchored/quadratic similarly has positive slope. This removes the binary delayed-invasion barrier in the tested smooth models. No finite-N continuous genotype dynamics were simulated.

Fixed activation fee C_i=c_i*I(r_i>0) introduces a discontinuity at 0. For any fixed partner response and positive fee, sufficiently small positive mutants are disadvantaged. For arbitrary finite unilateral jumps, set z=clip((L_i+J*r_j)/(2D),0,1); activating is strictly preferred iff (L_i+J*r_j)*z-D*z^2>c_i. When interior, equivalently (L_i+J*r_j)^2/(4D)>c_i with positive numerator slope. Local mutation barrier and global unilateral activation are separate. Exact pure equilibria can be found by enumerating the active supports and boundary/free stationary solutions, then checking full unilateral best responses including inactive response. This is a discrete acquisition decision plus continuous strength, not a proof every real cue has an activation fee.

## 2. All 72 tested contexts

q_A=.9, q_B=.6/.8, k=.3/.5, c_A=c_B=.12; lambda=0/.5/1; anchored/centered; linear/quadratic/fixed cost. Table: counts at global potential maximizer, all 12 settings per model-cost pair. All maximizers are Nash; potential maximizer need not maximize joint payoff or describe reached state.

| Mode / cost | Both positive | B loses vs own baseline | Sum below own baseline | Origin is Nash | Multiple pure Nash |
|---|---:|---:|---:|---:|---:|
| anchored / linear | 12 | 0 | 0 | 0 | 0 |
| anchored / quadratic | 12 | 0 | 0 | 0 | 0 |
| anchored / fixed | 12 | 4 | 0 | 0 | 0 |
| centered / linear | 9 | 6 | 0 | 0 | 0 |
| centered / quadratic | 12 | 6 | 0 | 0 | 0 |
| centered / fixed | 0 | 6 | 6 | 6 | 1 |

Wave22 witness q_B=.6,k=.5,lambda=0,anchored:
binary FF vs CC: deltaU=(+.07,-.23), sum=-.16. Continuous linear-cost equilibrium r=(.604460,.436862), deltaU=(+.226317,+.051794), sum=+.278110. Quadratic cost r=(.591133,.443350), sum=+.338518. Fixed fee r=(.703634,.536036), deltaU=(+.179492,-.028274), sum=+.151217. Therefore the old negative joint payoff conclusion is not robust to simply permitting partial responses under this squared-loss geometry; even retaining the same cost at r=1. Partner loss is more robust than joint-payoff loss, but not universal.

For the anchored fixed-fee witness A has a strictly positive jump advantage and a finite local activation barrier: with B=0, positive payoff change requires r_A between (q_A - sqrt(q_A^2-4*D*c_A))/(2D)=.1527864 and the upper root (outside [0,1]). B at A=0 has maximum gross activation benefit exactly .12, equal to cost (not strict negative global advantage); any r_A>0 increases B's best activation payoff. Distinguish this from a finite-population invasion trajectory.

For freely adjustable midpoint baseline, q_B=.6,k=.5 with linear costs, B's marginal benefit at zero is -.02+J*r_A, where J=.04+.06*lambda. With B=0, A chooses r_A=.28/.75=.373333. B becomes active exactly when lambda>0.2261904762 (tie at boundary has zero best response). At lambda=0/.5/1 the Nash strengths are (.373333,0)/(.374103,.008250)/(.376471,.023529). Cue correlation can permit partial participation without changing either species' marginal cue quality. Joint improvement is +.034844 to +.035571, yet B loses about .0174 to .0175 vs midpoint baseline in all three cases; cue correlation alone does not guarantee recovery of partner welfare.

For centered fixed fee, k=.3, q_B either .6 or .8, all lambda: only A activates r_A=.615385; deltaU=(+.003077,-.028402), sum=-.025325. At k=.5 the origin is Nash in all six cells. For q_B=.8,k=.5,lambda=1 there is also an interior equilibrium (.688995,.583732) with sum change -.036136, whereas origin remains global potential maximizer. Thus cue correlation can create an alternative equilibrium rather than guarantee coordinated welfare gain. No claim of equilibrium selection.

## 3. Audit and next decision

Executed exact active-set enumeration for 72 settings with complete BR checks, 5,184 individual payoff comparisons to independently enumerated environmental/cue outcomes (max error 8.89e-16), 5,184 unilateral potential-difference identities (max error 8.33e-16), 96 Wave22 endpoint checks, 734,472 independent grid potential evaluations (none exceed enumerated maximum within tolerance). Largest equilibrium unilateral regret 5.56e-17. Pure JS executed in tool isolate; reproducible Node .mjs script and full cell-level JSON committed. No CI execution or finite-N continuous-trait trajectories, no new raw biological data. Previous binary results remain valid within their own model, not universal. The earlier rare-mutation re-entry approximation still requires direct recurrent-mutation validation. Pardikes raw-data HOLD unchanged.

Decision: do not headline "strong selection inevitably destroys future adaptation." Use a conditional theory: whether asynchronous cue evolution produces a temporary loss, permanent response barrier, or payoff externality depends on the local shape/entry cost of the reaction norm and cue correlation. The binary cascade is a limiting restricted strategy case. Next compare continuous local mutation and acquisition/response two-coordinate genetics under the same endpoint payoffs, or prioritize empirical identification of activation costs and cue covariance. Avoid another unconstrained simulation sweep until the estimands are defined.
