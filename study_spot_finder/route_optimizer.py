"""Pure-Python route optimization used by the advanced Streamlit exercise.

This module deliberately contains no Streamlit calls. Keeping computation in an
importable module allows the same function to run offline, in the Streamlit
process (the baseline), or in a ProcessPoolExecutor worker (the improved app).
"""

from __future__ import annotations

from itertools import permutations
from math import asin, cos, factorial, radians, sin, sqrt
from time import perf_counter
from typing import Iterable

import pandas as pd


PRESET_FILENAMES = {
    "High-capacity audit": "high_capacity_audit.csv",
    "Quiet-space audit": "quiet_space_audit.csv",
    "Outlet-maintenance round": "outlet_maintenance_round.csv",
}

PRECOMPUTED_BASE_URL = (
    "https://raw.githubusercontent.com/chaewoojin/streamlit_tutorial/"
    "main/study_spot_finder/precomputed"
)

Point = tuple[str, float, float]


def select_scenario_spots(spots: pd.DataFrame, scenario: str, count: int = 11) -> pd.DataFrame:
    """Choose a deterministic set of locations for one operations scenario."""
    if scenario == "High-capacity audit":
        selected = spots.sort_values(
            ["seats", "rating", "spot"], ascending=[False, False, True]
        ).head(count)
    elif scenario == "Quiet-space audit":
        selected = spots.loc[spots["noise"].eq("Silent")].sort_values(
            ["rating", "seats", "spot"], ascending=[False, False, True]
        ).head(count)
    elif scenario == "Outlet-maintenance round":
        selected = spots.loc[spots["outlets"].eq(True)].sort_values(  # noqa: E712
            ["rating", "seats", "spot"], ascending=[False, False, True]
        ).head(count)
    else:
        raise ValueError(f"Unknown scenario: {scenario}")

    if len(selected) < count:
        raise ValueError(f"Scenario {scenario!r} has only {len(selected)} eligible spots")

    # Sorting fixes the starting location, making offline and live results identical.
    return selected.sort_values("spot").reset_index(drop=True)


def points_from_frame(spots: pd.DataFrame) -> tuple[Point, ...]:
    """Convert a DataFrame to small, hashable and process-safe inputs."""
    return tuple(
        (str(row.spot), float(row.lat), float(row.lon))
        for row in spots[["spot", "lat", "lon"]].itertuples(index=False)
    )


def _distance_km(a: Point, b: Point) -> float:
    """Return great-circle distance between two latitude/longitude points."""
    earth_radius_km = 6371.0088
    lat1, lon1, lat2, lon2 = map(radians, (a[1], a[2], b[1], b[2]))
    delta_lat = lat2 - lat1
    delta_lon = lon2 - lon1
    haversine = (
        sin(delta_lat / 2) ** 2
        + cos(lat1) * cos(lat2) * sin(delta_lon / 2) ** 2
    )
    return 2 * earth_radius_km * asin(sqrt(haversine))


def solve_route(points: Iterable[Point]) -> pd.DataFrame:
    """Find the shortest round trip by enumerating every possible visit order.

    The first point is fixed as the start. Eleven points therefore require
    evaluating 10! = 3,628,800 routes, which is intentionally substantial enough
    to make the app-design tradeoff visible in a classroom demonstration.
    """
    locations = tuple(points)
    if not 2 <= len(locations) <= 11:
        raise ValueError("The teaching solver accepts between 2 and 11 locations")

    names = [point[0] for point in locations]
    if len(names) != len(set(names)):
        raise ValueError("Every location must have a unique name")

    started = perf_counter()
    n_locations = len(locations)
    distances = [
        [_distance_km(origin, destination) for destination in locations]
        for origin in locations
    ]

    best_distance = float("inf")
    best_middle: tuple[int, ...] | None = None

    for middle in permutations(range(1, n_locations)):
        total = distances[0][middle[0]]
        total += sum(
            distances[middle[index]][middle[index + 1]]
            for index in range(len(middle) - 1)
        )
        total += distances[middle[-1]][0]
        if total < best_distance:
            best_distance = total
            best_middle = middle

    assert best_middle is not None
    visit_order = (0, *best_middle, 0)
    elapsed = perf_counter() - started
    route_count = factorial(n_locations - 1)

    rows: list[dict[str, object]] = []
    cumulative = 0.0
    for visit, location_index in enumerate(visit_order, start=1):
        leg_distance = 0.0
        if visit > 1:
            previous_index = visit_order[visit - 2]
            leg_distance = distances[previous_index][location_index]
            cumulative += leg_distance

        name, latitude, longitude = locations[location_index]
        rows.append(
            {
                "visit": visit,
                "spot": name,
                "lat": latitude,
                "lon": longitude,
                "leg_km": leg_distance,
                "cumulative_km": cumulative,
                "total_km": best_distance,
                "routes_evaluated": route_count,
                "compute_seconds": elapsed,
            }
        )

    return pd.DataFrame(rows)
