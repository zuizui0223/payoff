# PAYOFF-B prospective actionability-balance novelty boundary

Date: **2026-10-02**  
Status: **literature-screened boundary; not an exhaustive priority proof**

## Bottom line

Do **not** claim novelty for:

- value of information;
- sequential information acquisition;
- waiting for better information before an irreversible action;
- Bayesian optimal stopping;
- adaptive management with learning;
- real-options logic that waiting can preserve or destroy future options.

These are established.

The narrow prospective PAYOFF-B contribution is the ecological specialization:

> seasonal cue quality can improve while biological actionability declines,
> so the usable value of information can be hump-shaped through a life-history
> sequence. Under the declared reduced model this yields an exact
> information-actionability balance condition, a closed-form optimal commitment
> time under exponential learning/recourse loss, actor-specific commitment-time
> divergence, and a finite interval in which information is worth using even
> though cue accuracy itself improves monotonically.

## Prior-art boundary

### Value of information in ecology

Canessa et al. (2015), *Methods in Ecology and Evolution* 6:1219-1228,
DOI 10.1111/2041-210X.12423, explicitly frame ecological VOI as the expected
benefit of reducing uncertainty relative to the cost of obtaining information.

Williams, Eaton & Breininger (2011), *Ecological Modelling* 222:3429-3436,
DOI 10.1016/j.ecolmodel.2011.07.003, treat information value in adaptive
resource management with sequential actions and future uncertainty.

Therefore PAYOFF-B cannot claim to introduce VOI, sequential learning or
adaptive ecological decision theory.

### Stopping with irreversible action

Lehrer & Wang (2024), *Economic Theory* 78:619-648,
DOI 10.1007/s00199-023-01543-8, study an unknown state in which a decision
maker can stop and take an irreversible action, pay for more information, or
wait.

Therefore PAYOFF-B cannot claim novelty for the general tension between
additional information and irreversible commitment.

### Information has no decision value if it cannot change action

This is a standard decision-analytic property. Environmental VOI work also
distinguishes information value from information that cannot alter subsequent
choice.

Therefore the statement

> perfect information can be behaviorally worthless after complete
> irreversibility

is an ecological illustration / exact special case, not a general new theorem.

## Candidate contribution after the screen

The safe candidate contribution is narrower and model-specific.

### 1. Actionability-discounted seasonal information value

Above the canonical Paper-2 cue-actionability boundary,

    V_A(q)=S q-B.

The stagewise reduced form is

    V(q,r)=r V_A(q),

where r is retained actionability, not raw remaining distance or time.

### 2. Dynamic balance

For

    N(t)=r(t)[S q(t)-B]-C(t),

the interior balance is

    r S q' + r'[S q-B] = C'.

With zero marginal waiting cost,

    S q' / [S q-B] = -r'/r.

This ties a Paper-2 ecological loss geometry to a shrinking-recourse trajectory.

### 3. Closed-form commitment time

For

    q(t)=q0+Delta_q[1-exp(-alpha t)]
    r(t)=exp(-beta t),

the unique no-cost peak is

    t*=log(1+alpha/beta)/alpha.

Two actors observing the same q(t) but having different beta therefore commit
at different times.

### 4. Finite information-use window

For fixed positive deadline cost D,

    use information iff
    K exp(-beta t)[1-exp(-alpha t)] > D.

If D lies below the peak but above zero, information use exists only on a
finite interval even though q(t) increases throughout.

This entry-peak-exit pattern is the most distinctive prospective ecological
prediction.

## What must still be shown before claiming ecological novelty

A strong paper would need at least one natural or experimental system where:

1. cue quality is estimated independently at multiple ordered stages;
2. remaining response opportunity is independently measured or manipulated;
3. cue-linked behavior is measured on a common scale across stages;
4. a q-plus-recourse model predicts behavior better than q alone;
5. ideally, behavior shows the predicted intermediate-stage peak or finite
   use window.

Without that evidence, the current result remains a theoretical ecological
specialization of established decision-theory logic.

## Safe language

Use:

> We specialize sequential value-of-information logic to a seasonal ecological
> setting in which cue reliability improves while the biological response set
> contracts. The resulting reduced model yields an exact actionability-balance
> condition and predicts an intermediate stage at which environmental
> information has maximal behavioral value.

Avoid:

> We introduce value of information to ecology.

Avoid:

> We discover that more information is not always better.

Avoid:

> We introduce optimal stopping under irreversible action.

Avoid:

> Schrödinger's spring is a quantum-mechanical model.

The Schrödinger language is only a communication analogy for a latent seasonal
state whose observability improves while response options disappear.
