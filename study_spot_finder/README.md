# USC Study Spot Finder

A standalone Streamlit app for the USC Summer Scholars workshop. It contains:

- The original 90-row study-space finder.
- An exact inspection-route optimization problem using the existing coordinates.
- Three execution modes: direct computation, a worker process, and prepared data.
- Offline scripts and result files for three preset operations scenarios.

## Run it

```bash
cd study_spot_finder
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

On Windows, activate with `.venv\Scripts\Activate.ps1`.

## Rebuild the prepared results

```bash
python precompute_routes.py
```

This intentionally takes several seconds per scenario. It writes three CSV files
under `precomputed/`. The deployed app downloads those files from the repository;
before the branch is pushed, it falls back to the bundled local copies.

## Files

```text
app.py                 Streamlit finder and scaling comparison
study_spots.csv        Synthetic workshop dataset
route_optimizer.py     Pure CPU-heavy route calculation
precompute_routes.py   Offline batch computation
study_spot_data.py     Reproducible dataset generator
precomputed/           Prepared route-result files
```
