import json
import csv
from pathlib import Path

INPUT = Path("results/annotation/vep_annotations.jsonl")
OUTPUT = Path("results/annotation/vep_annotations.tsv")

FIELDS = [
    "chrom",
    "pos",
    "ref",
    "alt",
    "most_severe_consequence",
    "gene_symbol",
    "gene_id",
    "transcript_id",
    "impact",
    "canonical",
    "mane_select",
    "hgvsc",
    "hgvsp",
    "variant_class",
]

with INPUT.open() as infile, OUTPUT.open("w", newline="") as outfile:
    writer = csv.DictWriter(outfile, fieldnames=FIELDS, delimiter="\t")
    writer.writeheader()

    count = 0

    for line in infile:
        result = json.loads(line)

        input_fields = result.get("input", "").split()
        if len(input_fields) < 5:
            continue

        chrom, pos, _, ref, alt = input_fields[:5]

        transcripts = result.get("transcript_consequences", [])

        selected = None

        if transcripts:
            selected = next(
                (t for t in transcripts if t.get("mane_select")),
                None
            )

            if selected is None:
                selected = next(
                    (t for t in transcripts if t.get("canonical") == 1),
                    None
                )

            if selected is None:
                selected = transcripts[0]

        selected = selected or {}

        writer.writerow({
            "chrom": chrom,
            "pos": pos,
            "ref": ref,
            "alt": alt,
            "most_severe_consequence":
                result.get("most_severe_consequence", ""),
            "gene_symbol":
                selected.get("gene_symbol", ""),
            "gene_id":
                selected.get("gene_id", ""),
            "transcript_id":
                selected.get("transcript_id", ""),
            "impact":
                selected.get("impact", ""),
            "canonical":
                selected.get("canonical", ""),
            "mane_select":
                selected.get("mane_select", ""),
            "hgvsc":
                selected.get("hgvsc", ""),
            "hgvsp":
                selected.get("hgvsp", ""),
            "variant_class":
                result.get("variant_class", ""),
        })

        count += 1

print(f"Parsed variants: {count}")
print(f"Output: {OUTPUT}")
