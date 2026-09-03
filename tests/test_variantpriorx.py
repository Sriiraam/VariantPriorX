import sqlite3
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RANKED = ROOT / "results" / "annotation" / "variantpriorx_ranked.tsv"
DB = ROOT / "database" / "variantpriorx.db"


def load_ranked():
    return pd.read_csv(RANKED, sep="\t")


def test_ranked_file_exists():
    assert RANKED.exists()


def test_database_exists():
    assert DB.exists()


def test_total_variants():
    df = load_ranked()
    assert len(df) == 497


def test_unique_variants():
    df = load_ranked()
    assert df["variant_id"].nunique() == 497
    assert not df["variant_id"].duplicated().any()


def test_impact_counts():
    df = load_ranked()

    assert (df["max_impact"] == "HIGH").sum() == 55
    assert (df["max_impact"] == "MODERATE").sum() == 442


def test_gnomad_status_counts():
    df = load_ranked()

    counts = df["status"].value_counts()

    assert counts.get("FOUND", 0) == 475
    assert counts.get("NOT_FOUND", 0) == 20
    assert counts.get("ERROR:JSONDecodeError", 0) == 2


def test_score_range():
    df = load_ranked()

    assert df["variantpriorx_score"].max() == 7
    assert df["variantpriorx_score"].min() == -5


def test_top_score_variants():
    df = load_ranked()

    top = df[df["variantpriorx_score"] == 7]

    assert len(top) == 2
    assert {"CLCN7", "EEF1A2"}.issubset(set(top["gene_symbol"]))


def test_frequency_missing_not_zero():
    df = load_ranked()

    missing = df[df["status"] != "FOUND"]

    assert missing["frequency_score"].fillna(0).eq(0).all()


def test_database_integrity():
    conn = sqlite3.connect(DB)

    count = conn.execute(
        "SELECT COUNT(*) FROM variants"
    ).fetchone()[0]

    unique_count = conn.execute(
        "SELECT COUNT(DISTINCT variant_id) FROM variants"
    ).fetchone()[0]

    conn.close()

    assert count == 497
    assert unique_count == 497
