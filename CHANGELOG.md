# Changelog

All notable changes to VariantPriorX are documented in this file.

The project follows semantic versioning for portfolio releases.

## [0.1.0] - 2026-09-03

### Added

- Initial VariantPriorX clinical genomics prioritization workflow.
- GIAB HG002 CMRG GRCh38 benchmark dataset integration.
- Small-variant decomposition using bcftools.
- Ensembl VEP functional consequence annotation.
- ClinVar clinical evidence integration.
- gnomAD population frequency annotation.
- Transparent evidence-based variant prioritization scoring.
- SQLite database containing 497 prioritized variants.
- Nextflow DSL2 workflow for downstream evidence integration, scoring, and database generation.
- Interactive Streamlit dashboard for variant exploration.
- Docker container for reproducible dashboard deployment.
- Automated pytest validation suite.
- Internal prioritization benchmarking using ClinVar evidence stratification and gnomAD population-frequency groups.
- GitHub Actions continuous integration workflow.
- Dataset, architecture, execution, tool-decision, and QC documentation.

### Validation

- 497 prioritized variants.
- 497 unique variant identifiers.
- 55 HIGH-impact variants.
- 442 MODERATE-impact variants.
- 475 variants matched to gnomAD.
- Maximum VariantPriorX prioritization score: 7.
- Automated validation suite: 10 tests.

### Notes

VariantPriorX is a research and educational portfolio project. Its prioritization score is not an ACMG/AMP classification and must not be interpreted as a clinical diagnosis or medical recommendation.
