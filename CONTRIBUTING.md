# Contributing to VariantPriorX

Thank you for your interest in VariantPriorX.

VariantPriorX is primarily a bioinformatics portfolio and educational project, but reproducibility improvements, bug fixes, documentation improvements, and well-scoped feature contributions are welcome.

## Development Setup

Clone the repository:

```bash
git clone https://github.com/Sriiraam/VariantPriorX.git
cd VariantPriorX
```

Create and activate a Python virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Testing

Run the validation suite before submitting changes:

```bash
pytest -q
```

All tests should pass.

## Development Guidelines

Please:

- Keep changes focused and clearly documented.
- Preserve reproducible data-processing behavior.
- Do not commit large raw genomic datasets or reference resources.
- Do not commit credentials, API keys, tokens, or secrets.
- Add or update tests when changing prioritization logic.
- Document changes that alter workflow behavior or interpretation.
- Preserve the distinction between evidence-based prioritization and clinical classification.

## Clinical Interpretation Boundary

VariantPriorX does not provide independent ACMG/AMP pathogenicity classification.

Changes must not present the VariantPriorX prioritization score as a clinical diagnosis, pathogenicity determination, or medical recommendation.

## Pull Requests

A pull request should briefly describe:

1. What was changed.
2. Why the change was needed.
3. How the change was tested.
4. Whether the change affects prioritization results or interpretation.

## License

By contributing to VariantPriorX, you agree that your contributions will be distributed under the MIT License.
