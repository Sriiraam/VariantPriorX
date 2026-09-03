#  VariantPriorX

### Evidence-Based Germline Variant Prioritization for Clinical Genomics Research

[![CI](https://github.com/Sriiraam/VariantPriorX/actions/workflows/ci.yml/badge.svg)](https://github.com/Sriiraam/VariantPriorX/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Nextflow](https://img.shields.io/badge/Nextflow-DSL2-23AA62?logo=nextflow&logoColor=white)](https://www.nextflow.io/)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Live%20Dashboard-FF4B4B?logo=streamlit&logoColor=white)](https://variantpriorx.streamlit.app/)
[![Tests](https://img.shields.io/badge/tests-10%20passed-success)](https://github.com/Sriiraam/VariantPriorX/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-v0.1.0-blue)](CHANGELOG.md)

> **VariantPriorX** is a reproducible clinical-genomics research workflow that integrates functional consequence, curated clinical evidence, and population allele frequency to transparently prioritize medically relevant germline variants.

### 🚀 [Open the Live VariantPriorX Dashboard](https://variantpriorx.streamlit.app/)

---

## 📌 Overview

Modern germline variant analysis can produce thousands of candidate variants, but identifying variants that deserve further investigation requires integration of multiple evidence sources.

VariantPriorX demonstrates a transparent and reproducible prioritization strategy using:

- 🧬 **Ensembl VEP** — functional consequence annotation
- 🏥 **ClinVar** — curated clinical significance evidence
- 🌍 **gnomAD** — population allele-frequency evidence
- ⚙️ **Nextflow DSL2** — reproducible workflow orchestration
- 🐍 **Python / pandas** — evidence integration and prioritization
- 🗄️ **SQLite** — structured variant storage
- 📊 **Streamlit + Plotly** — interactive exploration
- 🐳 **Docker** — portable dashboard deployment
- 🧪 **pytest + GitHub Actions** — automated validation and CI

The project uses the **Genome in a Bottle HG002 Challenging Medically Relevant Genes (CMRG) benchmark**, providing a controlled public dataset for demonstrating clinical-genomics workflow engineering.

> **Important:** HG002 is a benchmark/reference genome, not a clinical patient.

---

## 🎯 Project Objective

VariantPriorX addresses the research question:

> **Can medically relevant germline variants from a benchmark human genome be systematically prioritized using functional consequence, population frequency, and curated clinical evidence?**

The project focuses on **evidence integration and prioritization**, rather than independent pathogenicity classification.

---

## ✨ Key Features

| Capability | Implementation |
|---|---|
| 🧬 Benchmark genome | GIAB HG002 / NA24385 |
| 🧹 Variant decomposition | bcftools |
| 🔬 Functional annotation | Ensembl VEP REST API |
| 🏥 Clinical evidence | NCBI ClinVar |
| 🌍 Population evidence | gnomAD |
| 🧠 Prioritization | Transparent rule-based scoring |
| ⚙️ Workflow orchestration | Nextflow DSL2 |
| 🗄️ Data layer | SQLite |
| 📊 Interactive analytics | Streamlit + Plotly |
| 🐳 Containerization | Docker |
| 🧪 Validation | pytest |
| 🔄 Continuous integration | GitHub Actions |
| 📚 Provenance | Dedicated documentation |
| ⚖️ Interpretation boundary | Explicit research-only framework |

---

## 🧬 Dataset

VariantPriorX uses the **Genome in a Bottle (GIAB) HG002 CMRG v1.00 benchmark**.

| Attribute | Value |
|---|---|
| Sample | HG002 |
| Alias | NA24385 |
| Reference material | NIST RM 8391 |
| Genome build | GRCh38 |
| Benchmark | Challenging Medically Relevant Genes |
| Version | CMRG v1.00 |
| Variant types | Germline SNVs + small indels |
| Initial records | 27,939 |
| Records after decomposition | 29,333 |
| HIGH/MODERATE candidates | 497 |

Primary benchmark file:

```text
HG002_GRCh38_CMRG_smallvar_v1.00.vcf.gz
```

The large source datasets and genomic reference resources are intentionally excluded from Git to keep the repository lightweight.

Detailed provenance is available in:

➡️ [Data Provenance](docs/DATA_PROVENANCE.md)

---

## 🏗️ Workflow Architecture

```text
GIAB HG002 CMRG
        │
        ▼
┌─────────────────────┐
│     Input QC        │
│   bcftools stats    │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│ Variant Decomposition│
│      bcftools       │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│    Ensembl VEP      │
│ Functional Evidence │
└─────────┬───────────┘
          │
          ├───────────────────┐
          │                   │
          ▼                   ▼
┌─────────────────┐   ┌─────────────────┐
│     ClinVar     │   │     gnomAD      │
│Clinical Evidence│   │Population AF    │
└────────┬────────┘   └────────┬────────┘
         │                     │
         └──────────┬──────────┘
                    │
                    ▼
          ┌───────────────────┐
          │ Evidence Integration│
          │   Master Table    │
          └─────────┬─────────┘
                    │
                    ▼
          ┌───────────────────┐
          │ VariantPriorX     │
          │ Prioritization    │
          └─────────┬─────────┘
                    │
                    ▼
          ┌───────────────────┐
          │      SQLite       │
          │ Variant Database  │
          └─────────┬─────────┘
                    │
                    ▼
          ┌───────────────────┐
          │ Streamlit + Plotly│
          │ Interactive UI    │
          └───────────────────┘
```

The current Nextflow DSL2 implementation orchestrates the downstream evidence-integration stages:

```text
BUILD_MASTER
     ↓
SCORE_VARIANTS
     ↓
BUILD_DATABASE
```

Upstream annotation artifacts are generated before execution of the current downstream Nextflow workflow.

---

## 🔬 Variant Processing

### 1️⃣ Input QC

The original GIAB CMRG VCF contained:

```text
Total records:          27,939
SNPs:                   21,524
Indels:                  6,502
Multiallelic sites:       1,394
Multiallelic SNP sites:      14
```

The input VCF uses GRCh38.

---

### 2️⃣ Variant Decomposition

Multiallelic variants were decomposed with `bcftools norm`.

Result:

```text
Input records:          27,939
Split multiallelic:      1,394
Output records:         29,333
Remaining multiallelic:      0
```

Genotype distribution after decomposition:

```text
0|1     10,075
1|0      8,527
1|1     10,731
```

Reference-based left alignment was intentionally excluded to avoid introducing a multi-gigabyte GRCh38 reference dependency into this lightweight portfolio implementation.

---

## 🧬 Functional Annotation — Ensembl VEP

The 29,333 decomposed variants were annotated through the **Ensembl Variant Effect Predictor REST API**.

Annotation fields include:

- Gene symbol
- Gene ID
- Transcript
- Consequence
- IMPACT
- MANE Select
- Canonical transcript
- HGVS coding notation
- HGVS protein notation
- Variant class

Maximum transcript impact was calculated across transcript consequences.

Candidate selection retained:

```text
HIGH       55
MODERATE  442
─────────────
TOTAL     497
```

These **497 variants** form the final VariantPriorX prioritization candidate set.

---

## 🏥 ClinVar Integration

ClinVar GRCh38 evidence was integrated using:

- ClinVar variant ID
- Clinical significance (`CLNSIG`)
- Review status (`CLNREVSTAT`)
- Associated condition (`CLNDN`)

ClinVar IDs were available for **298 of the 497 candidate variants**.

The candidate set contains substantial benign/likely benign and conflicting evidence, but no clear Pathogenic/Likely Pathogenic ClinVar group suitable for independent clinical-performance evaluation.

VariantPriorX preserves the original ClinVar evidence rather than independently assigning clinical classifications.

---

## 🌍 gnomAD Population Frequency

Population-frequency evidence was retrieved from **gnomAD v4** through its GraphQL interface.

Final retrieval status:

| Status | Variants |
|---|---:|
| FOUND | 475 |
| NOT_FOUND | 20 |
| Unresolved technical records | 2 |
| **Total** | **497** |

A critical design rule is:

> **NOT_FOUND ≠ allele frequency 0**

Missing or unresolved gnomAD evidence receives **no rarity bonus**.

A frequency of `0` is considered valid only when gnomAD successfully returns the variant with a valid allele-number context.

---

# 🧠 Transparent Prioritization Framework

VariantPriorX uses a deterministic evidence-based score.

```text
VariantPriorX Score
        =
Functional Impact Score
        +
ClinVar Evidence Score
        +
Population Frequency Score
```

This makes every ranking explainable and auditable.

---

## 🧬 Functional Impact Score

| VEP Impact | Score |
|---|---:|
| HIGH | +4 |
| MODERATE | +2 |
| LOW | 0 |
| MODIFIER | 0 |

---

## 🏥 ClinVar Evidence Score

| Evidence | Score |
|---|---:|
| Pathogenic | +5 |
| Likely pathogenic | +4 |
| VUS / conflicting evidence | +1 |
| Missing / not provided | 0 |
| Likely benign | -3 |
| Benign | -4 |

ClinVar evidence is retained as source evidence and is **not an independent VariantPriorX clinical classification**.

---

## 🌍 Population Frequency Score

Frequency scoring is applied only when the gnomAD retrieval status is `FOUND`.

| Population AF | Score |
|---|---:|
| `< 0.0001` | +3 |
| `< 0.001` | +2 |
| `< 0.01` | +1 |
| `0.01 – 0.05` | -2 |
| `>= 0.05` | -3 |
| Missing / unresolved | 0 |

Detailed scoring methodology:

➡️ [VariantPriorX Scoring Framework](docs/SCORING.md)

---

# 📈 Results

The final prioritized dataset contains:

```text
Total candidates       497
Unique variants        497
HIGH impact             55
MODERATE impact        442

gnomAD FOUND           475
gnomAD NOT_FOUND        20
gnomAD unresolved        2

Minimum score           -5
Maximum score            7
```

### 🏆 Highest-Prioritized Variants

| Gene | Impact | Population AF | Score |
|---|---|---:|---:|
| **CLCN7** | HIGH | 6.48 × 10⁻⁷ | **7** |
| **EEF1A2** | HIGH | 0 | **7** |
| **SIGLEC16** | HIGH | 1.02 × 10⁻⁴ | **6** |
| **GIPC3** | MODERATE | 4.61 × 10⁻⁶ | **5** |
| **MLPH** | MODERATE | 2.53 × 10⁻⁴ | **5** |
| **RHCE** | MODERATE | 4.37 × 10⁻⁵ | **5** |

A high VariantPriorX score indicates **prioritization for further investigation**, not pathogenicity.

---

# 📊 Internal Prioritization Benchmarking

VariantPriorX includes an internal benchmarking stage designed to test whether the prioritization rules behave consistently with their intended evidence model.

> This is an **internal prioritization sanity benchmark**, not a clinical accuracy benchmark.

Because ClinVar and population frequency are themselves components of the score, these analyses are not independent validation experiments.

---

## 🌍 Population-Frequency Benchmark

| Frequency Group | Variants | Median Score | Mean Score |
|---|---:|---:|---:|
| **VERY_RARE** | 15 | **5.0** | **4.60** |
| **RARE** | 13 | **4.0** | **3.46** |
| LOW_FREQUENCY | 23 | 0.0 | 1.04 |
| UNCOMMON | 34 | -2.0 | -1.88 |
| **COMMON** | 390 | **-5.0** | **-3.32** |

A clear prioritization gradient was observed:

```text
VERY_RARE     median = +5
     ↓
RARE          median = +4
     ↓
LOW_FREQUENCY median =  0
     ↓
UNCOMMON      median = -2
     ↓
COMMON        median = -5
```

This demonstrates that rare variants are preferentially ranked while common variants are strongly deprioritized, consistent with the implemented scoring framework.

---

## 🏥 ClinVar Stratification

| ClinVar Group | Variants | Median Score | Mean Score |
|---|---:|---:|---:|
| Conflicting | 8 | 2.5 | 2.25 |
| VUS | 3 | 0.0 | -0.33 |
| Other | 206 | -1.0 | 0.51 |
| **Benign / Likely Benign** | **280** | **-5.0** | **-4.52** |

Benign and likely benign variants were strongly shifted toward negative prioritization scores.

No clear Pathogenic/Likely Pathogenic group was present in the final candidate set. Therefore, VariantPriorX does **not** report:

- Accuracy
- Sensitivity
- Specificity
- Precision / recall
- AUROC
- Clinical pathogenicity prediction performance

This distinction prevents internal scoring behavior from being misrepresented as independent clinical validation.

Full benchmark methodology and limitations:

➡️ [Benchmarking Report](docs/benchmarking.md)

---

# 📊 Interactive Dashboard

### 🚀 [Launch VariantPriorX](https://variantpriorx.streamlit.app/)

The Streamlit dashboard provides an interactive interface over the final SQLite variant database.

### Dashboard capabilities

- 📌 Project-level KPI cards
- 📊 Score-distribution analysis
- 🧬 Functional-impact breakdown
- 🌍 Population-frequency analysis
- 🏥 ClinVar evidence profile
- 🔬 AF-vs-prioritization visualization
- 🏆 Top-ranked variant exploration
- 🔎 Gene and variant search
- 🧾 Variant-level evidence inspection
- 📥 Filtered table export
- ⚠️ Explicit interpretation boundary

The dashboard reads directly from:

```text
database/variantpriorx.db
```

---

# 🗄️ SQLite Data Layer

The final ranked variants are stored in a structured SQLite database.

```text
database/
└── variantpriorx.db
```

The database contains:

```text
497 rows
497 unique variant IDs
```

Indexes are provided for commonly queried fields including:

- Variant ID
- Gene
- VariantPriorX score
- ClinVar significance

This separates analytical processing from dashboard presentation and provides a lightweight reproducible data layer.

---

# ⚙️ Nextflow DSL2 Workflow

VariantPriorX includes modular Nextflow processes for downstream evidence integration.

```text
modules/
├── build_master.nf
├── score_variants.nf
└── build_database.nf
```

Run:

```bash
nextflow run main.nf
```

Resume cached execution:

```bash
nextflow run main.nf -resume
```

The workflow generates execution metadata including:

```text
report.html
timeline.html
trace.txt
dag.html
```

The current workflow expects the required upstream annotation artifacts to exist before downstream execution.

This boundary is intentional and documented rather than presenting the repository as a fully self-contained clean-clone genomic annotation pipeline.

---

# 🐳 Docker

VariantPriorX includes a containerized Streamlit deployment.

Build the image:

```bash
docker build -t variantpriorx .
```

Run:

```bash
docker run --rm -p 8501:8501 variantpriorx
```

Open:

```text
http://localhost:8501
```

The Docker image packages the dashboard and committed SQLite database while excluding large genomic resources.

---

# 🧪 Testing & Continuous Integration

VariantPriorX includes automated validation using **pytest**.

Current validation:

```text
10 passed
```

Tests verify:

- Database availability
- 497 expected variants
- Variant ID uniqueness
- HIGH/MODERATE impact counts
- gnomAD retrieval-status counts
- Score range
- Highest-ranked variants
- Missing-frequency handling
- Database row integrity
- SQLite uniqueness/integrity

Run locally:

```bash
source .venv/bin/activate
pytest -q
```

Expected:

```text
..........                                                       [100%]
10 passed
```

Every push and pull request to `main` is validated through **GitHub Actions CI**.

➡️ [View GitHub Actions](https://github.com/Sriiraam/VariantPriorX/actions)

---

# 🔁 Reproducibility

Create the environment:

```bash
python3 -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
pip install -r requirements.txt
```

Run validation:

```bash
pytest -q
```

Run downstream workflow:

```bash
nextflow run main.nf
```

Launch dashboard:

```bash
streamlit run streamlit_app/app.py
```

For detailed reproducibility information:

➡️ [Reproducibility Guide](docs/REPRODUCIBILITY.md)

---

# 📁 Repository Structure

```text
VariantPriorX/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── database/
│   └── variantpriorx.db
│
├── docs/
│   ├── adr/
│   ├── DATA_PROVENANCE.md
│   ├── INTERPRETATION_BOUNDARY.md
│   ├── REPRODUCIBILITY.md
│   ├── SCORING.md
│   ├── benchmarking.md
│   ├── architecture.md
│   ├── dataset.md
│   ├── execution_plan.md
│   ├── input_qc.md
│   └── tool_decisions.md
│
├── metadata/
│
├── modules/
│   ├── build_master.nf
│   ├── score_variants.nf
│   └── build_database.nf
│
├── scripts/
│   ├── benchmark_prioritization.py
│   ├── build_database.py
│   ├── build_master_table.py
│   ├── parse_vep_annotations.py
│   ├── query_gnomad.py
│   ├── score_variants.py
│   └── vep_rest_batch.py
│
├── streamlit_app/
│   └── app.py
│
├── tests/
│   └── test_variantpriorx.py
│
├── CHANGELOG.md
├── CITATION.cff
├── CONTRIBUTING.md
├── Dockerfile
├── LICENSE
├── SECURITY.md
├── main.nf
├── nextflow.config
├── requirements.txt
└── README.md
```

Large raw genomic data, reference resources, temporary workflow directories, and generated intermediate results are intentionally excluded from version control.

---

# 📚 Documentation

VariantPriorX includes dedicated technical and governance documentation.

| Document | Purpose |
|---|---|
| 📊 [Benchmarking](docs/benchmarking.md) | Internal prioritization validation and limitations |
| 🧬 [Data Provenance](docs/DATA_PROVENANCE.md) | Dataset and evidence-source provenance |
| 🧠 [Scoring Framework](docs/SCORING.md) | Transparent prioritization methodology |
| ⚠️ [Interpretation Boundary](docs/INTERPRETATION_BOUNDARY.md) | Research/clinical-use limitations |
| 🔁 [Reproducibility](docs/REPRODUCIBILITY.md) | Environment and execution guidance |
| 🏗️ [Architecture](docs/architecture.md) | Workflow architecture |
| 📦 [Dataset](docs/dataset.md) | Dataset documentation |
| 🛠️ [Tool Decisions](docs/tool_decisions.md) | Technical design decisions |
| 📝 [Changelog](CHANGELOG.md) | Project version history |
| 🤝 [Contributing](CONTRIBUTING.md) | Contribution guidelines |
| 🔐 [Security](SECURITY.md) | Security policy |
| 📖 [Citation](CITATION.cff) | Citation metadata |
| ⚖️ [MIT License](LICENSE) | Open-source license |

---

# ⚠️ Clinical Interpretation Boundary

VariantPriorX is a **research, educational, and portfolio project**.

It is **not** a clinical diagnostic system.

VariantPriorX does not:

- Diagnose genetic disease
- Recommend treatment
- Establish disease causality
- Replace clinical geneticists or molecular pathologists
- Independently classify variants as pathogenic or benign
- Implement the complete ACMG/AMP framework

The VariantPriorX score represents:

> **Evidence-based prioritization for further investigation — not clinical pathogenicity.**

HG002 is used exclusively as a public benchmark/reference genome.

See:

➡️ [Interpretation Boundary](docs/INTERPRETATION_BOUNDARY.md)

---

# 🛠️ Technology Stack

### Bioinformatics

`bcftools` · `Ensembl VEP` · `ClinVar` · `gnomAD`

### Workflow Engineering

`Nextflow DSL2`

### Data Engineering

`Python 3.12` · `pandas` · `SQLite`

### Visualization

`Streamlit` · `Plotly`

### Reproducibility & DevOps

`Docker` · `Git` · `GitHub Actions` · `pytest`

---

# 🧭 Design Principles

VariantPriorX was built around several engineering principles:

### 🔍 Transparency

Every final score can be decomposed into its individual evidence contributions.

### ♻️ Reproducibility

Processing logic, workflow configuration, tests, provenance, and deployment configuration are version controlled.

### 🧩 Modularity

Evidence integration, scoring, database construction, and presentation are separated into distinct components.

### 📦 Lightweight Deployment

Large reference datasets are excluded from Git while the final SQLite database enables immediate dashboard deployment.

### ⚠️ Conservative Missing-Data Handling

Missing population evidence is not interpreted as rarity.

### 🏥 Clinical Boundary Awareness

Prioritization is clearly separated from clinical pathogenicity classification.

---

# 🚧 Limitations

VariantPriorX currently has several intentional limitations:

- The project evaluates one GIAB benchmark genome.
- The final candidate set does not contain a clear ClinVar Pathogenic/Likely Pathogenic benchmark group.
- Internal benchmarking is not independent because some evaluated evidence dimensions contribute to the prioritization score.
- The project does not implement full ACMG/AMP classification.
- gnomAD queries rely on remote API availability.
- The lightweight workflow avoids bundling a full GRCh38 reference genome.
- Reference-based left normalization is not included in the current implementation.
- The current Nextflow workflow orchestrates downstream integration rather than the entire upstream annotation process from raw VCF.

These limitations are documented explicitly to keep project claims aligned with demonstrated functionality.

---

# 🔮 Future Scope

Potential extensions include:

### 🧬 Independent Benchmark Validation

Evaluate prioritization against a separate curated truth set containing known pathogenic and benign variants while preventing evaluation labels from contributing directly to the tested score.

### 📐 ACMG/AMP Evidence Assistance

Add structured ACMG/AMP evidence collection and rule tracking while maintaining expert review and avoiding automated clinical diagnosis.

### 👨‍👩‍👦 Inheritance-Aware Prioritization

Extend the workflow to trio-based analysis using HG002/HG003/HG004 for:

- De novo variants
- Recessive inheritance
- Compound heterozygosity
- Segregation evidence

### 🧬 Additional Variant Types

Extend beyond SNVs and small indels to support:

- Structural variants
- Copy-number variants
- Repeat expansions

### 🏥 Additional Evidence Sources

Potential integration with:

- ClinGen
- OMIM-compatible evidence workflows
- Gene-disease validity resources
- Constraint metrics
- Disease-specific knowledge bases

### ⚙️ Full End-to-End Nextflow Orchestration

Expand the current downstream DSL2 workflow to include:

```text
INPUT_QC
   ↓
DECOMPOSE
   ↓
VEP_ANNOTATION
   ↓
CLINVAR_ANNOTATION
   ↓
GNOMAD_ANNOTATION
   ↓
BUILD_MASTER
   ↓
SCORE_VARIANTS
   ↓
BUILD_DATABASE
```

### 🧪 Expanded Testing

Add:

- Unit tests for individual scoring rules
- Schema validation
- API-response mocks
- Workflow integration tests
- Docker health tests
- Regression snapshots

### 📦 Versioned Releases

Publish stable GitHub releases with versioned scoring methodology and reproducibility metadata.

---

# 📖 Citation

If you use or reference VariantPriorX, please cite the project using the repository citation metadata:

➡️ [CITATION.cff](CITATION.cff)

GitHub also provides a **Cite this repository** option based on this metadata.

Suggested project reference:

```text
Sriram B. (2026). VariantPriorX: Evidence-Based Germline Variant Prioritization
for Clinical Genomics Research. Version 0.1.0.
https://github.com/Sriiraam/VariantPriorX
```

---

# 📝 Changelog

Version history and major project changes are documented here:

➡️ [CHANGELOG.md](CHANGELOG.md)

Current release:

```text
v0.1.0
```

---

# 🤝 Contributing

Reproducibility improvements, bug fixes, documentation improvements, and well-scoped feature contributions are welcome.

Please read:

➡️ [CONTRIBUTING.md](CONTRIBUTING.md)

---

# 🔐 Security

Security and sensitive-data handling guidance:

➡️ [SECURITY.md](SECURITY.md)

VariantPriorX should not be used to store or process identifiable clinical patient information without an appropriate secure and compliant environment.

---

# ⚖️ License

VariantPriorX is released under the **MIT License**.

➡️ [LICENSE](LICENSE)

---

# 👨‍💻 Author

**Sriram B.**

Bioinformatics · Genomics · Reproducible Workflow Engineering

GitHub: [@Sriiraam](https://github.com/Sriiraam)

---

## 🌟 VariantPriorX

**From benchmark variants → evidence integration → transparent prioritization → reproducible exploration.**

### 🧬 [Explore the Live Dashboard](https://variantpriorx.streamlit.app/)

### 💻 [View the Source Code](https://github.com/Sriiraam/VariantPriorX)

---

*VariantPriorX is intended for research, educational, and portfolio use. It is not a medical device or clinical diagnostic system.*
