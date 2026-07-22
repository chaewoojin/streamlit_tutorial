"""Generate the web-loadable route files used by the advanced exercise."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from route_optimizer import PRESET_FILENAMES, points_from_frame, select_scenario_spots, solve_route


def precompute(data_path: Path, output_dir: Path) -> None:
    """Solve every named scenario and write its route as a CSV artifact."""
    spots = pd.read_csv(data_path)
    output_dir.mkdir(parents=True, exist_ok=True)

    for scenario, filename in PRESET_FILENAMES.items():
        selected = select_scenario_spots(spots, scenario)
        result = solve_route(points_from_frame(selected))
        result.insert(0, "scenario", scenario)
        output_path = output_dir / filename
        result.to_csv(output_path, index=False)
        seconds = float(result["compute_seconds"].iloc[0])
        print(f"{scenario}: {seconds:.2f}s -> {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data",
        type=Path,
        default=Path("study_spots.csv"),
        help="Study-spots CSV (default: study_spots.csv)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("precomputed"),
        help="Output directory (default: precomputed)",
    )
    args = parser.parse_args()
    precompute(args.data, args.output)


if __name__ == "__main__":
    main()
