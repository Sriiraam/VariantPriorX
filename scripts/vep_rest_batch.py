import json
import time
import urllib.request
import urllib.error
from pathlib import Path

INPUT = Path("results/annotation/vep_input_variants.txt")
OUTPUT = Path("results/annotation/vep_annotations.jsonl")

BATCH_SIZE = 200
MAX_RETRIES = 5

URL = (
    "https://rest.ensembl.org/"
    "vep/homo_sapiens/region"
    "?canonical=1&mane=1&hgvs=1&variant_class=1&symbol=1"
)

variants = [
    line.strip()
    for line in INPUT.read_text().splitlines()
    if line.strip()
]

print(f"Total variants: {len(variants)}")

completed = 0

if OUTPUT.exists():
    with OUTPUT.open() as handle:
        completed = sum(1 for _ in handle)

    print(f"Existing annotations: {completed}")

remaining = variants[completed:]

with OUTPUT.open("a") as out:

    for start in range(0, len(remaining), BATCH_SIZE):

        batch = remaining[start:start + BATCH_SIZE]

        payload = json.dumps(
            {"variants": batch}
        ).encode()

        for attempt in range(1, MAX_RETRIES + 1):

            try:
                request = urllib.request.Request(
                    URL,
                    data=payload,
                    headers={
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                    },
                    method="POST",
                )

                with urllib.request.urlopen(
                    request,
                    timeout=120
                ) as response:
                    results = json.load(response)

                for result in results:
                    out.write(json.dumps(result) + "\n")

                out.flush()

                completed += len(results)

                print(
                    f"Annotated {completed}/{len(variants)}"
                )

                break

            except (
                urllib.error.HTTPError,
                urllib.error.URLError,
                TimeoutError,
            ) as error:

                print(
                    f"Attempt {attempt} failed: {error}"
                )

                if attempt == MAX_RETRIES:
                    raise

                time.sleep(attempt * 5)

        time.sleep(0.3)

print("VEP annotation complete.")
