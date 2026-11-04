"""Download a bounded, documented slice of ChEMBL activity records."""
import csv
import json
import math
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen

API = "https://www.ebi.ac.uk/chembl/api/data"
TARGET = "CHEMBL220"
FILTERS = {
    "target_chembl_id": TARGET,
    "standard_type": "IC50",
    "standard_units": "nM",
    "standard_relation": "=",
    "assay_type": "B",
    "order_by": "activity_id",
    "limit": 500,
}
DATA = Path(__file__).resolve().parent / "data"

def get_json(path):
    with urlopen(f"{API}/{path}", timeout=60) as response:
        return json.load(response)

def main():
    rows = []
    # Use a bounded slice for a quick demonstration, not a comprehensive benchmark.
    for offset in (0, 500):
        query = urlencode(dict(FILTERS, offset=offset))
        page = get_json(f"activity.json?{query}")
        for item in page["activities"]:
            try:
                nm = float(item["standard_value"])
            except (KeyError, TypeError, ValueError):
                continue
            smiles = item.get("canonical_smiles")
            if smiles and math.isfinite(nm) and nm > 0 and not item.get("data_validity_comment"):
                rows.append((item["activity_id"], smiles, 9 - math.log10(nm)))
        if not page["page_meta"]["next"]:
            break
    if not rows:
        raise SystemExit("No eligible activity records returned. Check the ChEMBL query.")
    DATA.mkdir(exist_ok=True)
    with (DATA / "demo_activity.csv").open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["activity_id", "smiles", "pIC50"])
        writer.writerows(rows)
    print(f"Saved {len(rows)} measurements for {TARGET}.")

if __name__ == "__main__":
    main()
