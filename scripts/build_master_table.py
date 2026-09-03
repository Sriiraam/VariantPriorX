import pandas as pd

VEP = "results/annotation/vep_clinical_candidates.tsv"
CLIN = "results/annotation/clinvar_annotations.tsv"
GNO = "results/annotation/gnomad_frequency.tsv"
OUT = "results/annotation/variantpriorx_master.tsv"

vep = pd.read_csv(VEP, sep="\t")
clin = pd.read_csv(CLIN, sep="\t")
gno = pd.read_csv(GNO, sep="\t")

# Clean column names
vep.columns = vep.columns.str.strip()
clin.columns = clin.columns.str.strip()
gno.columns = gno.columns.str.strip()

# Build IDs
vep["variant_id"] = (
    vep["chrom"].astype(str).str.replace(r"^chr", "", regex=True)
    + "-" + vep["pos"].astype(str)
    + "-" + vep["ref"].astype(str)
    + "-" + vep["alt"].astype(str)
)

# ClinVar already corresponds to the same 497 variants.
# Rename first four columns explicitly to avoid header-format problems.
clin = clin.rename(columns={
    clin.columns[0]: "chrom",
    clin.columns[1]: "pos",
    clin.columns[2]: "ref",
    clin.columns[3]: "alt"
})

clin["variant_id"] = (
    clin["chrom"].astype(str).str.replace(r"^chr", "", regex=True)
    + "-" + clin["pos"].astype(str)
    + "-" + clin["ref"].astype(str)
    + "-" + clin["alt"].astype(str)
)

master = vep.merge(
    clin[[
        "variant_id",
        "clinvar_id",
        "clnsig",
        "clnrevstat",
        "clndn"
    ]],
    on="variant_id",
    how="left"
)

master = master.merge(
    gno,
    on="variant_id",
    how="left"
)

master.to_csv(OUT, sep="\t", index=False)

clinvar_matched = (
    master["clinvar_id"].notna()
    & (master["clinvar_id"].astype(str) != ".")
).sum()

print("Master rows:", len(master))
print("Unique variants:", master["variant_id"].nunique())
print("ClinVar matched:", clinvar_matched)
print("gnomAD FOUND:", (master["status"] == "FOUND").sum())
print("gnomAD NOT_FOUND:", (master["status"] == "NOT_FOUND").sum())
print("gnomAD errors:", master["status"].astype(str).str.startswith("ERROR").sum())
print("Created:", OUT)
