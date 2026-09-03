# Tool Decisions

| Stage | Tool | Purpose |
|---|---|---|
| VCF inspection | bcftools | Validate and inspect input variants |
| Normalization | bcftools | Normalize multiallelic variants and representation |
| Functional annotation | Ensembl VEP | Variant consequence annotation |
| Population evidence | gnomAD | Population allele-frequency evidence |
| Clinical evidence | ClinVar | Curated clinical significance |
| Prioritization | Python | Transparent rule-based evidence integration |
| Workflow | Nextflow DSL2 | Reproducible orchestration |
| Data layer | SQLite | Structured variant/evidence storage |
| Dashboard | Streamlit | Interactive exploration and reporting |
| Containers | Docker | Reproducible software environment |
| Testing | pytest | Automated validation |
| CI | GitHub Actions | Repository-level automated checks |

## Design Principle

VariantPriorX will prioritize interpretability and provenance.

Each prioritized variant should retain the evidence explaining why it received its ranking.
