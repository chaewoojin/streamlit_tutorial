# Streamlit, taught in Streamlit

A self-teaching Streamlit workshop for USC undergraduates. The tutorial *is* a Streamlit app, so
every concept is demonstrated live next to the code that produced it.

## Run it

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Opens at `http://localhost:8501`.

## Deploy it (so students can read it before/after class)

1. Push this folder to a public GitHub repo.
2. Go to **share.streamlit.io** → sign in with GitHub → **Create app**.
3. Repo, branch `main`, main file `app.py` → **Deploy**.
4. Share the resulting `*.streamlit.app` URL.

No secrets or data files needed — the sample data is generated in code.

## What's inside

| Lesson | Covers |
|---|---|
| 0 | Framing, the 3-line app |
| 1 | venv, pip install, `streamlit run`, auto-rerun, install troubleshooting |
| 2 | **The rerun model** — the mental model everything else depends on |
| 3 | Text, status messages, metrics, dataframes, `st.data_editor` |
| 4 | All the widgets, forms, and the button-doesn't-latch trap |
| 5 | Columns, tabs, expanders, sidebar, placeholders, progress |
| 6 | Built-in charts, a filter→chart pattern, maps, other plotting libraries |
| 7 | `st.session_state` — counter, echo, growing list, live state inspector |
| 8 | `@st.cache_data` vs `@st.cache_resource`, with a timed demo |
| 9 | File upload, download button, media, the absolute-path deploy trap |
| 10 | `pages/` folder, `st.navigation`, shared modules, `config.toml` |
| 11 | `secrets.toml`, `.gitignore`, Community Cloud secrets |
| 12 | Pre-flight checklist, `requirements.txt`, git push, deploy, updating |
| 13 | Searchable troubleshooting list + debugging technique |
| 14 | **Build sheet** — students answer 6 questions and download a generated `app.py` starter |
| — | Printable cheat sheet |

Progress checkpoints across all lessons are tracked in the sidebar.

## Suggested 2-hour session

| Time | Activity |
|---|---|
| 0:00–0:15 | Lessons 0–1 together. Everyone gets `streamlit run` working before moving on. This is the step that strands people; budget for it. |
| 0:15–0:30 | Lesson 2 at the front. Do not skip it — most later confusion traces back here. |
| 0:30–1:00 | Lessons 3–6, students working through demos on their own with you circulating. |
| 1:00–1:20 | Lessons 7–9. Session state is the second conceptual hurdle. |
| 1:20–1:35 | Lesson 14 build sheet — students plan their own app and download the starter. |
| 1:35–2:00 | Lessons 11–12 live: everyone deploys. End with URLs posted in the class channel. |

Lessons 10 and 13 work well as assigned reading.

## A note on how the demos work

`run_and_show()` renders each snippet with `exec()`, so the "Code" tab is guaranteed to be exactly
what produced the "Live result" tab — they can never drift apart. This is a teaching device, not a
pattern to copy into student projects. Worth saying out loud if a sharp student asks.

## Customizing for your course

- Swap `load_sample_data()` for a dataset from your syllabus so demos match their homework.
- Edit the rubric list at the bottom of Lesson 14 to match your actual grading criteria.
- The USC palette lives in the `CARDINAL` / `GOLD` constants near the top of `app.py`.
