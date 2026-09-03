# Variant Decomposition QC

## Input

HG002 GIAB CMRG v1.00 GRCh38 small-variant benchmark.

## Results

| Metric | Raw | Decomposed |
|---|---:|---:|
| Records | 27,939 | 29,333 |
| SNPs | 21,524 | 21,538 |
| Indels | 6,502 | 7,030 |
| Multiallelic sites | 1,394 | 0 |

## Genotypes after decomposition

- 0|1: 10,075
- 1|0: 8,527
- 1|1: 10,731

## Interpretation

Multiallelic records were decomposed into individual alternate alleles using bcftools norm -m -any.

No multiallelic records remain.

Reference-based left alignment has not yet been performed because no GRCh38 FASTA was supplied at this stage.
