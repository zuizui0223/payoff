# Wave 14 — completed family-balanced thermal/food compensation reanalysis

2026-11-25. Draft PR #426. Secondary analysis of Burraco, Laurila & Orizaola (2021), Oikos 130:231–239, DOI 10.1111/oik.07919; data DOI 10.6084/m9.figshare.13089020.v1. Original collection in 2011, eleven full-sibling clutches; distinct documented year from the 2012 priority competition experiment. Immune-study cohort overlap remains unresolved. One room per temperature, so temperature and room effects are inseparable. Published results known before reanalysis; no new preregistration or novelty claim about the general environmental constraints.

## Source and completed analysis

Authenticated workbook 87,598 bytes; provider MD5 d492e35ec5d8ebb038449cbd83efe595 and SHA256 10d4be0c29be5b767ceddd44c014ed1f704f95c3a1b87eddfae1d96dd091de53. Parser and eligibility HOLDs retained: empty sheets, title-prefaced header, four unexplained asterisk marks, duplicate vial label with distinct design keys, and one zero recorded duration. All 787 composite keys unique. Five absent planned slots all in 12-day/cold/limited condition. Do not infer missing individuals died. One zero duration excluded from paired time/mass endpoint only; recorded survival kept. Strict mode excludes both duplicate-vial rows (785 recorded survival flags, 693 complete duration/mass pairs); observed mode retains both distinct keys (787 flags, 694 complete pairs); strict-unmarked excludes four additional starred rows (781 flags, 689 complete pairs). All 11 families meet full 12-cell support in all modes. Original data unchanged, no imputation.

Whole-family equal-weight means and 10,000 bootstrap draws per endpoint/mode, all 12 cells resampled together. Bootstrap conditional on observed rooms and families, not replicated temperature inference. Duration/mass conditional on survival and paired observation. Survival separately uses observed 0/1 flags and intended-slot worst/best-case bounds.

## Strict mode results

Delay-associated duration differences (days, delayed minus control); mass log ratio, survival risk difference in percentage points. Approximate conditional percentile intervals and all sensitivities saved in JSON.

| Room/food | 6-day duration | 12-day duration | 12-day mass log ratio | 12-day survival difference (pp) |
|---|---:|---:|---:|---:|
| 19°C/full | -5.155 | -8.515 | +0.043124 | -10.606 |
| 19°C/limited | -9.315 | -1.052 | -0.091044 | -4.545 |
| 15°C/full | -5.173 | -7.427 | +0.000806 | -6.061 |
| 15°C/limited | +0.336 | +21.023 | -0.065238 | -14.242 |

The 12-day cold-limited contrast on duration is +21.022727 [15.886174,26.324394]; survival difference -14.2424 pp [-26.9697,-2.1212]; observed-family mean survival 89.3939% in normal versus 75.1515% in delayed. Because the five missing planned records occur in the delayed cold-limited cell, the intended-slot survival difference is bounded by -21.2121 to -13.6364 pp under extreme unknown outcomes, not an imputed effect. Survivor mass log ratio -0.065238 [-0.114341,-0.020243].

For six-day nominal treatment, food restriction changes the duration contrast by -4.160606 days in the warm room and +5.509091 in the cold room. For twelve-day nominal treatment, +7.463636 and +28.450000 days, respectively. Thus duration three-way contrast (cold minus warm of food-restriction effect on delay-associated duration) +9.669697 [5.130303,13.793939] and +20.986364 [14.992386,26.507652]. The direction is maintained in all three modes and leave-one-family-out point sensitivities. Six-day estimates range 8.543939–9.798485; twelve-day 19.860606–20.986364 across modes. This describes nonadditive effects in the two rooms. It cannot establish independent causal temperature or temperature-by-treatment effects.

Survival and mass endpoints are separate: warm/full twelve-day treatment shortens observed larval period by 8.52 days but observed survival is lower by 10.61 pp (conditional interval reaches zero at numerical precision); do not assert full compensation or no fitness costs. Six-day warm/limited has stronger developmental acceleration, but mass among complete survivors lower. Mass and survival do not uniformly track duration. No actual individual hatch dates or partner-relative phase observed. Nominal recovery ratio is a scaling of duration change by assigned cold days, not actual calendar compensation or phase retention. No causal mediation.

## Reproduction and decision

Run https://github.com/zuizui0223/payoff/actions/runs/45549838769, job 138988110077, artifact 14993515090; upload ZIP SHA256 6d36a5fb5a5740678cd1739212350ab022191f54b4eb80a973ab76ab69128e94. Exact aggregate results in data/payoff_b_burraco_thermal_family_fit_wave14_result_20261125.json. Synthetic arithmetic check passed; independent cell-contrast arithmetic rechecked from returned means, not separate fit implementation. ZIP digest from upload log, ZIP not independently downloaded. All earlier source receipts and holds retained. No new primary eligible theta, no pooled meta-analysis and no merge or frozen manuscript changes.

Next scientific priority: source-verified cross-system experiment in which timing and corrective opportunity can be independently identified, with an observed partner/resource target and fitness endpoint. Current thermal, competition and immune experiments support a secondary developmental-compensation synthesis, but must not be relabelled as three independent primary effects. A model of conditional compensation can be formulated separately without claiming those data establish actual mismatch or lifetime fitness.
