# Streptomyces matched-S negative recovery v1

Lane: **A only**.

Question:

> Has the existing *Streptomyces coelicolor* literature already produced a matched, stable `S` colony/lineage in which terminal genomic differentiation into antibiotic-hyperproducing specialists is specifically suppressed while the relevant background and net task are preserved?

Current answer:

```text
NO CERTIFIED MATCHED-S CANDIDATE RECOVERED IN THE AUDITED CANDIDATE SET.
```

This is a focused negative recovery, **not** a proof that no such strain exists anywhere.

## 1. The additional identifiability problem

The observed specialist fraction is not the same estimand as the specialist-generation rate.

In a minimal one-generation bookkeeping model let

```text
mu = fraction entering the specialist state
r  = realized specialist survival/output relative to the generalist state
F  = observed specialist fraction after realization
```

Then

```text
F = mu*r / ((1-mu) + mu*r).
```

For any strict interior `F` and any strict interior candidate `mu`, one can choose

```text
r = F(1-mu) / (mu(1-F))
```

and obtain exactly the same observed `F`.

Therefore:

```text
lower observed specialist frequency
    does not identify
lower differentiation-generation rate.
```

A matched-S claim must distinguish suppression of **generation** from selective loss, poor growth, poor sporulation, or other post-generation filtering of specialist descendants.

## 2. Candidate audit

### ΔparE — strongest apparent reduction, but wrong estimand

Primary source:

```text
Wang et al. 2013, Nucleic Acids Research
DOI 10.1093/nar/gkt752
```

Reported result:

```text
parent 3456 Cml-sensitive derivatives: 0.28% (9/3200)
3456ΔparE:                         <0.03% (0/3200)
parE complementation:               0.36% (8/2100)
```

This looks superficially attractive as an S-like perturbation.  However, the same study shows that Topoisomerase IV is required for maintenance/partitioning of **circular** replicons.  The authors interpret the reduced recovered Cml-sensitive class as loss of viable circularized chromosome derivatives, not as a direct measurement that terminal-deletion events were generated less often.

In addition, ΔparE has strong pleiotropy:

```text
slower growth on multiple media
retarded sporulation on SFM
abnormal chromosome partitioning
anucleate spore compartments
```

Hence:

```text
DELTA_parE
    = survivor/maintenance filter + growth/sporulation pleiotropy
    != identified suppression of specialist generation.
```

Status:

```text
DELTA_PARE_MATCHED_S_CERTIFIED = FALSE
```

### ΔrecA — DNA repair/recombination perturbation

Primary source:

```text
Huang et al. 2006, Journal of Bacteriology
PMID 16980478
```

The recA-null strains establish that RecA can be deleted in *S. coelicolor*, but the mutation causes recombination/repair defects, minute low-viability colonies and sporulation abnormalities.  No direct test identifies a reduced terminal-specialist generation rate while holding post-generation realization fixed.

Status:

```text
DELTA_RECA_MATCHED_S_CERTIFIED = FALSE
```

### tap/tpg disruption — opposite direction

Primary source:

```text
Bao & Cohen 2003, Genes & Development
DOI 10.1101/gad.1060303
```

Tap/Tpg support linear telomere replication.  Tap ablation produces telomere deletion, chromosome circularization and subtelomeric amplification.  This is the opposite of the required matched-S perturbation.

Status:

```text
TAP_TPG_MATCHED_S_CERTIFIED = FALSE
```

### ΔftsK_SC — opposite direction

Primary source:

```text
Role of an FtsK-like protein in genetic stability in S. coelicolor
PMCID PMC1899397
```

Reported Cml-sensitive frequency:

```text
M145 parent:      0.4 +/- 0.1%
ftsK_SC null:    10.6 +/- 0.5%
```

The mutation strongly increases chromosome instability.

Status:

```text
DELTA_FTSK_MATCHED_S_CERTIFIED = FALSE
```

### Δsco2730 — opposite direction plus secondary-metabolism pleiotropy

A recent copper-chaperone/transporter study reports that Δsco2730 increases chromosomal-end-loss frequency to approximately 0.5%, around tenfold above the knockdown/WT controls, while secondary metabolism is also altered.

Status:

```text
DELTA_SCO2730_MATCHED_S_CERTIFIED = FALSE
```

### Sub-MIC tetracycline or gentamicin — context modulation, not an architecture

The caste-ratio study reports lower mutant/caste frequencies under sub-MIC tetracycline and gentamicin than in the drug-free control.  This is useful evidence that caste production is environmentally responsive.

It does not produce a matched S architecture because:

```text
the ecological context itself is changed;
the reduction is modest rather than an isolated OFF state;
the treatment is not a stable/heritable strategic unit;
post-generation selection under antibiotic exposure is not independently removed.
```

This candidate is therefore a **context-manipulation** result, not an S architecture.

### Artificial circularization / large genome reduction — background not matched

Artificial circularization and large subtelomeric deletions remove hundreds of kilobases to megabases and can alter secondary metabolism.  Historical reviews also report artificially circularized Streptomyces chromosomes as more unstable than native linear chromosomes.

These strains cannot be relabeled `generalist-only` because the focal terminal-differentiation mechanism is not isolated from broad genome/background changes.

Status:

```text
CIRCULARIZED_OR_LARGE_REDUCTION_MATCHED_S_CERTIFIED = FALSE
```

## 3. What the search teaches us

The remaining problem is not simply “find a strain with fewer mutants.”

A valid matched S requires all of:

```text
1. direct measurement of terminal-specialist generation;
2. lower generation rate in S than D;
3. matched post-generation specialist survival/realization;
4. matched generalist growth and sporulation;
5. preservation of the relevant reproduction + antibiotic net task;
6. same ecological context;
7. matched genetic/background comparison;
8. focal isolation of the differentiation-generating mechanism;
9. stable/heritable S and D strategic units.
```

This converts the current empirical target from a vague literature search into a precise perturbation problem.

## 4. Strongest current negative result

Within the audited candidate classes, every apparent route fails for a different reason:

```text
ΔparE                    -> survivor filter + pleiotropy
ΔrecA                    -> repair/recombination pleiotropy
Tap/Tpg disruption       -> instability increases
ΔftsK_SC                 -> instability increases strongly
Δsco2730                 -> instability increases + metabolism changes
sub-MIC antibiotics      -> context effect, not stable S
large genome alteration  -> background/focal-isolation failure
```

So the present A-lane status is sharpened to:

```text
STREPTOMYCES_D_ARCHITECTURE_CANDIDATE_STRONG
STREPTOMYCES_MATCHED_S_ARCHITECTURE_NOT_YET_RECOVERED
STREPTOMYCES_DIFFERENTIATION_GENERATION_SUPPRESSION_NOT_IDENTIFIED
STREPTOMYCES_ARCHITECTURE_MAPPING_NOT_YET_CERTIFIED
```

## 5. What would change the status

A decisive candidate would be an otherwise matched strain or lineage in which the propensity to generate terminal deletion specialists is specifically reduced, **with direct generation-rate measurement**, while baseline growth, sporulation and the relevant antibiotic-mediated colony task remain sufficiently matched.

Only after that A-lane comparison is established should an S:D frequency-series experiment be used in Lane G.

No result in this document changes the generic game lane, the raw-data lane, or the E1 architecture-frequency status.
