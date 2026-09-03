# VariantPriorX — Project Scope

## Objective

VariantPriorX is a reproducible clinical-genomics mini-project for prioritizing medically relevant germline SNVs and small indels using functional, population-frequency, and curated clinical evidence.

## Core Question

Can medically relevant germline variants from a benchmark human genome be systematically prioritized using functional consequence, population frequency, and curated clinical evidence?

## Input

- Sample: HG002 / NA24385
- Dataset: Genome in a Bottle (GIAB) CMRG v1.00
- Reference assembly: GRCh38
- Variant types: germline SNVs and small indels
- Input format: compressed VCF
- Benchmark regions: GIAB CMRG BED

## Planned Workflow

HG002 CMRG VCF
→ VCF validation
→ normalization
→ functional annotation
→ population-frequency annotation
→ ClinVar evidence
→ clinically relevant gene flags
→ evidence-based filtering/prioritization
→ SQLite
→ Streamlit report/dashboard

## Engineering

- Python
- Nextflow DSL2
- VEP
- bcftools
- SQLite
- Streamlit
- Docker
- pytest
- GitHub Actions

## Constraints

- Complete project target: <= 1.5 GB
- Local-first execution
- No paid cloud infrastructure
- No AI/ML required

## Interpretation Boundary

VariantPriorX is an educational/research bioinformatics project.

It does not provide medical diagnosis and does not independently assign clinical pathogenicity. Clinical evidence from resources such as ClinVar will be reported with provenance rather than presented as a new clinical classification.
