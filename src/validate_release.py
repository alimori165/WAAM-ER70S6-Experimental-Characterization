#!/usr/bin/env python3
"""Validate the public release against the repository's conservative data policy."""
from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / "data" / "processed" / "summary_metrics.csv"
FORBIDDEN_PUBLIC_COLUMNS = {
    "heat_input", "elongation", "toughness", "fracture_toughness", "kic",
    "cooling_rate", "delta_t8_5", "uts", "ys"
}


def main():
    with SUMMARY.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        columns = {c.lower() for c in (reader.fieldnames or [])}
        overlap = columns & FORBIDDEN_PUBLIC_COLUMNS
        if overlap:
            raise SystemExit(f"Unverified fields found in public summary: {sorted(overlap)}")
        rows = list(reader)
    if [r["condition"] for r in rows] != ["W1", "W2", "W3"]:
        raise SystemExit("Condition order must be W1, W2, W3")
    for r in rows:
        if float(r["average_grain_size_um"]) <= 0 or float(r["average_vickers_hardness_HV10"]) <= 0:
            raise SystemExit("Metrics must be positive")
    required_figures = [
        ROOT / "figures" / "source" / "experimental_setup.jpg",
        ROOT / "figures" / "source" / "sampling_layout.jpg",
        ROOT / "figures" / "source" / "tensile_fractography_overview.jpg",
    ]
    missing = [str(p.relative_to(ROOT)) for p in required_figures if not p.exists()]
    if missing:
        raise SystemExit(f"Missing required figures: {missing}")
    print("Release validation passed.")

if __name__ == "__main__":
    main()
