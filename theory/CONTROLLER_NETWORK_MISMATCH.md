# PAYOFF-B prospective network controller-discordance theorem

Date: **2026-10-03**  
Status: **prospective post-freeze Paper-2 extension; frozen GEB V2 unchanged**

## 1. From pairs to interaction networks

For actor \(i\), let effective mean phase retention be

\[
\lambda_i=\phi_i(1-G_i g_iK_i).
\]

Suppose all actors are initially synchronized at the same signed seasonal error

\[
e_{i,t}=m_t
\]

and receive the same subsequent environmental innovation.

After one controller step,

\[
e_{i,t+1}=\lambda_i m_t+w_t.
\]

For an undirected weighted interaction network with edge weights
\(a_{ij}\ge0\), define total edge weight

\[
W=\sum_{i<j}a_{ij}
\]

and mean squared interaction mismatch

\[
\mathcal M_{t+1}
=
\frac{1}{W}
\sum_{i<j}
a_{ij}
(e_{i,t+1}-e_{j,t+1})^2.
\]

Because the common innovation cancels,

\[
e_{i,t+1}-e_{j,t+1}
=
m_t(\lambda_i-\lambda_j).
\]

Therefore

\[
\boxed{
\mathcal M_{t+1}
=
m_t^2
\frac{
\sum_{i<j}
a_{ij}(\lambda_i-\lambda_j)^2
}{W}.
}
\]

## 2. Graph-Laplacian form

Let \(L\) be the weighted graph Laplacian and
\(\boldsymbol\lambda\) the vector of actor retentions. Then

\[
\sum_{i<j}
a_{ij}(\lambda_i-\lambda_j)^2
=
\boldsymbol\lambda^\top
L
\boldsymbol\lambda.
\]

Hence

\[
\boxed{
\mathcal M_{t+1}
=
m_t^2
\frac{
\boldsymbol\lambda^\top
L
\boldsymbol\lambda
}{W}.
}
\]

The quantity

\[
D_\lambda
=
\frac{
\boldsymbol\lambda^\top L\boldsymbol\lambda
}{W}
\]

is the **controller discordance** seen by the interaction network.

The graph identity is standard. Its ecological meaning here is that climate
forcing does not translate into community mismatch according to the marginal
distribution of controller types alone. It depends on which different
controllers are connected by ecological interactions.

## 3. Complete-network special case

For an unweighted complete graph with \(N\) actors,

\[
\sum_{i<j}
(\lambda_i-\lambda_j)^2
=
N
\sum_i
(\lambda_i-\bar\lambda)^2.
\]

With population variance

\[
\operatorname{Var}_{pop}(\lambda)
=
\frac1N
\sum_i(\lambda_i-\bar\lambda)^2,
\]

and \(W=N(N-1)/2\),

\[
\boxed{
D_\lambda
=
\frac{2N}{N-1}
\operatorname{Var}_{pop}(\lambda).
}
\]

In a fully connected community, controller variance itself determines
one-step mismatch from a common shock.

## 4. Binary controller states recover the existing network-cut result

Suppose every actor has one of two effective retentions
\(\lambda_0,\lambda_1\).

Only edges joining unlike controller states contribute, so

\[
\boldsymbol\lambda^\top L\boldsymbol\lambda
=
(\lambda_1-\lambda_0)^2 C,
\]

where \(C\) is the total weight of edges crossing the two controller states.

Thus

\[
\boxed{
D_\lambda
=
(\lambda_1-\lambda_0)^2\frac{C}{W}.
}
\]

The earlier PAYOFF-B network-cut geometry is therefore recovered as the binary
special case of a continuous controller-discordance field.

This unifies:
- discrete asynchronous cue uptake;
- continuous differences in information/control retention.

## 5. Topology matters even when the controller distribution is unchanged

Consider four actors on a path with controller multiset

\[
\{0,0,1,1\}.
\]

If similar controllers are adjacent,

\[
0-0-1-1,
\]

only one edge contributes controller discordance.

If the same values alternate,

\[
0-1-0-1,
\]

all three edges contribute.

The marginal controller distribution is identical, but network mismatch differs
threefold.

Therefore:

> **Community vulnerability depends on the placement of controller differences
> across interaction edges, not only on how heterogeneous the species are.**

## 6. Ecological interpretation

The full post-freeze chain can now be written

\[
\text{cue information}
\rightarrow
(K_i,g_i,\phi_i)
\rightarrow
\lambda_i
\rightarrow
\boldsymbol\lambda^\top L\boldsymbol\lambda
\rightarrow
\text{interaction mismatch}.
\]

A common climate anomaly excites a common phase-error mode. Heterogeneous
controllers convert that common mode into edge-level mismatch.

This supplies a continuous mechanistic analogue of asynchronous information
uptake.

## 7. Relation to coordination recovery

The controller-discordance theorem concerns mismatch **generation** under
shared forcing.

The earlier Paper-2 game concerns mismatch **persistence and recovery** after
actors occupy different timing states.

Network topology therefore enters twice:

1. through the edges across which controller differences create mismatch;
2. through strategic interaction structure that can stabilize or rescue timing
   conventions.

These are distinct mechanisms and should not be merged into one parameter.

## 8. Prospective natural test

A direct community test needs:
- actor-specific phase-retention estimates on a common temporal coordinate;
- an independently specified interaction network;
- a shared environmental anomaly or common-mode phase error;
- downstream pairwise mismatch.

The prospective prediction is that network-weighted mismatch should scale with

\[
m_t^2 D_\lambda
\]

better than with unweighted controller variance alone when the interaction
network is sparse or modular.

## 9. Novelty boundary

Graph Laplacian Dirichlet energy and the complete-graph variance identity are
standard mathematics.

PAYOFF-B should claim only the ecological synthesis:

> **heterogeneous readiness/information/control becomes community phenological mismatch
> according to the network Dirichlet energy of the controller field, with the
> earlier binary network-cut result as a special case.**

No current natural community dataset in PAYOFF-B directly validates this
network-controller prediction.
