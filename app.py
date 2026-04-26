import streamlit as st
from seed import seed_doctors_once

st.set_page_config(page_title="Medicinski sustav", layout="wide")

seed_doctors_once()

st.title("Medicinski sustav")
st.write("Ako vidiš ovo, Streamlit radi i doktori su seedani.")
