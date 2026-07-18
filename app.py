"""
Hourly Streamlit Tutorial — a workshop app for USC Summer Scholars.

Run:  streamlit run app.py
"""

import io
import textwrap
import time
import zipfile

import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Hourly Streamlit Tutorial",
    page_icon="◑",
    layout="centered",
    initial_sidebar_state="collapsed",
)

INK = "#17130F"
MUTED = "#7A736C"
CARDINAL = "#990000"
GOLD = "#FFC72C"
RULE = "#E6E1DA"

st.markdown(
    f"""
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,800&family=JetBrains+Mono:wght@400;500&display=swap');

      section[data-testid="stSidebar"] {{ display: none; }}
      header[data-testid="stHeader"] {{ background: transparent; }}
      .block-container {{ padding-top: 5.5rem; padding-bottom: 5rem; max-width: 46rem; }}

      .wordmark {{
        font-family: 'JetBrains Mono', monospace; font-size: 0.7rem;
        letter-spacing: 0.18em; text-transform: uppercase; color: {MUTED};
        margin-bottom: 1.1rem;
      }}
      .wordmark b {{ color: {INK}; font-weight: 500; }}

      h1, h2, h3 {{
        font-family: 'Bricolage Grotesque', system-ui, sans-serif !important;
        letter-spacing: -0.025em !important;
        color: {INK} !important;
      }}
      h1 {{ font-weight: 800 !important; font-size: 2.5rem !important; line-height: 1.05 !important; }}
      h2 {{ font-weight: 800 !important; font-size: 1.35rem !important; margin-top: 2.2rem !important; }}
      h3 {{ font-weight: 500 !important; font-size: 1.05rem !important; }}

      .stMarkdown p {{ line-height: 1.65; }}
      code, pre, .stCode {{ font-family: 'JetBrains Mono', monospace !important; }}

      /* the hour, drawn to scale */
      .rail {{ display: flex; gap: 3px; margin: 1.1rem 0 0.5rem 0; }}
      .rail span {{ height: 5px; border-radius: 3px; background: {RULE}; }}
      .rail span.on {{ background: {CARDINAL}; }}
      .rail span.done {{ background: {GOLD}; }}
      .railcap {{
        font-family: 'JetBrains Mono', monospace; font-size: 0.68rem;
        letter-spacing: 0.1em; text-transform: uppercase; color: {MUTED};
        display: flex; justify-content: space-between; margin-bottom: 2.6rem;
      }}

      .lede {{ font-size: 1.12rem; line-height: 1.6; color: {INK}; }}
      .note {{
        border-left: 2px solid {CARDINAL}; padding: 0.1rem 0 0.1rem 0.9rem;
        color: {INK}; margin: 1.2rem 0; font-size: 0.97rem; line-height: 1.6;
      }}
      .stepno {{
        font-family: 'JetBrains Mono', monospace; font-size: 0.72rem;
        letter-spacing: 0.16em; color: {CARDINAL}; text-transform: uppercase;
      }}
      .check {{
        font-size: 0.9rem; color: {MUTED}; border-top: 1px solid {RULE};
        padding-top: 0.6rem; margin-top: 0.2rem;
      }}
      hr {{ border-color: {RULE} !important; }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
STEPS = [
    ("Why", 3),
    ("Set up", 8),
    ("One idea", 6),
    ("Toolkit", 10),
    ("Build", 22),
    ("Ship", 8),
    ("Look up", 3),
]
NAMES = [s[0] for s in STEPS]


def demo(code: str):
    """Run a snippet and show the exact source beside it."""
    code = textwrap.dedent(code).strip()
    a, b = st.tabs(["Result", "Code"])
    with b:
        st.code(code, language="python")
    with a:
        exec(code, globals())  # teaching device only


@st.cache_data
def study_spots(n: int = 90) -> pd.DataFrame:
    rng = np.random.default_rng(11)
    buildings = ["Leavey", "Doheny", "Annenberg", "Tutor Center", "SGM", "Fertitta"]
    rooms = ["Reading Room", "3rd Floor", "Atrium", "Quiet Wing", "Courtyard", "Basement", "Lounge"]
    b = rng.choice(buildings, n)
    raw = [f"{x} {y}" for x, y in zip(b, rng.choice(rooms, n))]
    seen, names = {}, []
    for r in raw:
        seen[r] = seen.get(r, 0) + 1
        names.append(r if seen[r] == 1 else f"{r} {seen[r]}")
    return pd.DataFrame(
        {
            "spot": names,
            "building": b,
            "seats": rng.integers(6, 120, n),
            "noise": rng.choice(["Silent", "Low", "Medium"], n, p=[0.3, 0.45, 0.25]),
            "outlets": rng.choice([True, False], n, p=[0.7, 0.3]),
            "rating": (rng.normal(3.9, 0.6, n).clip(1, 5)).round(1),
            "lat": rng.normal(34.0224, 0.0035, n).round(5),
            "lon": rng.normal(-118.2851, 0.0035, n).round(5),
        }
    )


def starter_zip() -> bytes:
    df = study_spots()
    app = textwrap.dedent(
        '''
        import streamlit as st
        import pandas as pd

        st.title("USC Study Spot Finder")

        df = pd.read_csv("study_spots.csv")
        st.dataframe(df)
        '''
    ).strip()
    readme = textwrap.dedent(
        """
        # Study Spot Finder — workshop starter

        1. python3 -m venv .venv && source .venv/bin/activate
        2. pip install -r requirements.txt
        3. streamlit run app.py

        Then follow steps 2-6 in the workshop app.
        """
    ).strip()
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("study_spots.csv", df.to_csv(index=False))
        z.writestr("app.py", app + "\n")
        z.writestr("requirements.txt", "streamlit\npandas\n")
        z.writestr("README.md", readme + "\n")
        z.writestr(".gitignore", ".venv/\n__pycache__/\n.streamlit/secrets.toml\n.DS_Store\n")
    return buf.getvalue()


# ---------------------------------------------------------------------------
# Navigation + the hour, drawn to scale
# ---------------------------------------------------------------------------
st.markdown(
    '<div class="wordmark"><b>Hourly Streamlit Tutorial</b> &nbsp;·&nbsp; 2026 USC Summer Scholars</div>',
    unsafe_allow_html=True,
)

choice = st.segmented_control("Section", NAMES, default="Why", key="nav",
                              label_visibility="collapsed")
current = choice or "Why"
idx = NAMES.index(current)

bars = "".join(
    f'<span style="flex:{m}" class="{"on" if i == idx else "done" if i < idx else ""}"></span>'
    for i, (_, m) in enumerate(STEPS)
)
st.markdown(
    f'<div class="rail">{bars}</div>'
    f'<div class="railcap"><span>{current} · {STEPS[idx][1]} min</span>'
    f'<span>{sum(m for _, m in STEPS[:idx])} / 60 elapsed</span></div>',
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------------
if current == "Why":
    st.title("You will not learn Streamlit today.")
    st.markdown(
        '<p class="lede">You will build one working app, put it on the internet, '
        'and learn how to look up everything else.</p>',
        unsafe_allow_html=True,
    )

    st.write(
        "Streamlit turns a Python script into a web app. No HTML, no JavaScript, no server. "
        "Here is a complete, working application:"
    )
    demo(
        """
        import streamlit as st

        st.title("My app")
        st.write("Hello 👋")
        """
    )

    st.markdown(
        '<div class="note">Nobody memorizes this library. You write a line, run it, '
        'see it, and search the docs when you need something new. That loop — not a feature '
        'list — is what you are here to practice.</div>',
        unsafe_allow_html=True,
    )

    st.markdown("## The hour")
    st.markdown(
        """
        **Set up** · get it running on your laptop  
        **One idea** · the single concept that explains Streamlit's behavior  
        **Toolkit** · the ten functions that cover most apps  
        **Build** · a real app, six small steps  
        **Ship** · a public URL you can send to anyone
        """
    )
    st.caption("Then you do the same thing with your own project.")

# ---------------------------------------------------------------------------
elif current == "Set up":
    st.title("Set up")
    st.markdown('<p class="lede">Four commands. Everything after this assumes they worked.</p>',
                unsafe_allow_html=True)

    os_choice = st.segmented_control("OS", ["macOS / Linux", "Windows"], default="macOS / Linux",
                                     key="os", label_visibility="collapsed")
    if os_choice == "Windows":
        st.code(
            "mkdir study-spots; cd study-spots\n"
            "py -m venv .venv\n"
            ".venv\\Scripts\\Activate.ps1\n"
            "pip install streamlit pandas",
            language="bash",
        )
    else:
        st.code(
            "mkdir study-spots && cd study-spots\n"
            "python3 -m venv .venv\n"
            "source .venv/bin/activate\n"
            "pip install streamlit pandas",
            language="bash",
        )
    st.markdown('<p class="check">Your prompt now starts with (.venv). That is how you know it worked.</p>',
                unsafe_allow_html=True)

    st.markdown("## Then run something")
    st.write("Save this as `app.py`:")
    st.code('import streamlit as st\n\nst.title("It works")', language="python")
    st.code("streamlit run app.py", language="bash")
    st.write(
        "Your browser opens at `localhost:8501`. That terminal is now your app — leave it running, "
        "`Ctrl+C` stops it."
    )

    st.markdown(
        '<div class="note">Edit the file, hit save, and the page offers to rerun. '
        'Open the ⋮ menu and turn on <b>Always rerun</b> — now saving updates the app instantly. '
        'Keep your editor and browser side by side for the rest of the hour.</div>',
        unsafe_allow_html=True,
    )

    with st.expander("It didn't work"):
        st.markdown(
            """
            **`command not found: streamlit`** — the venv isn't active. Run the activate line again,
            or use `python -m streamlit run app.py`.

            **Windows opens the Microsoft Store** — use `py` instead of `python`.

            **Port already in use** — an app is still running somewhere.
            `streamlit run app.py --server.port 8502`.
            """
        )

# ---------------------------------------------------------------------------
elif current == "One idea":
    st.title("Your script reruns. All of it.")
    st.markdown(
        '<p class="lede">Every time anyone touches a widget, Streamlit runs your file again '
        'from line 1, with the new value in place.</p>',
        unsafe_allow_html=True,
    )

    demo(
        """
        st.write("Script ran at", time.strftime("%H:%M:%S"))
        n = st.slider("Move me", 0, 100, 25, key="d_slider")
        st.write("Value:", n)
        """
    )
    st.markdown('<p class="check">Move the slider. The timestamp changes — because line one ran again.</p>',
                unsafe_allow_html=True)

    st.markdown("## So a normal variable can't remember anything")
    left, right = st.columns(2)
    with left:
        st.markdown("**Broken**")
        st.code('count = 0\nif st.button("+1"):\n    count += 1\nst.write(count)', language="python")
        if st.button("+1", key="broken_btn"):
            pass
        st.write("Count: 0")
        st.caption("Resets on every rerun.")
    with right:
        st.markdown("**Fixed**")
        st.code(
            'st.session_state.setdefault("c", 0)\nif st.button("+1"):\n'
            '    st.session_state.c += 1\nst.write(st.session_state.c)',
            language="python",
        )
        st.session_state.setdefault("c", 0)
        if st.button("+1", key="fixed_btn"):
            st.session_state.c += 1
        st.write("Count:", st.session_state.c)
        st.caption("`st.session_state` survives reruns.")

    st.markdown(
        '<div class="note">Almost every "why is my app doing that" question — buttons that '
        'seem dead, values that vanish, apps that feel slow — comes back to this one sentence.</div>',
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------------------------
elif current == "Toolkit":
    st.title("Ten functions")
    st.markdown('<p class="lede">Enough for most apps. Everything else, you look up.</p>',
                unsafe_allow_html=True)

    group = st.segmented_control("Group", ["Show", "Ask", "Chart", "Arrange"], default="Show",
                                 key="tk", label_visibility="collapsed")

    if group == "Show":
        demo(
            """
            st.title("Title")
            st.write("st.write takes almost anything — text, numbers, DataFrames.")
            st.metric("Seats free", 128, "+14")
            st.dataframe(study_spots(4)[["spot", "seats", "rating"]], hide_index=True)
            """
        )
    elif group == "Ask":
        demo(
            """
            city = st.selectbox("Building", ["Leavey", "Doheny", "SGM"], key="t_sel")
            seats = st.slider("Minimum seats", 0, 100, 20, key="t_slider")
            quiet = st.checkbox("Silent only", key="t_check")
            st.write(f"Looking for {seats}+ seats in {city}." + (" Silent." if quiet else ""))
            """
        )
    elif group == "Chart":
        demo(
            """
            df = study_spots()
            st.bar_chart(df.groupby("building")["seats"].sum())
            st.map(df, size=15)
            """
        )
    else:
        demo(
            """
            a, b = st.columns(2)
            a.metric("Spots", 90)
            b.metric("Avg rating", 3.9)

            with st.sidebar:
                st.write("Controls go here")

            with st.expander("Details"):
                st.write("Hidden until clicked.")
            """
        )

    st.markdown(
        '<div class="note">That is the whole toolkit for today: '
        '<code>title · write · metric · dataframe · selectbox · slider · checkbox · '
        'bar_chart · map · columns</code></div>',
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------------------------
elif current == "Build":
    st.title("Build it")
    st.markdown(
        '<p class="lede">One app, six steps. Add a few lines, save, watch the browser.</p>',
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns([3, 2])
    with c1:
        st.write("**USC Study Spot Finder** — filter 90 campus study spots by building, "
                 "rating and noise.")
    with c2:
        st.download_button("⬇ Starter kit", starter_zip(), "study-spots-starter.zip",
                           "application/zip", width="stretch")
    st.caption("Unzip it into your project folder: the data, a 6-line app.py, requirements.txt.")

    st.divider()
    step = st.segmented_control(
        "Step", ["1", "2", "3", "4", "5", "6"], default="1", key="build",
        label_visibility="collapsed",
    ) or "1"

    BUILD = {
        "1": (
            "See the data",
            "Replace app.py with this, then run it.",
            '''
            import streamlit as st
            import pandas as pd

            st.title("USC Study Spot Finder")

            df = pd.read_csv("study_spots.csv")
            st.dataframe(df)
            ''',
            "A sortable table of 90 spots.",
        ),
        "2": (
            "Let people filter",
            "Add this below the read_csv line, and change the last line to show `hits`.",
            '''
            buildings = st.multiselect("Building", sorted(df["building"].unique()),
                                       default=sorted(df["building"].unique()))
            min_rating = st.slider("Minimum rating", 1.0, 5.0, 3.5, 0.1)
            quiet = st.checkbox("Silent spots only")

            hits = df[df["building"].isin(buildings) & (df["rating"] >= min_rating)]
            if quiet:
                hits = hits[hits["noise"] == "Silent"]

            st.dataframe(hits)
            ''',
            "Moving the slider shrinks the table. This is the whole rerun idea, working.",
        ),
        "3": (
            "Answer the question up front",
            "Add above the table. Nobody reads a table to get a total.",
            '''
            a, b, c = st.columns(3)
            a.metric("Spots", len(hits))
            b.metric("Seats", int(hits["seats"].sum()))
            c.metric("Avg rating", round(hits["rating"].mean(), 2) if len(hits) else 0)
            ''',
            "Three numbers that update as you filter.",
        ),
        "4": (
            "Add a chart",
            "One line of pandas, one line of Streamlit.",
            '''
            st.subheader("Seats by building")
            st.bar_chart(hits.groupby("building")["seats"].sum())
            ''',
            "A bar chart that responds to your filters.",
        ),
        "5": (
            "Put it on a map",
            "The columns are already named lat and lon, so this just works.",
            '''
            st.subheader("Where they are")
            st.map(hits, size=15)
            ''',
            "Pins clustered around campus.",
        ),
        "6": (
            "Make it feel finished",
            "Cache the load, move controls to the sidebar, handle the empty case.",
            '''
            @st.cache_data
            def load():
                return pd.read_csv("study_spots.csv")

            df = load()

            with st.sidebar:
                st.header("Filters")
                # move your multiselect / slider / checkbox in here

            if hits.empty:
                st.warning("No spots match. Try loosening a filter.")
                st.stop()
            ''',
            "Controls on the left, results on the right, no red error when filters match nothing.",
        ),
    }

    title, how, code, expect = BUILD[step]
    st.markdown(f'<p class="stepno">Step {step} of 6</p>', unsafe_allow_html=True)
    st.markdown(f"### {title}")
    st.write(how)
    st.code(textwrap.dedent(code).strip(), language="python")
    st.markdown(f'<p class="check">You should see → {expect}</p>', unsafe_allow_html=True)

    if step == "6":
        st.success("That's the app. Take it to **Ship** and put it online.", icon="✅")

    st.divider()
    st.markdown("## Then make it yours")
    st.write("This is the assignment. Same six steps, your own subject.")
    st.markdown(
        """
        1. Bring a CSV you care about — your project data, a Kaggle set, anything.
        2. At least **two filters**, **one metric row**, **one chart**.
        3. Handle the empty case, so a bad filter shows a message instead of a traceback.
        4. **Deploy it** and submit the URL.
        """
    )
    st.caption("Scope it to one screen. If it takes more than an evening, it's too big.")

# ---------------------------------------------------------------------------
elif current == "Ship":
    st.title("Ship")
    st.markdown('<p class="lede">GitHub, then one form. Free, and it stays up.</p>',
                unsafe_allow_html=True)

    st.markdown('<p class="stepno">01 · list what you import</p>', unsafe_allow_html=True)
    st.write("A file named `requirements.txt`, one package per line. No `os`, `json`, or other built-ins.")
    st.code("streamlit\npandas", language="text")

    st.markdown('<p class="stepno">02 · push to github</p>', unsafe_allow_html=True)
    st.code(
        "git init\n"
        "git add .\n"
        'git commit -m "Study spot finder"\n'
        "git branch -M main\n"
        "git remote add origin https://github.com/YOU/study-spots.git\n"
        "git push -u origin main",
        language="bash",
    )
    st.caption("Public repo for the free tier. Your CSV must be committed too.")

    st.markdown('<p class="stepno">03 · deploy</p>', unsafe_allow_html=True)
    st.markdown(
        """
        Go to **share.streamlit.io**, sign in with GitHub, click **Create app**.  
        Pick your repo, branch `main`, main file `app.py`. Deploy.
        """
    )
    st.write("Two minutes later you have `https://your-app.streamlit.app`. "
             "Every `git push` after this updates it automatically.")

    st.markdown(
        '<div class="note"><b>The two things that break deploys.</b><br>'
        'A package you imported is missing from requirements.txt — the log tells you which one.<br>'
        'A file path from your own machine. Use <code>"study_spots.csv"</code>, never '
        '<code>/Users/you/Desktop/...</code>. The server has no Desktop.</div>',
        unsafe_allow_html=True,
    )

    with st.expander("If your app needs an API key"):
        st.write("Never put it in your code. Locally, `.streamlit/secrets.toml`:")
        st.code('OPENAI_API_KEY = "sk-..."', language="toml")
        st.code('key = st.secrets["OPENAI_API_KEY"]', language="python")
        st.write("Gitignore that file, and paste its contents into **Advanced settings** when you deploy.")

# ---------------------------------------------------------------------------
else:
    st.title("Look it up")
    st.markdown(
        '<p class="lede">This is the actual skill. You will use these more than anything '
        'you memorized today.</p>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        **docs.streamlit.io/develop/api-reference** — every function, with a runnable example.
        Start here; the answer is usually a single function you didn't know existed.

        **discuss.streamlit.io** — paste your error message verbatim. Someone has had it.

        **streamlit.io/gallery** — apps with source. Read one before you design yours.
        """
    )

    st.markdown("## Card")
    st.code(
        """
        st.title / write / metric / caption
        st.dataframe(df)            interactive table
        st.selectbox / slider / checkbox / multiselect
        st.text_input / file_uploader / download_button
        st.bar_chart / line_chart / map
        st.columns(2) / st.tabs([..]) / st.sidebar / st.expander
        st.session_state["k"]       survives reruns
        @st.cache_data              don't reload on every rerun
        st.stop()                   quit the script early
        st.secrets["KEY"]           API keys
        """,
        language="text",
    )

    st.markdown(
        '<div class="note">Search like this: <i>"streamlit how to &lt;the thing&gt;"</i>. '
        'Not <i>"python web app tutorial"</i>. The library is small enough that the '
        'first result is usually right.</div>',
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)
st.caption("2026 USC Summer Scholars — built with Streamlit. Source: https://github.com/yourusername/streamlit_tutorial")