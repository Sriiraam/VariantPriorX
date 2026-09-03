# Reproducibility

VariantPriorX separates large genomic resources from lightweight repository artifacts.

## Python Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Automated Validation

```bash
pytest -q
```

## Nextflow

VariantPriorX uses Nextflow DSL2 for downstream evidence integration, prioritization, and database construction.

```bash
nextflow run main.nf
```

Cached execution can be resumed with:

```bash
nextflow run main.nf -resume
```

The current downstream workflow expects the required annotation artifacts to have been generated beforehand.

Large genomic datasets and reference resources are intentionally excluded from Git.

## Docker

Build:

```bash
docker build -t variantpriorx .
```

Run:

```bash
docker run --rm -p 8501:8501 variantpriorx
```

The Streamlit dashboard is exposed on port 8501.

## Reproducibility Boundary

The repository contains workflow implementation, prioritization logic, tests, documentation, and lightweight artifacts required for demonstration.

Large upstream genomic datasets and reference resources are excluded from Git and documented separately.
