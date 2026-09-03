import pandas as pd
import numpy as np

INFILE = "results/annotation/variantpriorx_master.tsv"
OUTFILE = "results/annotation/variantpriorx_ranked.tsv"

df = pd.read_csv(INFILE, sep="\t")

# -------------------------
# 1. Impact score
# -------------------------
impact_score = {
    "HIGH": 4,
    "MODERATE": 2,
    "LOW": 0,
    "MODIFIER": 0
}

df["impact_score"] = (
    df["max_impact"]
    .map(impact_score)
    .fillna(0)
)

# -------------------------
# 2. ClinVar score
# -------------------------
def score_clinvar(value):
    if pd.isna(value) or value == ".":
        return 0

    value = str(value).lower()

    if "pathogenic" in value and "conflicting" not in value:
        if "likely_pathogenic" in value and "pathogenic" not in value.replace("likely_pathogenic", ""):
            return 4
        return 5

    if "uncertain_significance" in value:
        return 1

    if "conflicting" in value:
        return 1

    if "likely_benign" in value and "benign" not in value.replace("likely_benign", ""):
        return -3

    if "benign" in value:
        return -4

    return 0

df["clinvar_score"] = df["clnsig"].apply(score_clinvar)

# -------------------------
# 3. Population frequency
# -------------------------
df["population_af"] = pd.to_numeric(
    df["joint_af"],
    errors="coerce"
)

def score_frequency(row):
    # Technical failure or not present:
    # keep as unknown, not AF=0
    if row["status"] != "FOUND":
        return 0

    af = row["population_af"]

    if pd.isna(af):
        return 0
    elif af < 0.0001:
        return 3
    elif af < 0.001:
        return 2
    elif af < 0.01:
        return 1
    elif af < 0.05:
        return -2
    else:
        return -3

df["frequency_score"] = df.apply(score_frequency, axis=1)

# -------------------------
# 4. Final VariantPriorX score
# -------------------------
df["variantpriorx_score"] = (
    df["impact_score"]
    + df["clinvar_score"]
    + df["frequency_score"]
)

# Frequency evidence label
def frequency_label(row):
    if row["status"] == "NOT_FOUND":
        return "NOT_FOUND"

    if str(row["status"]).startswith("ERROR"):
        return "UNRESOLVED"

    af = row["population_af"]

    if pd.isna(af):
        return "UNKNOWN"
    elif af < 0.0001:
        return "VERY_RARE"
    elif af < 0.001:
        return "RARE"
    elif af < 0.01:
        return "LOW_FREQUENCY"
    elif af < 0.05:
        return "UNCOMMON"
    else:
        return "COMMON"

df["frequency_class"] = df.apply(frequency_label, axis=1)

# -------------------------
# 5. Rank
# -------------------------
df = df.sort_values(
    by=[
        "variantpriorx_score",
        "impact_score",
        "frequency_score"
    ],
    ascending=False
).reset_index(drop=True)

df["rank"] = range(1, len(df) + 1)

# Put useful columns first
priority = [
    "rank",
    "variant_id",
    "gene_symbol",
    "most_severe_consequence",
    "max_impact",
    "hgvsc",
    "hgvsp",
    "clnsig",
    "clnrevstat",
    "clndn",
    "population_af",
    "frequency_class",
    "impact_score",
    "clinvar_score",
    "frequency_score",
    "variantpriorx_score"
]

remaining = [c for c in df.columns if c not in priority]

df = df[priority + remaining]

df.to_csv(
    OUTFILE,
    sep="\t",
    index=False
)

print("Ranked variants:", len(df))
print("Unique variants:", df["variant_id"].nunique())

print("\nScore distribution:")
print(
    df["variantpriorx_score"]
    .value_counts()
    .sort_index(ascending=False)
)

print("\nTop 15 variants:")
print(
    df[
        [
            "rank",
            "variant_id",
            "gene_symbol",
            "max_impact",
            "clnsig",
            "population_af",
            "frequency_class",
            "variantpriorx_score"
        ]
    ]
    .head(15)
    .to_string(index=False)
)

print("\nCreated:")
print(OUTFILE)
