# VariantPriorX Execution Plan

## Phase 1 — Dataset
- Freeze scope
- Document dataset
- Download GIAB CMRG files
- Verify integrity
- Inspect VCF

## Phase 2 — Variant Processing
- Validate VCF
- Inspect variant composition
- Normalize variants
- Generate QC summaries

## Phase 3 — Annotation
- Configure GRCh38 resources
- Run VEP
- Add population-frequency evidence
- Add ClinVar evidence
- Preserve annotation provenance

## Phase 4 — Prioritization
- Design transparent ranking rules
- Rank variants
- Generate evidence tables
- Validate representative variants

## Phase 5 — Engineering
- Nextflow DSL2 workflow
- Modular processes
- Configuration
- Docker
- SQLite database
- Tests

## Phase 6 — Presentation
- Streamlit dashboard
- Variant explorer
- Evidence visualization
- Prioritized variant report

## Phase 7 — Production Polish
- Benchmarking
- CI/CD
- Documentation
- GitHub release
- Public dashboard deployment
