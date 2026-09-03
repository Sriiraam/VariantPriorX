import pandas as pd
import sqlite3
from pathlib import Path

INPUT = "results/annotation/variantpriorx_ranked.tsv"
DB = "database/variantpriorx.db"

Path("database").mkdir(exist_ok=True)

df = pd.read_csv(INPUT, sep="\t")

conn = sqlite3.connect(DB)

df.to_sql(
    "variants",
    conn,
    if_exists="replace",
    index=False
)

conn.execute(
    "CREATE UNIQUE INDEX IF NOT EXISTS idx_variant_id "
    "ON variants(variant_id)"
)

conn.execute(
    "CREATE INDEX IF NOT EXISTS idx_gene "
    "ON variants(gene_symbol)"
)

conn.execute(
    "CREATE INDEX IF NOT EXISTS idx_score "
    "ON variants(variantpriorx_score)"
)

conn.execute(
    "CREATE INDEX IF NOT EXISTS idx_clinvar "
    "ON variants(clnsig)"
)

conn.commit()

print("Database:", DB)

rows = conn.execute(
    "SELECT COUNT(*) FROM variants"
).fetchone()[0]

unique_variants = conn.execute(
    "SELECT COUNT(DISTINCT variant_id) FROM variants"
).fetchone()[0]

print("Rows:", rows)
print("Unique variants:", unique_variants)

print("\nTop 10 ranked variants:")

query = """
SELECT
    rank,
    variant_id,
    gene_symbol,
    max_impact,
    frequency_class,
    variantpriorx_score
FROM variants
ORDER BY rank
LIMIT 10
"""

for row in conn.execute(query):
    print(row)

conn.close()
