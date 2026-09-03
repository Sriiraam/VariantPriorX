# Input VCF Quality Control

## Dataset

- Sample: HG002 / NA24385
- Dataset: GIAB CMRG v1.00
- Assembly: GRCh38
- Input: HG002_GRCh38_CMRG_smallvar_v1.00.vcf.gz

## Validation

| Metric | Result |
|---|---:|
| Samples | 1 |
| Sample ID | HG002 |
| VCF records | 27,939 |
| SNPs | 21,524 |
| Indels | 6,502 |
| Multiallelic sites | 1,394 |
| Multiallelic SNP sites | 14 |
| Chromosomes represented | chr1–chr22 |
| Index | Valid |
| Reference assembly | human_GRCh38_no_alt_analysis_set.fasta |

## Interpretation

The VCF is readable, indexed, uses GRCh38 coordinates, contains the expected HG002 sample, and contains both SNVs and small indels across all autosomes.

Multiallelic records will be decomposed before downstream annotation and prioritization.
