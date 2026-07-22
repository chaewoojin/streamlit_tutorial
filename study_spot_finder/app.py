"""USC Study Spot Finder with an OR/MS scaling demonstration.

Run from this directory with:
    streamlit run app.py
"""

from __future__ import annotations

import io
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen

import pandas as pd
import streamlit as st

from route_optimizer import (
    PRECOMPUTED_BASE_URL,
    PRESET_FILENAMES,
    points_from_frame,
    select_scenario_spots,
    solve_route,
)


APP_DIR = Path(__file__).resolve().parent


def load_precomputed_file(filename: str) -> tuple[pd.DataFrame, str]:
    """Download a prepared result, falling back locally before GitHub is updated."""
    url = f"{PRECOMPUTED_BASE_URL}/{filename}"
    try:
        with urlopen(url, timeout=5) as response:
            result = pd.read_csv(io.BytesIO(response.read()))
        return result, "prepared web file + st.cache_data"
    except (URLError, TimeoutError, OSError):
        result = pd.read_csv(APP_DIR / "precomputed" / filename)
        return result, "prepared local fallback + st.cache_data"


def render_finder(spots: pd.DataFrame) -> None:
    """Render the original filtering exercise."""
    st.title("USC Study Spot Finder")
    st.write("Filter 90 synthetic campus study spaces by building, rating and amenities.")

    with st.sidebar:
        st.header("Finder filters")
        buildings = st.multiselect(
            "Building",
            sorted(spots["building"].unique()),
            default=sorted(spots["building"].unique()),
        )
        minimum_rating = st.slider("Minimum rating", 1.0, 5.0, 3.5, 0.1)
        silent_only = st.checkbox("Silent spots only")
        outlets_only = st.checkbox("Outlets required")

    hits = spots.loc[
        spots["building"].isin(buildings)
        & spots["rating"].ge(minimum_rating)
    ]
    if silent_only:
        hits = hits.loc[hits["noise"].eq("Silent")]
    if outlets_only:
        hits = hits.loc[hits["outlets"].eq(True)]  # noqa: E712

    if hits.empty:
        st.warning("No study spots match. Try loosening a filter.")
        return

    first, second, third = st.columns(3)
    first.metric("Spots", len(hits))
    second.metric("Seats", int(hits["seats"].sum()))
    third.metric("Average rating", f"{hits['rating'].mean():.2f}")

    st.dataframe(hits, hide_index=True, width="stretch")

    chart_column, map_column = st.columns(2)
    with chart_column:
        st.subheader("Seats by building")
        st.bar_chart(hits.groupby("building")["seats"].sum())
    with map_column:
        st.subheader("Locations")
        st.map(hits, latitude="lat", longitude="lon", size=14)


def render_route(route: pd.DataFrame, waited: float, source: str) -> None:
    """Render the common result returned by all three acquisition strategies."""
    first, second, third = st.columns(3)
    first.metric("Shortest round trip", f"{float(route['total_km'].iloc[0]):.2f} km")
    second.metric("Routes evaluated", f"{int(route['routes_evaluated'].iloc[0]):,}")
    third.metric("Time you waited", f"{waited:.2f} s")
    st.caption(f"Result source: **{source}**")

    table_column, map_column = st.columns([3, 2])
    with table_column:
        st.dataframe(
            route[["visit", "spot", "leg_km", "cumulative_km"]],
            hide_index=True,
            width="stretch",
            column_config={
                "visit": "Stop",
                "spot": "Study spot",
                "leg_km": st.column_config.NumberColumn("Leg (km)", format="%.3f"),
                "cumulative_km": st.column_config.NumberColumn(
                    "Total (km)", format="%.3f"
                ),
            },
        )
    with map_column:
        st.map(route.iloc[:-1], latitude="lat", longitude="lon", size=18)


def render_route_lab(
    spots: pd.DataFrame,
    load_precomputed,
    run_in_worker,
) -> None:
    """Let students compare direct, worker, and precomputed execution paths."""
    st.title("Study-Spot Route Optimization Lab")
    st.write(
        "A facilities manager must inspect 11 spaces and return to the start. "
        "The exact teaching solver evaluates 10! = 3,628,800 visit orders."
    )

    scenario = st.selectbox("Inspection scenario", list(PRESET_FILENAMES))
    source = st.radio(
        "How should the route be obtained?",
        [
            "Run in the Streamlit process — blocking",
            "Run in a worker process — isolated",
            "Load a prepared result — fast",
        ],
    )

    selected = select_scenario_spots(spots, scenario)
    points = points_from_frame(selected)
    st.caption(f"{len(points)} locations · {3_628_800:,} candidate routes")

    if source.startswith("Load"):
        button_label = "Load prepared route"
        spinner_text = "Downloading the prepared result..."
    elif source.startswith("Run in a worker"):
        button_label = "Optimize in worker process"
        spinner_text = "Worker is evaluating 3,628,800 routes..."
    else:
        button_label = "Optimize in app process"
        spinner_text = "The Streamlit process is evaluating 3,628,800 routes..."

    if st.button(button_label, type="primary"):
        started = time.perf_counter()
        with st.spinner(spinner_text):
            if source.startswith("Load"):
                route, result_source = load_precomputed(PRESET_FILENAMES[scenario])
            elif source.startswith("Run in a worker"):
                route = run_in_worker(points)
                result_source = "ProcessPoolExecutor worker + st.cache_data"
            else:
                route = solve_route(points)
                result_source = "direct call in the Streamlit app process"

        st.session_state["route_result"] = {
            "scenario": scenario,
            "mode": source,
            "route": route,
            "waited": time.perf_counter() - started,
            "source": result_source,
        }

    saved = st.session_state.get("route_result")
    if saved and saved["scenario"] == scenario and saved["mode"] == source:
        render_route(saved["route"], saved["waited"], saved["source"])

    with st.expander("What changes between the three modes?"):
        st.markdown(
            """
            - **Direct:** the current Streamlit run performs every calculation and waits.
            - **Worker:** the user still waits for `future.result()`, but CPU-heavy Python runs
              in a separate process. Identical requests are cached.
            - **Prepared:** an offline script already solved the known scenario. The app only
              downloads a small result file and renders it.
            """
        )


def render_architecture() -> None:
    st.title("Why these strategies matter")
    st.markdown(
        """
        Streamlit reruns the script after widget interactions. Fast filtering should remain
        simple; expensive work needs an explicit execution boundary.

        **1. A button or form** prevents every widget change from launching optimization.

        **2. `st.cache_data`** remembers identical data or computation requests within the
        running app.

        **3. Offline precomputation** creates durable results before users arrive. Unlike a
        cache, those result files survive application restarts.

        **4. `ProcessPoolExecutor`** isolates optional CPU-heavy live work from the Streamlit
        app process. It does not make `future.result()` non-blocking for the requesting user.
        """
    )
    st.code(
        "python precompute_routes.py\nstreamlit run app.py",
        language="bash",
    )
    st.info(
        "For production jobs that should continue after the user leaves, replace the local "
        "worker pool with a job service or separate HTTP backend."
    )


def main() -> None:
    st.set_page_config(
        page_title="USC Study Spot Finder",
        page_icon="📍",
        layout="wide",
    )

    # These Streamlit decorators live behind the main guard. Spawned worker
    # processes import this module as __mp_main__, so they do not initialize UI
    # caches or resources of their own.
    @st.cache_data
    def load_spots() -> pd.DataFrame:
        return pd.read_csv(APP_DIR / "study_spots.csv")

    @st.cache_data(show_spinner=False)
    def load_precomputed(filename: str) -> tuple[pd.DataFrame, str]:
        return load_precomputed_file(filename)

    @st.cache_resource
    def get_executor() -> ProcessPoolExecutor:
        return ProcessPoolExecutor(max_workers=2)

    @st.cache_data(show_spinner=False)
    def run_in_worker(
        points: tuple[tuple[str, float, float], ...],
    ) -> pd.DataFrame:
        future = get_executor().submit(solve_route, points)
        return future.result()

    page = st.segmented_control(
        "Page",
        ["Finder", "Route optimization", "Architecture"],
        default="Finder",
        label_visibility="collapsed",
    )
    spots = load_spots()

    if page == "Route optimization":
        render_route_lab(spots, load_precomputed, run_in_worker)
    elif page == "Architecture":
        render_architecture()
    else:
        render_finder(spots)


if __name__ == "__main__":
    main()
