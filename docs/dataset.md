# Dataset

## Selected Benchmark

VariantPriorX uses the Genome in a Bottle (GIAB) HG002 Challenging Medically Relevant Genes (CMRG) v1.00 small-variant benchmark.

| Field | Value |
|---|---|
| GIAB sample | HG002 |
| Coriell identifier | NA24385 |
| Reference | GRCh38 |
| Benchmark | CMRG v1.00 |
| Variant class | SNVs + small indels |
| Source | NIST / Genome in a Bottle |
| Input | HG002_GRCh38_CMRG_smallvar_v1.00.vcf.gz |
| Benchmark regions | HG002_GRCh38_CMRG_smallvar_v1.00.bed |

## Verified File Sizes

Before download, server metadata was checked using HTTP headers.

- VCF: 231,237 bytes (~226 KB)
- BED: 61,538 bytes (~60 KB)

The dataset is therefore comfortably within the project's <=1.5 GB storage target.

## Why HG002?

HG002 is a well-characterized GIAB benchmark genome and allows VariantPriorX to use a reproducible benchmark rather than presenting an anonymous dataset as a clinical patient.

## Why CMRG?

CMRG focuses on challenging medically relevant genomic regions.

This gives the project a clinically relevant scope while avoiding unnecessary whole-genome data.

## Important Limitation

HG002 is a benchmark/reference genome, not a clinical diagnostic case.

VariantPriorX therefore demonstrates variant annotation and evidence-based prioritization, not patient diagnosis.
