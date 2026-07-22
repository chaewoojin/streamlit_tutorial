"""Deterministic synthetic data used by the tutorial and starter kit."""

import numpy as np
import pandas as pd


def make_study_spots(n: int = 90) -> pd.DataFrame:
    """Return the synthetic USC study-space dataset used in the workshop."""
    rng = np.random.default_rng(11)
    buildings = ["Leavey", "Doheny", "Annenberg", "Tutor Center", "SGM", "Fertitta"]
    rooms = [
        "Reading Room",
        "3rd Floor",
        "Atrium",
        "Quiet Wing",
        "Courtyard",
        "Basement",
        "Lounge",
    ]
    building = rng.choice(buildings, n)
    raw_names = [f"{b} {r}" for b, r in zip(building, rng.choice(rooms, n))]

    seen: dict[str, int] = {}
    names: list[str] = []
    for raw_name in raw_names:
        seen[raw_name] = seen.get(raw_name, 0) + 1
        suffix = seen[raw_name]
        names.append(raw_name if suffix == 1 else f"{raw_name} {suffix}")

    return pd.DataFrame(
        {
            "spot": names,
            "building": building,
            "seats": rng.integers(6, 120, n),
            "noise": rng.choice(["Silent", "Low", "Medium"], n, p=[0.3, 0.45, 0.25]),
            "outlets": rng.choice([True, False], n, p=[0.7, 0.3]),
            "rating": (rng.normal(3.9, 0.6, n).clip(1, 5)).round(1),
            "lat": rng.normal(34.0224, 0.0035, n).round(5),
            "lon": rng.normal(-118.2851, 0.0035, n).round(5),
        }
    )
