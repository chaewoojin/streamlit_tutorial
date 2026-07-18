<div align="center">

# Streamlit, taught in Streamlit

**A self-teaching workshop for USC summer scholars.**

The tutorial *is* a Streamlit app — every concept is demonstrated live, next to the code that produced it.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.50+-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)
![USC](https://img.shields.io/badge/USC-Summer_Scholars-990000?style=flat-square)
![Duration](https://img.shields.io/badge/Duration-2_hours-FFC72C?style=flat-square&labelColor=17130F)

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app.streamlit.app)

</div>

---

## Run it

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Opens at `http://localhost:8501`.

## Deploy it

So students can read it before and after class.

1. Push the Streamlit project folder to a **public** GitHub repo.
2. Go to **[share.streamlit.io](https://share.streamlit.io)** → sign in with GitHub → **Create app**.
3. Repo, branch `main`, main file `app.py` → **Deploy**.
4. Share the resulting `*.streamlit.app` URL.

> [!NOTE]
> No secrets or data files needed — the sample data is generated in code.

---

<div align="center">
<br>
<sub>Built with Streamlit · USC Summer Scholars</sub>
</div>