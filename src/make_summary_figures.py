#!/usr/bin/env python3
"""Generate conservative summary figures from curated experimental metrics."""
from pathlib import Path
import argparse
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "processed" / "summary_metrics.csv"
OUT = ROOT / "figures" / "generated"


def save_bar(df, column, ylabel, filename):
    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    bars = ax.bar(df["condition"], df[column])
    ax.set_xlabel("WAAM wall condition")
    ax.set_ylabel(ylabel)
    ax.set_title(ylabel + " by wall condition")
    ax.grid(axis="y", alpha=0.25)
    for bar, value in zip(bars, df[column]):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height(), f"{value:g}",
                ha="center", va="bottom", fontsize=10)
    fig.tight_layout()
    fig.savefig(OUT / filename, dpi=220, bbox_inches="tight")
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="validate inputs before plotting")
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(DATA)
    expected = {"condition", "average_grain_size_um", "average_vickers_hardness_HV10"}
    missing = expected - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")
    if set(df["condition"]) != {"W1", "W2", "W3"}:
        raise ValueError("Expected exactly W1, W2, and W3")
    save_bar(df, "average_vickers_hardness_HV10", "Average Vickers hardness (HV10)", "hardness_by_condition.png")
    save_bar(df, "average_grain_size_um", "Average grain size (µm)", "grain_size_by_condition.png")
    if args.check:
        print("Input validation and figure generation completed successfully.")

if __name__ == "__main__":
    main()
