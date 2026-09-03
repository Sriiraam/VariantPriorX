import sqlite3
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "database" / "variantpriorx.db"
OUT = ROOT / "results" / "benchmarking"
OUT.mkdir(parents=True, exist_ok=True)

conn = sqlite3.connect(DB)
df = pd.read_sql_query("SELECT * FROM variants", conn)
conn.close()

# -----------------------------
# Basic integrity
# -----------------------------
summary = [
    ["total_variants", len(df)],
    ["unique_variants", df["variant_id"].nunique()],
    ["high_impact", (df["max_impact"] == "HIGH").sum()],
    ["moderate_impact", (df["max_impact"] == "MODERATE").sum()],
    ["gnomad_found", (df["status"] == "FOUND").sum()],
    ["gnomad_not_found", (df["status"] == "NOT_FOUND").sum()],
    ["gnomad_unresolved", df["status"].astype(str).str.startswith("ERROR").sum()],
    ["maximum_score", df["variantpriorx_score"].max()],
    ["minimum_score", df["variantpriorx_score"].min()],
]

pd.DataFrame(
    summary,
    columns=["metric", "value"]
).to_csv(
    OUT / "benchmark_summary.tsv",
    sep="\t",
    index=False
)

# -----------------------------
# ClinVar evidence groups
# -----------------------------
def clinvar_group(value):
    x = str(value).lower()

    if x in {"nan", "none", ""}:
        return "NO_CLINVAR"

    # Conflicting classifications must not be
    # counted as pathogenic simply because the
    # word "pathogenicity" appears in the label.
    if "conflicting" in x:
        return "CONFLICTING"

    if "uncertain" in x:
        return "VUS"

    if "benign" in x:
        return "BENIGN_OR_LIKELY_BENIGN"

    if "pathogenic" in x:
        return "PATHOGENIC_OR_LIKELY_PATHOGENIC"

    return "OTHER"


df["clinvar_group"] = df["clnsig"].apply(clinvar_group)

clinvar_summary = (
    df.groupby("clinvar_group", dropna=False)
      .agg(
          variants=("variant_id", "count"),
          median_score=("variantpriorx_score", "median"),
          mean_score=("variantpriorx_score", "mean"),
          max_score=("variantpriorx_score", "max"),
          min_score=("variantpriorx_score", "min"),
      )
      .reset_index()
      .sort_values("median_score", ascending=False)
)

clinvar_summary.to_csv(
    OUT / "clinvar_score_summary.tsv",
    sep="\t",
    index=False
)

# -----------------------------
# Frequency sanity benchmark
# -----------------------------
found = df[
    (df["status"] == "FOUND") &
    (df["population_af"].notna())
].copy()

def frequency_group(af):
    af = float(af)

    if af < 0.0001:
        return "VERY_RARE"
    if af < 0.001:
        return "RARE"
    if af < 0.01:
        return "LOW_FREQUENCY"
    if af < 0.05:
        return "UNCOMMON"
    return "COMMON"


found["benchmark_frequency_group"] = found["population_af"].apply(frequency_group)

frequency_summary = (
    found.groupby("benchmark_frequency_group")
         .agg(
             variants=("variant_id", "count"),
             median_score=("variantpriorx_score", "median"),
             mean_score=("variantpriorx_score", "mean"),
         )
         .reset_index()
)

frequency_summary.to_csv(
    OUT / "frequency_score_summary.tsv",
    sep="\t",
    index=False
)

# -----------------------------
# Top-ranked evidence review
# -----------------------------
top = (
    df.sort_values(
        ["variantpriorx_score", "gene_symbol"],
        ascending=[False, True]
    )
    .head(20)
)

wanted = [
    "variant_id",
    "gene_symbol",
    "max_impact",
    "clnsig",
    "population_af",
    "status",
    "impact_score",
    "clinvar_score",
    "frequency_score",
    "variantpriorx_score",
]

wanted = [c for c in wanted if c in top.columns]

top[wanted].to_csv(
    OUT / "top20_evidence_review.tsv",
    sep="\t",
    index=False
)

print("\nVariantPriorX internal benchmarking complete")
print("============================================")
print(f"Variants: {len(df)}")
print(f"Unique:   {df['variant_id'].nunique()}")
print(f"Score:    {df['variantpriorx_score'].min()} to {df['variantpriorx_score'].max()}")

print("\nClinVar score stratification:")
print(clinvar_summary.to_string(index=False))

print("\nPopulation-frequency stratification:")
print(frequency_summary.to_string(index=False))

print("\nTop 10 ranked variants:")
cols = [c for c in ["gene_symbol", "max_impact", "population_af",
                     "clnsig", "variantpriorx_score"] if c in top.columns]
print(top[cols].head(10).to_string(index=False))

print(f"\nOutputs: {OUT}")
