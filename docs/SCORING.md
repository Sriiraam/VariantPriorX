# VariantPriorX Prioritization Score

VariantPriorX uses a transparent rule-based score combining functional consequence, curated clinical evidence, and population frequency.

The score is intended for ranking only and is not an ACMG/AMP pathogenicity classification.

## Functional Impact

| VEP impact | Score |
| --- | ---: |
| HIGH | +4 |
| MODERATE | +2 |
| LOW | 0 |
| MODIFIER | 0 |

## ClinVar Evidence

| ClinVar evidence | Score |
| --- | ---: |
| Pathogenic | +5 |
| Likely pathogenic | +4 |
| Uncertain significance / conflicting evidence | +1 |
| Likely benign | -3 |
| Benign | -4 |
| Missing / not provided / unsupported category | 0 |

ClinVar classifications remain source evidence. VariantPriorX does not independently assign these classifications.

## Population Frequency

Frequency scoring is applied only when the gnomAD query status is `FOUND`.

| Population allele frequency | Score |
| --- | ---: |
| AF < 0.0001 | +3 |
| AF < 0.001 | +2 |
| AF < 0.01 | +1 |
| AF 0.01–0.05 | -2 |
| AF >= 0.05 | -3 |

For NOT_FOUND, unresolved API responses, or missing frequency values:

`frequency_score = 0`

Missing evidence is therefore not interpreted as evidence of rarity.

## Final Score

`VariantPriorX score = impact_score + clinvar_score + frequency_score`

Higher scores indicate stronger prioritization according to the implemented rules. They do not establish pathogenicity, disease causality, diagnosis, or clinical actionability.
