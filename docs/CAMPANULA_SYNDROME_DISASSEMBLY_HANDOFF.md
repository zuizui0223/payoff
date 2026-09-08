# Campanula syndrome-disassembly empirical handoff

Status: empirical side branch / biological handoff. This document does **not** modify the core PAYOFF theorems or claim that the current *Campanula microdonta* data already identify a PAYOFF game.

## 1. Why this system is useful

The Izu-island *Campanula microdonta* system offers a biological case in which several floral functions can be measured on the same individuals and compared across island populations with different historical pollination and mating environments.

The working floral architecture is decomposed into at least three functional modules:

```text
visual-information module
    floral-tube purple spots / candidate nectar-guide signal

mechanical-access module
    corolla size, throat width, opening geometry

reproductive-interface module
    reproductive-organ geometry and mating-assurance traits
```

The empirical interest is not whether all island flowers become uniformly "smaller" or uniformly "selfing-like". The stronger question is whether a formerly integrated floral syndrome can be partially disassembled when the payoff of one or more modules changes.

---

## 2. Upstream mapping to SCH / BALANCE / BITA / PAYOFF

### SCH: shared-function compromise

Treat an integrated ancestral floral phenotype as a shared architecture serving several functions simultaneously, for example:

```text
pollinator attraction / guidance
mechanical pollen transfer
reproductive assurance
resource economy
```

A conflict receipt requires evidence that the same phenotypic coordinate or tightly coupled trait bundle cannot simultaneously optimize all relevant functions in one ecological context.

Current observational island differences alone do not identify this conflict load `L`.

### BALANCE: whether integration is still worth keeping

A historical pollinator shift can change the relative value of maintaining the ancestral integrated architecture.

For a candidate released module,

```text
phi = R-K
```

is the static payoff difference between retaining the ancestral coupling and allowing that module to diverge, where `R` is recovered conflict loss and `K` is the cost of architectural release.

For *C. microdonta*, a plausible but unconfirmed case is that long-term loss of large-bee use reduces the benefit of maintaining a costly visual-guidance module.

### BITA: which module moves independently

The key empirical signature is not simply overall floral reduction. It is residual differentiation after the common size/investment axis is accounted for.

Candidate releases include:

```text
visual signal changes beyond allometric flower-size reduction;
opening geometry changes beyond common size reduction;
reproductive geometry changes beyond both.
```

This is the point at which the system can test whether syndrome evolution is modular rather than a one-axis collapse.

### PAYOFF: whether the new architecture can spread or persist

PAYOFF begins only after architecture payoffs are defined on a common fitness scale.

For two floral architectures `S` and `D`, for example guide-rich and guide-reduced,

```text
Delta(p)=phi+eta(2p-1)
```

requires reproductive payoff measured across architecture frequency `p` or an independently justified natural analogue.

Current phenotype + population-genetic data do not identify `eta`.

---

## 3. The syndrome-disassembly hypothesis

The side-branch hypothesis is:

> Pollination, selfing, and island syndromes can be treated not only as lists of correlated traits but as integrated architectures whose component modules can lose or gain payoff at different rates after ecological change.

For the Izu system:

```text
ancestral integrated floral syndrome
        |
        +--> visual information
        +--> mechanical access
        +--> reproductive interface
        |
        v
pollinator / mating-environment change
        |
        v
module-specific payoff shifts
        |
        v
partial release of coupling
        |
        v
mosaic floral architecture
```

This predicts that some traits can change strongly while others remain near the ancestral state, even under the same island transition.

---

## 4. Connection to pollination syndrome

The PAYOFF-compatible interpretation of a pollination syndrome is an architecture that jointly serves pollinator attraction, handling, contact, and reward acquisition.

A pollinator shift or loss need not move all components together.

The strongest *Campanula* prediction is therefore not:

```text
Bombus absence -> all floral traits decrease.
```

It is:

```text
Bombus absence -> the payoff landscape changes by module,
                  so visual, mechanical, and reproductive traits can decouple.
```

A candidate nectar-guide trait is especially useful because it represents information presented to visitors rather than only mechanical fit.

---

## 5. Connection to selfing syndrome

A selfing syndrome can be treated as the sequential or joint re-optimization of floral modules after pollinator-mediated outcross payoff falls and reproductive-assurance payoff rises.

Possible changes include:

```text
display investment reduction;
visual-guidance reduction;
flower-size reduction;
changes in opening geometry;
changes in reproductive-organ geometry.
```

The PAYOFF-side question is whether these changes arise as one indivisible syndrome or as multiple architecture releases with distinct payoff thresholds.

This turns "selfing syndrome" from a trait checklist into a candidate assembly/disassembly process.

---

## 6. Connection to island syndrome

Islandization is treated as a generator of local payoff environments rather than as a direct causal variable.

For island `j`, relevant drivers can include:

```text
pollinator presence / absence;
alternative visitor guilds;
autonomous-selfing value;
resource and climatic conditions;
colonization history;
gene flow among islands.
```

The local architecture gap can then differ among islands:

```text
phi_j = s_j L_j - K_j.
```

If movement or gene flow matters, the existing PAYOFF environment-mosaic layer can later be used to ask whether local architecture advantages are maintained, rescued, or erased by connectivity.

The claim is therefore not "islands cause spot loss". The stronger mechanistic formulation is:

> islandization changes interaction, mating, and connectivity conditions, which can redistribute payoff among floral modules.

---

## 7. What the present *Campanula* project can already test

The current phenotype + MIG-seq2 / population-history design can address a **pre-PAYOFF architecture-history layer**:

```text
1. Are spot differences larger than expected from a common flower-size axis?
2. Do visual, mechanical, and reproductive traits share one island trajectory or decouple?
3. Did low-spot architecture arise once and spread, or recur on distinct genetic backgrounds?
4. Is repeated low-spot architecture associated with the historical pollinator / mating context more consistently than with neutral relatedness alone?
```

These results can support or reject syndrome disassembly as a historical pattern.

They do not by themselves identify a frequency-dependent architecture game.

---

## 8. What would be needed for a true PAYOFF test

A direct PAYOFF test would require an experimental handoff with independently estimated reproductive payoff.

A minimal design would compare guide-rich and guide-reduced flowers under matched floral size and geometry, ideally in both historical pollinator contexts.

Required receipts include:

```text
architecture definition:
    guide-rich S versus guide-reduced D;

common payoff scale:
    seed set, pollen export, compatible-pollen receipt, or another preregistered fitness component;

frequency manipulation:
    vary p = frequency of D among local flowers;

reciprocal endpoint contrasts:
    Delta(0), Delta(1);

identification:
    phi=(Delta(0)+Delta(1))/2,
    eta=(Delta(1)-Delta(0))/2.
```

A particularly informative result would be `eta>0` in a pollinator-learning context, because it would imply a coordination barrier: a guide pattern could remain stable while common yet become vulnerable after the relevant pollinator interaction disappears.

That mechanism is prospective and must not be inferred from island spot frequencies alone.

---

## 9. Falsification cases

The syndrome-disassembly interpretation is weakened if:

```text
all floral traits collapse onto one size/investment axis with no residual module-specific differentiation;

low-spot populations form one neutral genetic lineage and phenotype divergence tracks ancestry alone;

spot variation has no functional association with visitor guidance or reproductive payoff;

module-specific payoff differences cannot be placed on a common fitness scale;

or frequency manipulations show no architecture-frequency effect where a PAYOFF game is claimed.
```

A strong negative result is still informative: it would support a simpler integrated-syndrome or neutral-history account instead of modular disassembly.

---

## 10. Position in the PAYOFF programme

This file is intentionally a side branch rather than part of the canonical theorem spine.

```text
core PAYOFF theory
    |
    +--> empirical handoff contracts
            |
            +--> Campanula syndrome-disassembly side branch
                    |
                    +--> pollination syndrome
                    +--> selfing syndrome
                    +--> island syndrome
```

Its role is to translate the existing architecture-payoff language into one concrete evolutionary-ecology system and to define what additional data would be required before a biological result can count as a PAYOFF test.

It should remain outside the canonical reader path until an empirical receipt identifies at least one architecture payoff contrast on a common fitness scale.