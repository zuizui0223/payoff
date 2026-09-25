# Phase–velocity decomposition of temporal buffering

Frozen as a **post-readout mechanistic interpretation** on 2026-09-25.

This note does not retroactively redefine the registered bird holdout test. It
explains why the failed temporal-substitution prediction is structurally
plausible in a moving environmental wave.

## 1. Minimal moving-front identity

Let an environmental front move as

[
E(t)=E_0+v_E t.
]

Let the organism's spatial tracking front move at speed (v_A), with a seasonal
timing shift (z):

[
A(t;z)=A_0+v_A(t+z).
]

The signed spatial mismatch is

[
e(t;z)=E(t)-A(t;z)
      =(E_0-A_0)-v_A z +(v_E-v_A)t.
]

This separates two controls exactly:

[
rac{partial e}{partial z}=-v_A,
]

so timing changes the **intercept / phase offset**, whereas

[
rac{partial}{partial t}e=v_E-v_A,
]

so movement-speed matching changes the **drift / slope** of mismatch through
time.

A fixed timing shift can therefore set mismatch to zero at one time, but when
(v_E
eq v_A) it cannot keep mismatch zero over a sustained interval.

Persistent zero mismatch over an interval requires both:

[
v_A=v_E
]

and a compatible initial phase offset.

This is elementary kinematics, not a claim of mathematical novelty.

## 2. Finite timing capacity buys time, not permanent substitution

If timing adjustment is bounded,

[
|z|le z_{max},
]

the largest spatial offset that timing alone can absorb is

[
B_z=v_A z_{max}.
]

When the animal and environmental fronts have a non-zero speed difference

[
Delta v=v_E-v_A,
]

the maximum additional time that a perfectly directed timing shift can buy
before the same mismatch threshold is reached is

[
T_{m buffer}
=
rac{v_A z_{max}}{|v_E-v_A|}.
]

With the speed ratio

[
u=rac{v_A}{v_E},
]

this becomes

[
T_{m buffer}
=
rac{u z_{max}}{|1-u|}.
]

Thus:

- larger timing capacity extends the buffer;
- the buffer is finite whenever (u
eq1);
- timing becomes especially effective near speed matching because spatial drift
  accumulates slowly;
- timing cannot rescue persistent velocity mismatch indefinitely.

This provides a simple analytic interpretation of the explicit-landscape result
in which phenology creates a temporary bypass and movement later re-enters.

## 3. Why the bird holdout substitution prediction failed

The registered bird holdout treated species timing responsiveness as a possible
substitute for movement-speed matching.

The result was:

[
eta_{q^2	imes h}=+0.0351pm0.0289,quad p=0.225,
]

opposite to the registered negative prediction.

At the same time, the timing-responsiveness main effect was

[
eta_h=-0.300pm0.105,quad p=0.0043,
]

as a secondary descriptive term.

The phase–velocity identity explains this combination naturally.

A species can use timing responsiveness to reduce its **overall phase offset**
(the vertical level of the mismatch surface) while still requiring appropriate
movement speed to control the **rate at which mismatch changes along a moving
environmental wave**.

Therefore

[
	ext{better timing}

otRightarrow
	ext{weaker speed dependence}.
]

Instead, timing and movement can form a division of labor:

[
	ext{timing} ightarrow 	ext{phase / intercept control},
]

[
	ext{movement speed} ightarrow 	ext{propagation / drift control}.
]

## 4. Independent consistency with the Amaral source analysis

The original Amaral et al. analysis independently treated bird migration speed
as environmentally responsive.

Its published analysis code / Table 1 reports that bird migration speed changed
with green-up date anomaly and green-up speed anomaly. Its species-sensitivity
term in the migration-speed model was not negative; the reported standardized
estimate was approximately (+0.119) with a 95% interval spanning zero
((-0.034, 0.203)).

This is not a new PAYOFF confirmatory result. It is prior-source consistency:
the source study itself does not suggest a simple trade-off in which greater
phenological sensitivity removes movement-speed adjustment.

## 5. Revised ecological architecture

The useful hierarchy is therefore:

```text
environmental forcing
    |
    +-- phase / calendar displacement
    |       -> timing responsiveness
    |       -> lowers mean phase error
    |
    +-- spatial propagation / wave velocity
            -> movement speed / route progression
            -> controls mismatch drift
```

Stopover and route-stage changes can act between these levels by changing the
effective movement schedule locally.

This architecture is stronger than a generic statement that organisms have
multiple responses. It predicts that a species may be highly phenologically
responsive and still remain strongly dependent on spatial transport.

## 6. Claim boundary

Licensed:

- timing and speed are structurally non-equivalent in the minimal moving-front
  representation because they alter intercept and drift respectively;
- bounded timing can buy a finite amount of time under non-zero speed mismatch;
- the failed bird holdout substitution test is consistent with this
  phase–velocity division of labor;
- timing responsiveness may improve average tracking without eliminating
  movement-speed dependence.

Not licensed:

- claiming that the post-readout identity was a preregistered prediction;
- claiming empirical support for a positive timing × movement synergy from the
  unsupported positive interaction;
- treating (T_{m buffer}) as an empirically estimated natural value in the
  current bird dataset;
- claiming all natural migration systems follow exactly this linear-front model.
