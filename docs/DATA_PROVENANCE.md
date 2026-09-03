# Data Provenance

## Benchmark Sample

VariantPriorX uses the Genome in a Bottle (GIAB) HG002 benchmark genome.

- Sample: HG002
- Alias: NA24385
- Reference material: NIST RM 8391
- Genome build: GRCh38
- Benchmark: Challenging Medically Relevant Genes (CMRG)
- Benchmark version: v1.00
- Variant type: Germline SNVs and small indels

HG002 is a benchmark/reference genome and is not treated as a clinical patient.

## Primary Dataset

Primary VCF:

`HG002_GRCh38_CMRG_smallvar_v1.00.vcf.gz`

Associated index:

`HG002_GRCh38_CMRG_smallvar_v1.00.vcf.gz.tbi`

Benchmark regions:

`HG002_GRCh38_CMRG_smallvar_v1.00.bed`

The original benchmark contained 27,939 variant records.

After multiallelic decomposition, VariantPriorX processed 29,333 records.

## Functional Annotation

Functional consequence information was obtained using the Ensembl Variant Effect Predictor (VEP) REST service.

HIGH and MODERATE impact variants were retained for downstream evidence prioritization, producing 497 candidate variants.

## ClinVar

ClinVar GRCh38 data from NCBI were used as curated clinical evidence.

VariantPriorX retains ClinVar identifiers, clinical significance, review status, and associated condition information when available.

## gnomAD

Population-frequency evidence was obtained programmatically from gnomAD.

Final query status:

- FOUND: 475
- NOT_FOUND: 20
- Unresolved technical records: 2

NOT_FOUND is treated as missing population evidence, not as allele frequency zero.

## Provenance Principle

VariantPriorX maintains a distinction between source evidence, derived annotations, and the final prioritization score.

The score is a research prioritization metric and not an ACMG/AMP pathogenicity classification.
