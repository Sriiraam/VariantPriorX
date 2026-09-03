# ADR-001: Dataset and Analysis Strategy

## Status

Accepted

## Decision

Use HG002 / NA24385 GIAB CMRG v1.00 GRCh38 small-variant benchmark as the primary VariantPriorX input.

## Alternatives Considered

### Full HG002 GIAB v4.2.1 genome-wide VCF

Rejected because the complete benchmark is unnecessary for this mini-project and substantially increases storage and processing requirements.

### HG002 restricted to ACMG medically actionable genes

Considered useful, but requires creation of a custom subset.

### GIAB CMRG

Selected because it provides an established benchmark specifically targeting challenging medically relevant genomic regions.

## Analysis Strategy

VariantPriorX will prioritize variants using multiple evidence dimensions:

1. Variant validity and normalization
2. Functional consequence
3. Population frequency
4. ClinVar clinical evidence
5. Gene-level clinical relevance
6. Transparent evidence-based ranking

The ranking system will remain interpretable and rule-based rather than using AI/ML.

## Consequences

Advantages:

- Small computational footprint
- Reproducible benchmark
- Clinically relevant genomic regions
- Suitable for local execution
- Strong clinical-genomics portfolio value

Limitations:

- Single benchmark genome
- Not a real diagnostic patient case
- Results must not be presented as clinical diagnoses
