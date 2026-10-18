# Supplementary Mathematical Note S4 — information/actionability optimum and controller identification

**Paper:** *Environmental predictability alone does not determine seasonal tracking*.  
**Purpose:** Correct mathematical scope and reproducibility of the theory in §§2.1, 2.6–2.7 and Discussion §5.4–5.5. This is a derivation of an elementary reduced model, **not a newly established ecological theorem, calibrated animal model, or fitness result**.

## S4.1. General optimum versus the threshold-normalized witness

Let an organism be able to use a cue of statistical reliability \(q(t)\) at time \(t\geq0\), with \(q_0\geq 1/2\) and \(q_0+\Delta q\leq 1\). Set

\[
q(t)=q_0+\Delta q(1-e^{-\alpha t}), \quad
r(t)=e^{-\beta t},\quad \alpha,\beta>0,\quad \Delta q\geq0,
\]

where \(r(t)\) is the usable fraction of the initially feasible response.
Let \(S>0\) be a reduced state-dependent opportunity scale, \(B\geq0\) an action threshold/loss, and \(C(t)\) direct waiting cost. The reduced opportunity objective is

\[
N(t)=r(t)\{Sq(t)-B\}-C(t).
\]

This is a deliberately specified expected-return proxy, **not** the general Blackwell value of free optional information. If action can be declined with payoff zero, the maximum is taken jointly over this outside option.

When \(C=0\), define \(A_\infty=S(q_0+\Delta q)-B\) and \(D=S\Delta q\). Then

\[
N(t)=e^{-\beta t}\{A_\infty-De^{-\alpha t}\}
\]

and

\[
N'(t)=e^{-\beta t}\left\{(\alpha+\beta)D e^{-\alpha t}-\beta A_\infty\right\}.
\]

The bracket is monotone nonincreasing in \(t\), strictly decreasing when \(D>0\). Its zero, if any, is unique; the only other admissible boundary is \(t=0\), together with the zero-payoff outside action.

- **\(A_\infty\leq0\)**: \(A_\infty-D e^{-\alpha t}\leq0\), so no positive opportunity payoff is available at any finite \(t\); decline action.
- **\(A_\infty>0,D=0\)**: no new accuracy is learned, and \(N(t)\) decays; the best opportunity is immediate.
- **\(A_\infty>0,D>0\)**: put \(R=(\alpha+\beta)D/(\beta A_\infty)\). If \(R\leq1\), \(N'(t)\leq0\) for every \(t\geq0\) and the optimum is immediate. If \(R>1\), a unique interior maximum occurs at \(t^*=\log(R)/\alpha\).

Thus the full piecewise decision is

\[
t^*=\max\left[0,\frac{1}{\alpha}
\log\frac{(\alpha+\beta)S\Delta q}
{\beta[S(q_0+\Delta q)-B]}\right]
\]

only when \(A_\infty>0,D>0\), with the two other cases treated separately.

The simpler expression

\[
t^*_{\rm threshold}=\frac{\log(1+\alpha/\beta)}{\alpha}
\]

holds for \(Sq_0=B\) with \(\Delta q>0\), because then \(A_\infty=D\). It is **not the general optimal decision time** and cannot be used to estimate a universal biological deadline.

Illustrative nonempirical parameter sets, with \(S=10,\alpha=\beta=1\):

| Baseline \(q_0\) | Improvement \(\Delta q\) | Loss \(B\) | Correct decision |
|---|---|---|---|
| 0.50 | 0.50 | 5 | Interior \(t^*=\log2\); cue reliability 0.75 |
| 0.55 | 0.45 | 5 | Interior \(t^*=\log1.8\), not \(\log2\) |
| 0.60 | 0.30 | 3 | Immediate \(t^*=0\), not \(\log2\) |
| 0.50 | 0.10 | 8 | No positive information-return action |

If \(C(t)\) is nonzero, an interior optimum instead solves

\[
r(t)S q'(t)+r'(t)\{Sq(t)-B\}-C'(t)=0,
\]

but a stationary point does not by itself establish a global optimum. The outside option and \(t=0\) must still be compared. These results require the stated exogenous cue trajectory and opportunity decay, not an ecological equilibrium with changing competitor behaviour.

## S4.2. Free optional information and realized predictor error are different

When cue acquisition is costless, post-signal actions remain optional, the feasible actions are unchanged and other players' strategies remain fixed, the optimal expected Bayes payoff with an added cue is at least its value without that cue. The actor can adopt the original policy regardless of the observed signal. Hence such ideal optional information has a nonnegative value.

The observed early-period negative incremental LOYO forecasting skill in Supplementary Table S2 is **not** a contradiction. S2 evaluates a **specific fitted statistical forecasting procedure**, which can overfit or be miscalibrated; it does not optimize across "discard the source cue" and "use the fitted source cue" at the decision time. Nor is that statistical procedure known to have been available to a bird.

## S4.3. Mean phase retention requires a centered cue or an explicit intercept

Let actual signed phase error be \(e\), an observable cue be \(z=e+v\) with \(E[v\mid e]=0\), a fixed prior phase mean \(m\), linear estimated error \(\hat e=m+K(z-m)\), and enacted correction \(u=h\hat e\). Let the local target motion/process innovation be \(w\). Then

\[
e_{\mathrm{next}}=\phi(e-h\hat e)+w,
\]

so

\[
E[e_{\mathrm{next}}\mid e]
=
\phi(1-hK)e-\phi h(1-K)m+E[w\mid e].
\]

The coefficient \(\lambda=\phi(1-hK)\) is therefore the **conditional-mean slope** only when any conditional mean innovation is constant in \(e\). The intercept vanishes only if the prior mean is centered appropriately and innovations have zero mean. In general, the conditional-mean relationship is affine, and neither perceived information \(K\) nor correction fraction \(h\) is separately identified from the product \(hK\).

For a linear Gaussian state and noisy cue, a standard posterior information fraction can be written as \(K=P/(P+R)\), where \(P=\mathrm{Var}(e)\) and \(R=\mathrm{Var}(v)\), with independence and zero noise mean assumed. Then

\[
\operatorname{Var}(e-h\hat e)=P[1-Kh(2-h)].
\]

Under independent process noise with variance \(Q\), the phase variance becomes

\[
P_{\mathrm{next}}=\phi^2P[1-Kh(2-h)]+Q.
\]

By comparison, \(\lambda^2P=\phi^2(1-hK)^2P\). Their difference is

\[
P_{\mathrm{next}}-\lambda^2P
=
\phi^2h^2K(1-K)P+Q,
\]

which is generally **positive even if \(Q=0\)**, because estimation uncertainty remains when \(0<K<1\). Thus using \(V_n=\lambda^{2n}V_0\) requires a truly deterministic scalar recurrence with no new stochastic observation or process innovations; merely setting \(Q=0\) in a noisy-cue controller is insufficient.

## S4.4. Interaction mismatch identity and interpretive limit

For two actors with **deterministic, centered and innovation-free** scalar retention \(e_{i,n}=\lambda_i^n e_{i,0}\), set \(m_0=(e_{1,0}+e_{2,0})/2\) and \(\Delta_0=e_{1,0}-e_{2,0}\). Algebra gives the exact identity

\[
\Delta_n
=
(\lambda_1^n-\lambda_2^n)m_0+
\frac{\lambda_1^n+\lambda_2^n}{2}\Delta_0.
\]

This partitions an inherited signed difference and different deterministic controller propagation. It is **not** an additive allocation of demographic fitness deficits to "information", "capacity" and "coordination": action constraints, density dependence, stochastic innovations and competitor responses can introduce interactions and alternative paths.

## S4.5. Executable and manuscript integrity

Source: \`src/paper2_actionability_peak.py\`; test suite: \`tests/test_paper2_actionability_peak.py\`. Unit tests verify boundary and interior regimes, the symmetric counterexample, the two-actor exact identity and the direct waiting-cost first-order condition. None fits or modifies V7R, registered V8, post hoc S2/S3, or Ortega data.

**Publication gate:** A mathematical proof and code match do not independently establish bird cue perception, ecological payoff surfaces or information-limited phenological adjustment.
