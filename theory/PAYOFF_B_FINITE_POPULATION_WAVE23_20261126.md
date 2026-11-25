# Wave 23 — finite population loss and mutation-enabled re-entry of the delayed response

2026-11-26. Separate branch stacked on Wave 22. Synthetic model experiment only; no biological data, manuscript changes, or primary meta-analysis admission.

## Fixed design

Use the Wave 22 witness q1=.9, q2=.6, k=.5, c1=c2=.12, hence s1=.03, s2=-.27, J=.29, A threshold .27/.29. Inherited fixed C and private-information F policies, expected payoffs integrated over environments and signals, no generation-specific environmental shock. Both species have equal fixed census sizes N, synchronous non-overlapping generations, independent binomial offspring sampling conditional on the current pair of frequencies. F relative fitness exp(s_i+J*p_j) vs C fitness 1. After selection, symmetric per-offspring switching mutation mu in either direction. If p is current F frequency then selected frequency f=p*exp(Delta)/(1-p+p*exp(Delta)), next F count ~ Binomial(N,mu+(1-2*mu)*f). Equal initial F frequencies .01 (integer counts 1,10,100); N=100,1000,10000 and mu=0,1e-6,1e-5,1e-4. Horizon 4000 generations, 1024 independent replicates per cell per seed. Cell seeds base+100*i+j with i,j ordered size/mutation index. Main base 20261126 and repeat 20361126; 24576 total runs, NumPy 2.3.5. This WF model differs from the continuous replicator time scale; a deterministic discrete-frequency comparator uses exactly the selection/mutation recursion without sampling.

Endpoints: first crossing p_A> .27/.29; first B F count zero strictly before first A crossing, conditional on A crossing; B reappearance after zero; first simultaneous p_A,p_B>=.95; joint95 at horizon and time fraction occupied; mean terminal sum of expected payoffs. These are strategy-frequency states, not species persistence, fixation under ongoing mutation, demographic growth, or unconditional probabilities beyond the horizon. Payoffs averaged over random cross-species pairing on the stipulated common additive scale. The thresholds are theoretical (invasion) or descriptive (95%); no biological calibration. Conditional time medians exclude trials that never reached the endpoint. All parameter cells reported.

## Executed results

No mutation: A crosses in 67,437,1024 of 1024 for increasing N in main; 64,480,1022 in repeat. In all 3094 of those crossing runs across seeds B had already reached zero. Neither seed has any joint95 event at any sampled N (0/6144 total no-mutation runs; not an exact zero probability). In contrast deterministic discrete no-mutation recurrence hits joint95 at generation 2605 and reaches a minimum B F frequency 1.109e-19. An absorbing lost allele cannot reappear without mutation. No claim of stochastic species extinction. The contrast is robust to the two simulation seeds, not all payoff surfaces or population sizes.

| N | mu | Joint95 ever main / 1024 | Repeat / 1024 | Main median hit generation conditional on hit |
|---:|---:|---:|---:|---:|
|100|0|0|0|NA|
|100|1e-6|1|0|2988|
|100|1e-5|16|20|2905|
|100|1e-4|545|534|2220|
|1000|0|0|0|NA|
|1000|1e-6|65|70|2882|
|1000|1e-5|625|616|2188|
|1000|1e-4|1024|1024|845|
|10000|0|0|0|NA|
|10000|1e-6|734|746|1806.5|
|10000|1e-5|1024|1024|884.5|
|10000|1e-4|1024|1024|651|

At N=10000 and mu=1e-4, 1005/1024 main and 1009/1024 repeat lose B F before A crossing even with mutation; all subsequently hit joint95, including the previously lost-B trajectories. Mutation enables renewed supply in this experiment; it does not require the ancestral F copies to survive. At equal N*mu=.01, joint95 differs substantially across N=100/mu=1e-4, N=1000/mu=1e-5, N=10000/mu=1e-6 (545,625,734 of 1024). Thus N*mu alone is not an observed collapse coordinate at this horizon; both initial copy number and drift/selection also change. No universal scaling law inferred. At N=10000, no mutation mean terminal sum 1.78 vs 1.839956 with mu=1e-5, relative to C,C sum 2: mutation permits partial recovery from the intermediate F,C state but does not restore the original aggregate performance. In this witness, blocking the final cascade can leave the worse intermediate state. Do not equate slower evolution with ecosystem rescue.

## Reproduction and limits

Run python scripts/payoff_b_finite_population_wave23_20261126.py --out result.json and repeat with --seed 20361126. Local Python runs completed with probability/boundary and event-order checks, full output includes Wilson intervals, conditional endpoint counts and trajectory-summary measures. The final script was refetched and Git blob SHA1 c4df8e610c3bff27f20e48ed51c1848ad28e1779 matched the locally executed repeat script. Main run used same numerical path before adding optional seed/replicate flags and base-seed output metadata. Compact result receipt in data/payoff_b_finite_population_wave23_result_20261126.json, exact integer counts and rounded6 secondary summaries; full JSON hashes recorded but full raw trajectory files not committed. No GitHub Actions CI execution. No post-outcome retuning of payoff witness.

Next gate: test additional Wave 22 invasion-path parameter combinations and separate early F loss from later successful mutation establishment with an exact finite-N fixation benchmark. Also audit information sharing and continuous reaction norms before generalizing. The present result is conditional on a binary-policy, fixed-N, constant expected-payoff model, and the only finite-N experiment tested is the Wave 22 witness. No ecological inference about actual mutation rates, generation times or real demographic extinction. Pardikes source HOLD and empirical primary effect count zero remain.
