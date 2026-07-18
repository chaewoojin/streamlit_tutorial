import streamlit as st
import pandas as pd

st.title("USC Study Spot Finder")

df = pd.read_csv("study_spots.csv")
st.dataframe(df)
