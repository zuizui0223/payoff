# Wave 28 — recombination assembles and disrupts seasonal response architectures
2026-11-27. Conditional genetic realization of Wave 27; design registered at 04cf950895f4d159995b42ea7cbbd274624938ab before calculation. Synthetic theory, not an empirical genetic model. Prior frozen analyses and main unchanged.

## Model and exact invasion boundary

The focal population is species A with q_max=.9, fixed partner response product z_B=0, no ancillary benefit and linear response cost, from Wave 27. For k=.3 or .5 define D=(1+k)/4 and r*=(.4-.06)/(2D). Two haploid loci encode x in {0,1} and r in {0,r*}. Haplotype order 00,10,01,11. Log relative fitness g(x,r)=.4*x*r-D*r^2-.06*r-.06*x^2, w=exp(g). The landscapes are (0,-.06,-.1203076923,.0289230769) at k=.3 and (0,-.06,-.1042666667,.0170666667) at k=.5. Both single changes are deleterious and double change beneficial relative to ancestor: reciprocal sign epistasis. This is a deliberately discrete two-locus realization of the continuous payoff landscape, not a result for infinitesimal mutations or a measurement of a real genetic architecture.

After viability selection f^s_h=f_h*w_h/sum(f*w), let D_LD=f^s_00*f^s_11-f^s_10*f^s_01. Recombination changes haplotype vector by R*D_LD*(-1,1,1,-1), preserving both marginal allele frequencies and multiplying LD by 1-R. It creates 11 when D_LD<0 and reduces its frequency when D_LD>0. These are established population-genetic identities. Near ancestral fixation and without mutation,
f'_11=(1-R)*exp(g11)*f11+O(||rare frequencies||^2).
The linearized rare-haplotype map is triangular up to ordering: rare 10 and 01 have multipliers exp(g10), exp(g01), and rare 11 feeds into both singles. Hence rare 11 can invade iff R<R_c=1-exp(-g11), with strict boundary 0.0285088083 at k=.3 and 0.0169218561 at k=.5. Equality requires higher-order analysis. At 11 fixation, rare 10/01 multipliers exp(g10-g11), exp(g01-g11) are <1 and rare 00 multiplier (1-R)*exp(-g11)<1. Thus for R>R_c both monomorphic corners are locally attracting in the mutation-free deterministic map. This is a local stability result, not a global critical initial frequency or an exact finite-N establishment probability.

## Executed experiment

Same two-locus recombination order in all cells, then symmetric mutation, then multinomial Wright-Fisher sampling. N=1,000 or 10,000, fixed sizes; R=0,.005,.02,.05,.1,.5; 2000 generations. With no mutation compare initial coupling (.9,0,0,.1) and repulsion (.8,.1,.1,0), both marginal derived allele frequencies .1. With ancestor-only initial state compare independent locus flips at mu=1e-4 each (double flip probability mu^2) and deliberately perfectly paired flips (double flip probability mu); both have the same marginal per-locus flip rate. The paired regime is a controlled extreme mutational-correlation contrast, not a biological claim of pleiotropic mutations at this rate. It does not hold the number of mutational events or the distribution of event sizes fixed. 96 cells x 256 replicates x 2 seeds = 49,152 trajectories. All conditions retained. A first visit to f11>=.95 is not fixation, especially with mutation. Expected log relative fitness here is not demographic population growth.

At k=.5,N=10000, no mutation, combined counts across two seeds:
| R | Initial coupling hit95 /512 | Initial repulsion ever11 /512 | Initial repulsion hit95 /512 |
|---:|---:|---:|---:|
| 0 | 512 | 0 | 0 |
| .005 | 512 | 493 | 42 |
| .02 | 440 | 512 | 2 |
| .05 | 0 | 512 | 0 |
| .1 | 0 | 512 | 0 |
| .5 | 0 | 512 | 0 |

At R=.02>R_c, a 10% initial 11 frequency can still reach >=95%; at N=10000 deterministic initial coupling reaches 11 fixation but repulsion remains near zero at generation 2000. Local rare-invasion threshold does not imply impossibility of finite-frequency invasion. At k=.3,N=10000,R=.02<R_c, repulsion hit95=121/512, all coupling hit95. Moderate recombination assembles rare double mutants; high recombination creates many without establishment. At N=1000,k=.3,R=.05, coupling hit95=85/512 even though the deterministic coupling path tends toward ancestor, illustrating stochastic crossing; do not claim recombination above threshold always prevents adaptation. Observed 0/512 values are finite-sample outcomes, not exact zero probabilities unless structural (repulsion at R=0 and mu=0).

At k=.5,N=10000 starting 00, R=0, independent mutation ever11=507/512, hit95=43/512; paired mutation ever11=512/512, hit95=512/512. At R=.02, independent ever11=512/512 but hit95=0/512; paired hit95=299/512. At R>=.05 neither mutation regime hits95 in this N,k setting. The appearance and establishment of a genetic combination are separate endpoints. Paired mutation strongly increases direct supply (mu versus mu^2), so these contrasts are not evidence that actual genetic covariance has this effect size.

## Bridge back to interspecies ecology

In the original centered payoff with conditionally independent cues, fixing a partner product z_B changes the focal gain coefficient to .4+J*z_B, J=2*k*.4*(qmax_B-.5). For the same fixed allelic r*, g11(z_B)=g11(0)+J*r* z_B while single-mutant payoffs remain unchanged. Thus R_c(z_B)=1-exp[-g11(0)-J*r* z_B]. For k=.5,R=.02, the exact rare-invasion sign changes at z_B=0.17294342 when qmax_B=.6 and 0.05764781 when qmax_B=.8. These are conditional thresholds; they do not show that the partner reaches those products, or that the reciprocal two-population system reaches its high-response attractor. This provides the concrete next experiment: use each partner's mean x*r as the time-dependent input to the other's four-haplotype selection and test whether recombination-mediated accessibility switches during coevolution, keeping independent/paired mutation and initial linkage disequilibrium distinct.

## Reproduction and scope

Local NumPy 2.3.5 executed both registered seeds and deterministic comparators. Initial streaming-container launch was unsupported; ordinary container execution succeeded with unchanged design. Validation covers recombination marginal preservation and LD decay on 1000 synthetic haplotype mixtures at all six R, no-mutation absorbing boundaries, local rare-double multiplier, mutation marginal rates, hit-before-emergence impossibility and no-double structural null. Script refetched; Git blob 8752c406b4fb467ba7b5839de029b5e1a18e4237 exactly matches local executed script; local SHA256 dc1eb29004df7567377f85766d2adae852cd8c4129bdf3c5e8b2dbbe065f380f. Full result SHA256 01130e2e1a0a2a85885ef3bf2e86970870aa5018897da06c88ea4a5460136b58. Compact all-cell receipt includes both seeds' exact counts and terminal means; full output is reproducible from script. No Actions CI run, no empirical evidence, no real linkage mapping, no novelty claim for the standard recombination-valley mechanism. Fixed partner only; no new direct q×r or primary theta estimates. Pardikes raw-data HOLD remains. Do not merge or reinterpret previous results as general claims.
