import csv
import time
import requests
from pathlib import Path

INPUT = Path("results/annotation/vep_clinical_candidates.tsv")
OUTPUT = Path("results/annotation/gnomad_frequency.tsv")

URL = "https://gnomad.broadinstitute.org/api"
DATASET = "gnomad_r4"

QUERY = """
query Variant($variantId: String!, $dataset: DatasetId!) {
  variant(variantId: $variantId, dataset: $dataset) {
    variantId
    exome {
      ac
      an
      af
    }
    genome {
      ac
      an
      af
    }
    joint {
      ac
      an
    }
  }
}
"""

with INPUT.open() as f:
    rows = list(csv.DictReader(f, delimiter="\t"))

done = set()

if OUTPUT.exists():
    with OUTPUT.open() as f:
        for row in csv.DictReader(f, delimiter="\t"):
            if row.get("status") in {"FOUND", "NOT_FOUND"}:
                done.add(row["variant_id"])

write_header = not OUTPUT.exists()

fields = [
    "variant_id",
    "exome_ac",
    "exome_an",
    "exome_af",
    "genome_ac",
    "genome_an",
    "genome_af",
    "joint_ac",
    "joint_an",
    "joint_af",
    "status"
]

with OUTPUT.open("a", newline="") as out:
    writer = csv.DictWriter(out, fieldnames=fields, delimiter="\t")

    if write_header:
        writer.writeheader()

    for i, row in enumerate(rows, 1):

        chrom = row["chrom"].replace("chr", "")
        variant_id = f"{chrom}-{row['pos']}-{row['ref']}-{row['alt']}"

        if variant_id in done:
            continue

        result_row = {field: "" for field in fields}
        result_row["variant_id"] = variant_id

        try:
            payload = {
                "query": QUERY,
                "variables": {
                    "variantId": variant_id,
                    "dataset": DATASET
                }
            }

            r = requests.post(URL, json=payload, timeout=60)

            if r.status_code == 200:
                body = r.json()

                if body.get("errors"):
                    messages = [
                        e.get("message", "")
                        for e in body["errors"]
                    ]

                    if any(
                        "Variant not found" in m
                        for m in messages
                    ):
                        result_row["status"] = "NOT_FOUND"
                    else:
                        result_row["status"] = "GRAPHQL_ERROR"

                else:
                    variant = body.get("data", {}).get("variant")

                    if variant:
                        exome = variant.get("exome") or {}
                        genome = variant.get("genome") or {}
                        joint = variant.get("joint") or {}

                        result_row["exome_ac"] = exome.get("ac", "")
                        result_row["exome_an"] = exome.get("an", "")
                        result_row["exome_af"] = exome.get("af", "")

                        result_row["genome_ac"] = genome.get("ac", "")
                        result_row["genome_an"] = genome.get("an", "")
                        result_row["genome_af"] = genome.get("af", "")

                        joint_ac = joint.get("ac")
                        joint_an = joint.get("an")

                        result_row["joint_ac"] = (
                            joint_ac if joint_ac is not None else ""
                        )
                        result_row["joint_an"] = (
                            joint_an if joint_an is not None else ""
                        )

                        if joint_ac is not None and joint_an:
                            result_row["joint_af"] = joint_ac / joint_an

                        result_row["status"] = "FOUND"

                    else:
                        result_row["status"] = "NOT_FOUND"

            else:
                result_row["status"] = f"HTTP_{r.status_code}"

        except Exception as e:
            result_row["status"] = f"ERROR:{type(e).__name__}"

        writer.writerow(result_row)
        out.flush()

        print(
            f"{i}/{len(rows)}  "
            f"{variant_id}  "
            f"{result_row['status']}  "
            f"joint_AF={result_row['joint_af']}"
        )

        time.sleep(6.5)

print("gnomAD query complete.")
