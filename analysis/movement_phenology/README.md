# PAYOFF-B movement–phenology macro analysis

This directory contains the empirical bridge from the PAYOFF-B anti-phase theorem to macroecological migration/phenology data.

## Core empirical quantities

~~~text
u_macro          = animal front speed / environmental front speed
q                = log(u_macro)
alignment        = cos(animal direction - environment direction)
vector_mismatch  = |v_animal - v_environment| / |v_environment|
~~~

The exact PAYOFF-B model motivates an **order-one finite timescale-matching prediction**. The empirical analysis does not treat the theoretical endpoint constants as a hard acceptance interval.

## Stage-1 data

Download the published Dryad package for Amaral et al. (2025), DOI 10.5061/dryad.ttdz08m6w, and place its data/final.rds at:

~~~text
external/amaral_2025/data/final.rds
~~~

Then run:

~~~text
Rscript analysis/movement_phenology/reanalyse_amaral_payoff_b.R
~~~

Outputs are written under outputs/movement_phenology/.

The Python metric helpers are independently testable with:

~~~text
python -m pytest -q tests/test_movement_phenology_metrics.py
~~~

## Evidence boundary

The Stage-1 response is arrival/green-up mismatch, not fitness. A fitted minimum is therefore a **tracking-performance optimum** conditional on the observational design, not direct proof of an evolutionary optimum.
