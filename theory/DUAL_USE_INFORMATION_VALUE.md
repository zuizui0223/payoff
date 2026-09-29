# PAYOFF-B dual-use information value

Date: **2026-09-29**  
Status: **exact binary extension; theory-only**

## Question

A later cue need not be useful only for choosing the seasonal action. If
waiting creates a downstream compensation problem, the same information
package may also reveal **how to compensate for having waited**.

This creates two values of information:

1. action information — which seasonal action better matches the future state?
2. compensation information — which compensatory response minimizes the cost
   created by waiting?

## Balanced binary compensation problem

Let the seasonal-action problem retain the original PAYOFF-B notation, with
prior risk \(R_0\), cue accuracy \(q\), and information value \(V_A(q)\).

Waiting also creates a balanced binary compensation state. Choosing the wrong
compensation response costs \(G\). Before any compensation cue, the best guess
has expected loss

\[
G/2.
\]

A compensation cue of accuracy \(r\ge1/2\) reduces this to

\[
R_C(r)=(1-r)G,
\]

so its information value is

\[
\boxed{
V_C(r)
=
(r-1/2)G.
}
\]

Let \(J\) be a direct nonrecoverable cost of waiting.

The exact waiting condition is then

\[
\boxed{
V_A(q)
>
J+(1-r)G.
}
\]

Equivalently,

\[
V_A(q)+V_C(r)
>
J+G/2.
\]

The same information package can therefore pay twice: once by improving the
seasonal action and once by reducing the downstream cost of compensation.

## Fixed compensation-information quality

For the original seasonal loss scale

\[
A=(1-\pi)C_F,\qquad
L=\pi C_M,\qquad
S=A+L,
\]

and \(q\) above the actionability boundary, the action threshold at fixed
compensation accuracy \(r\) is

\[
\boxed{
q_{\mathrm{wait}}(r)
=
\frac{
\max(A,L)+J+(1-r)G
}{
A+L
}.
}
\]

Thus

\[
\frac{\partial q_{\mathrm{wait}}}{\partial r}
=
-\frac{G}{A+L}.
\]

Better information about **compensation**, even with no change in the quality
of action information itself, lowers the reliability required to justify
waiting.

## One shared accuracy for both uses

Suppose one information package has the same accuracy \(x\) for the seasonal
state and the balanced compensation state.

In the active region,

\[
x(A+L)-\max(A,L)
>
J+(1-x)G.
\]

Therefore

\[
\boxed{
x_{\mathrm{wait}}
=
\frac{
\max(A,L)+J+G
}{
A+L+G
}.
}
\]

Waiting is possible at perfect information iff

\[
J<R_0.
\]

This condition is independent of \(G\): perfect compensation information can
remove compensation uncertainty, but it cannot erase direct waiting cost.

## Rescue by dual-use information

The distinction produces a regime that does not exist in the action-only
model.

Without compensation information, the compensation uncertainty \(G/2\) acts
like an additional fixed cost. Action information alone can never justify
waiting when

\[
J+G/2\ge R_0.
\]

Yet shared dual-use information can still produce a finite threshold whenever

\[
J<R_0.
\]

Hence there is a non-empty region

\[
\boxed{
J<R_0\le J+G/2
}
\]

in which:

- action information alone can never make waiting worthwhile;
- the same cue becomes worth waiting for when it also identifies the appropriate
  downstream compensation.

## Canonical witness

Use

\[
\pi=0.4,\quad
C_F=2,\quad
C_M=1,
\]

so

\[
R_0=0.4,\qquad
\max(A,L)=1.2,\qquad
A+L=1.6.
\]

Let

\[
J=0.20,\qquad G=0.60.
\]

Without compensation information,

\[
J+G/2=0.50>R_0,
\]

so even perfect action information is not worth waiting for.

With one shared dual-use information package,

\[
x_{\mathrm{wait}}
=
\frac{1.2+0.2+0.6}{1.6+0.6}
=
\frac{2.0}{2.2}
\approx0.9091.
\]

Thus information about compensation converts a **never-wait** system into one
with a finite information-use threshold.

## Ecological interpretation

This extension is relevant whenever waiting creates a problem whose solution is
itself state-dependent.

Examples include:

- a migrant that waits for environmental information and later chooses whether
  to compensate through faster travel, stopover compression or post-arrival
  buffering;
- a breeder that delays commitment and later chooses how much reproductive
  effort to invest;
- interacting species that learn not only the future environmental state but
  also which recovery route is least costly.

The result sharpens the hidden-deadline extension. Environmental information can
affect seasonal coordination through at least three channels:

\[
\text{information}
\rightarrow
\begin{cases}
\text{better seasonal action},\\
\text{better estimate of waiting cost},\\
\text{better compensation choice}.
\end{cases}
\]

These channels should not be collapsed into a single empirical correlation.

## Claim boundary

The theorem is exact for the declared balanced binary compensation problem.
PAYOFF-B does not currently claim that any natural system has measured both
information values directly.

The result is therefore a prospective mechanism, not an empirical
reinterpretation of the existing bird datasets.
