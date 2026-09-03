# VariantPriorX Internal Prioritization Benchmarking

## Purpose

VariantPriorX was evaluated using internal prioritization sanity checks to determine whether the implemented scoring framework behaves consistently with its intended evidence-based design.

This evaluation is not a clinical diagnostic benchmark and does not measure ACMG/AMP classification accuracy.

Because ClinVar evidence contributes directly to the VariantPriorX score, ClinVar-based score stratification is not an independent validation dataset.

## Benchmark Dataset

The benchmark was performed on the final VariantPriorX candidate set derived from the GIAB HG002 CMRG GRCh38 benchmark genome.

- Total prioritized variants: 497
- Unique variants: 497
- HIGH-impact variants: 55
- MODERATE-impact variants: 442
- Score range: -5 to 7

## Population-Frequency Stratification

Variants with successfully retrieved gnomAD population-frequency evidence were grouped by allele frequency.

| Frequency group | Variants | Median score | Mean score |
| --- | ---: | ---: | ---: |
| VERY_RARE | 15 | 5.0 | 4.60 |
| RARE | 13 | 4.0 | 3.46 |
| LOW_FREQUENCY | 23 | 0.0 | 1.04 |
| UNCOMMON | 34 | -2.0 | -1.88 |
| COMMON | 390 | -5.0 | -3.32 |

The observed score gradient is consistent with the intended prioritization logic: rare variants generally receive higher prioritization scores, while common variants are strongly deprioritized.

This result should be interpreted as an internal scoring sanity check because population frequency is itself one component of the VariantPriorX score.

## ClinVar Stratification

| ClinVar group | Variants | Median score | Mean score | Maximum | Minimum |
| --- | ---: | ---: | ---: | ---: | ---: |
| CONFLICTING | 8 | 2.5 | 2.25 | 5 | 0 |
| VUS | 3 | 0.0 | -0.33 | 0 | -1 |
| OTHER | 206 | -1.0 | 0.51 | 7 | -1 |
| BENIGN / LIKELY BENIGN | 280 | -5.0 | -4.52 | 2 | -5 |

Benign and likely benign ClinVar records were strongly shifted toward negative prioritization scores.

No clear Pathogenic/Likely Pathogenic ClinVar group was present in the final candidate set. Therefore, this project does not report sensitivity, specificity, precision, recall, AUROC, or other clinical classification performance metrics.

## Top-Ranked Variants

The highest VariantPriorX score observed was 7.

Two variants reached this score:

- CLCN7 — HIGH impact, very rare population frequency.
- EEF1A2 — HIGH impact, gnomAD FOUND with allele frequency 0.

SIGLEC16 reached a score of 6 through HIGH functional impact and rare population frequency.

Several MODERATE-impact variants reached score 5 through combinations of rare population frequency and other available evidence.

These rankings demonstrate how VariantPriorX combines multiple evidence dimensions rather than relying on a single annotation source.

## gnomAD Retrieval Validation

Population-frequency retrieval produced:

- FOUND: 475
- NOT_FOUND: 20
- Unresolved technical records: 2

NOT_FOUND and unresolved records receive no frequency evidence contribution and are not interpreted as allele frequency zero.

This prevents missing population data from being incorrectly treated as evidence of rarity.

## Interpretation

The internal benchmark demonstrates that:

1. Rare and very rare variants are preferentially ranked above common variants.
2. Benign and likely benign ClinVar variants are strongly deprioritized.
3. HIGH-impact variants can achieve high rankings when supported by population-frequency evidence.
4. Missing gnomAD evidence does not automatically increase a variant's score.
5. The final ranking remains transparent because each score can be decomposed into functional-impact, ClinVar, and population-frequency contributions.

## Limitations

This benchmark is not independent because ClinVar evidence and population frequency are components of the scoring system being evaluated.

The HG002 candidate set also contains no clear ClinVar Pathogenic/Likely Pathogenic variants after the implemented filtering and evidence-integration steps.

Therefore, the results demonstrate internal consistency and prioritization behavior, not clinical predictive performance.

A future independent validation could evaluate VariantPriorX against a separate truth set containing known pathogenic and benign variants without using the evaluation labels directly as scoring inputs.

## Conclusion

VariantPriorX successfully demonstrates transparent evidence-based germline variant prioritization with internally consistent ranking behavior.

The benchmark supports the technical behavior of the prioritization framework while preserving a clear boundary between research prioritization and clinical variant classification.
