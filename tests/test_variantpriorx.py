import sqlite3
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "database" / "variantpriorx.db"


def load_variants():
    conn = sqlite3.connect(DB)
    df = pd.read_sql_query("SELECT * FROM variants", conn)
    conn.close()
    return df


def test_database_exists():
    assert DB.exists()


def test_total_variants():
    df = load_variants()
    assert len(df) == 497


def test_unique_variants():
    df = load_variants()
    assert df["variant_id"].nunique() == 497
    assert not df["variant_id"].duplicated().any()


def test_impact_counts():
    df = load_variants()

    assert (df["max_impact"] == "HIGH").sum() == 55
    assert (df["max_impact"] == "MODERATE").sum() == 442


def test_gnomad_status_counts():
    df = load_variants()

    counts = df["status"].value_counts()

    assert counts.get("FOUND", 0) == 475
    assert counts.get("NOT_FOUND", 0) == 20
    assert counts.get("ERROR:JSONDecodeError", 0) == 2


def test_score_range():
    df = load_variants()

    assert df["variantpriorx_score"].max() == 7
    assert df["variantpriorx_score"].min() == -5


def test_top_score_variants():
    df = load_variants()

    top = df[df["variantpriorx_score"] == 7]

    assert len(top) == 2
    assert {"CLCN7", "EEF1A2"}.issubset(set(top["gene_symbol"]))


def test_frequency_missing_not_zero():
    df = load_variants()

    missing = df[df["status"] != "FOUND"]

    assert missing["frequency_score"].fillna(0).eq(0).all()


def test_database_row_integrity():
    df = load_variants()

    assert df["variant_id"].notna().all()
    assert df["variantpriorx_score"].notna().all()


def test_database_sql_integrity():
    conn = sqlite3.connect(DB)

    total = conn.execute(
        "SELECT COUNT(*) FROM variants"
    ).fetchone()[0]

    unique = conn.execute(
        "SELECT COUNT(DISTINCT variant_id) FROM variants"
    ).fetchone()[0]

    conn.close()

    assert total == 497
    assert unique == 497
