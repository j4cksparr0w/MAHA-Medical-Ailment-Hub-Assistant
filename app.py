import streamlit as st
from seed import seed_doctors_once

st.set_page_config(page_title="MAHA", layout="wide")

seed_doctors_once()

st.title("MAHA – Medical Ailment Hub Assistant")

st.write(
    "Portal za vođenje osnovne medicinske evidencije pacijenata, lijekova, terapija, povijesti bolesti i specijalističkih pregleda."
)

st.divider()

col1, col2, col3 = st.columns(3)

st.info("Sustav je spreman za rad.")