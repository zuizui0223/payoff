# PAYOFF-B information-deadline theorem map

Date: **2026-09-30**  
Status: **theory routing map; no new empirical claim**

This note routes PAYOFF-B information theory so that special-case formulas are
not used outside their assumptions.

## Step 1 — seasonal-action information value

Let

\[
A=(1-\pi)C_F,\qquad
L=\pi C_M,
\]

\[
S=A+L,\qquad
B=\max(A,L),\qquad
R_0=\min(A,L).
\]

For the symmetric binary seasonal cue,

\[
V_A(q)=\max[0,Sq-B].
\]

The cue becomes action-changing at

\[
q_0=B/S.
\]

All extensions below compare this information value with the fitness cost of
waiting.

---

## Step 2 — is the effective waiting cost fixed with respect to the focal cue?

### YES: fixed effective deadline

If the focal cue does not change the downstream compensation policy or expected
compensation loss, define one effective waiting cost

\[
D_{\mathrm{eff}}.
\]

Waiting occurs iff

\[
V_A(q)>D_{\mathrm{eff}}.
\]

When \(D_{\mathrm{eff}}<R_0\),

\[
\boxed{
q_{\mathrm{wait}}
=
\frac{B+D_{\mathrm{eff}}}{S}.
}
\]

If \(D_{\mathrm{eff}}\ge R_0\), the actor never waits even at perfect
information.

Implementation: src/endogenous_information_timing.py and
src/compensated_information_deadline.py.

### What is D_eff?

Raw waiting time is not the theorem input.

In the direct-plus-compensated model,

\[
\boxed{
D_{\mathrm{eff}}
=
J(\delta)
+
\min_c
\left[
K(c)+M(\delta-c)
\right].
}
\]

Here:

- \(\delta\): raw delay created by waiting;
- \(J(\delta)\): direct nonrecoverable waiting cost;
- \(c\): downstream recovered delay;
- \(K(c)\): cost of compensation;
- \(M(\delta-c)\): loss from residual timing delay.

The total may alternatively be identified directly as a causal fitness effect
of a biologically faithful waiting intervention that allows normal downstream
compensation.

### Hidden future deadline state

If realized effective cost depends on a future state \(H\) not known at
commitment, use

\[
\bar D_{\mathrm{eff}}(\mathcal I)
=
E[D_{\mathrm{eff}}(H)\mid\mathcal I].
\]

The fixed-cost threshold remains valid with
\(D_{\mathrm{eff}}\rightarrow\bar D_{\mathrm{eff}}(\mathcal I)\) only when
the focal cue itself does not change the compensation decision.

Implementation: src/state_dependent_information_deadline.py.

---

## Step 3 — does the focal cue also inform compensation?

### YES: dual-use information

If the same focal cue changes downstream compensation, then

\[
D_{\mathrm{eff}}=D_{\mathrm{eff}}(q).
\]

Do not plug a constant \(D_{\mathrm{eff}}\) into the fixed-cost formula.

Let:

- \(R_{C0}\): compensation loss if waiting occurs but compensation is
  uninformed;
- \(R_C(q)\): compensation loss when the focal cue also informs compensation;
- \(V_C(q)=R_{C0}-R_C(q)\);
- \(J\): direct nonrecoverable waiting cost.

Then

\[
\boxed{
\text{wait}
\iff
V_A(q)>J+R_C(q)
}
\]

or equivalently

\[
\boxed{
\text{wait}
\iff
V_A(q)+V_C(q)>J+R_{C0}.
}
\]

Implementation: src/dual_use_information_value.py.

### Three exact dual-use consequences

1. **No pure self-rescue.** If \(V_A(q)=0\), compensation information alone
   cannot justify creating a delay merely to learn how to repair it.
2. **Irreducible direct cost.** Perfect dual-use information is worth waiting
   for iff \(J<R_0\).
3. **Rescue interval.** Action information alone may give never-wait while
   dual-use information gives a finite threshold:

\[
J\in
[
\max(0,R_0-R_{C0}),
R_0
).
\]

### Multiple conditional recovery decisions

If waiting creates several cue-informed downstream decisions \(j\), then

\[
\boxed{
\text{wait}
\iff
V_A(q)+\sum_j V_j(q)
>
J+\sum_j R_{j0}.
}
\]

At perfect information every conditional module cancels its own prior burden:

\[
V_j(1)=R_{j0}.
\]

Therefore, regardless of the number or severity of conditional recovery
decisions,

\[
\boxed{
\exists q\le1\text{ with waiting optimal}
\iff
R_0>J.
}
\]

When all binary modules are active at the threshold,

\[
q_{wait}
=
1-
\frac{R_0-J}
{S+\sum_j S_j}.
\]

Thus downstream decision complexity changes **how reliable** the cue must be,
but not whether perfect information can overcome the direct cost of waiting.

---

## Step 4 — pairwise asynchronous information use

### Fixed-D_eff pair

For actors with the same seasonal loss scale and finite fixed thresholds,

\[
\boxed{
\Delta q
=
\frac{
|D_{\mathrm{eff},2}-D_{\mathrm{eff},1}|
}{
S
}.
}
\]

This identity is not licensed when the focal cue changes
\(D_{\mathrm{eff}}\).

### Balanced dual-use pair

For the balanced compensation special case, let \(G_i\) be the symmetric
wrong-compensation loss scale and \(J_i\) direct waiting cost.

For every actor with \(J_i<R_0\),

\[
\boxed{
q_i=1-H_i,
\qquad
H_i=
\frac{R_0-J_i}{S+G_i}.
}
\]

\(H_i\) is the actor's **information-waiting headroom**.

If both thresholds are finite,

\[
\boxed{
\Delta q=|H_1-H_2|.
}
\]

Thus asynchronous cue use can arise from different direct waiting costs,
different downstream compensation severity, or both. Raw waiting time need not
differ at all.

### Iso-threshold contour

Different mechanisms can generate the same threshold:

\[
\frac{R_0-J_1}{S+G_1}
=
\frac{R_0-J_2}{S+G_2}.
\]

Equal observed thresholds therefore do not imply equal raw deadlines, direct
costs or compensation problems.

If \(J_i\ge R_0\) for one actor while another has \(J_j<R_0\), asymmetric
information use can persist through \(q=1\).

---

## Step 5 — raw delay is not a threshold coordinate

Even in the cue-independent compensation case, raw waiting duration
\(\delta\) does not generally rank \(q_{\mathrm{wait}}\).

Downstream compensation can erase a raw-delay difference or reverse the
ranking. Migration distance, travel duration or calendar delay is therefore a
valid ordinal deadline proxy only under an additional homogeneity assumption
about \(J,K,M\) and compensatory capacity.

---

## Step 6 — after actor thresholds are known, return to the interaction network

Let

\[
S(q)=\{i:q>q_i\}
\]

be the information-using set.

Network mismatch is generated on edges crossing between \(S(q)\) and its
complement. This is the bridge to the existing network-cut, coordination-trap
and rescue-seed results.

The logical order is

\[
\boxed{
\text{cue quality}
\rightarrow
\text{actor-specific information use}
\rightarrow
\text{asynchronous interaction edges}
\rightarrow
\text{coordination dynamics}.
}
\]

Do not infer the first arrow from network mismatch alone.

---

## Empirical routing checklist

| Question | If yes | If no |
|---|---|---|
| Does the focal cue change downstream compensation? | dual-use theorem | fixed-D_eff theorem |
| Is future waiting cost unresolved at commitment? | use commitment-time conditional expectation | use fixed measured cost |
| Can normal downstream compensation recover delay? | estimate total causal D_eff or J/K/M/C | raw delay still needs a fitness mapping |
| Are two actors being compared? | estimate actor-specific threshold object | single-actor threshold |
| Is one actor never willing to wait at perfect information? | persistent asymmetry possible | finite asynchronous window if thresholds differ |
| Is compensation inferred only from sequential timing correlations? | fail closed | proceed under prespecified causal model |

---

## What is exact versus prospective

Exact in the declared models:

- fixed information threshold;
- hidden-state conditional-expectation extension;
- direct-plus-compensated effective cost;
- raw-delay rank erasure and reversal;
- dual-use waiting rule;
- no-self-rescue and irreducible-J corollaries;
- dual-use rescue interval;
- multi-module perfect-information condition and active-set threshold;
- fixed-cost pairwise window;
- balanced dual-use headroom window.

Prospective in nature:

- clean identification of D_eff for natural information waiting;
- actor-level q_wait in the same system;
- evidence that one focal natural cue jointly informs seasonal action and
  compensation;
- the predicted asynchronous window in an interacting natural pair;
- degradation-recovery network hysteresis.

The routing map expands the theory without upgrading any natural claim.
