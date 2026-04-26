import streamlit as st
import pandas as pd
from sqlalchemy.exc import IntegrityError

from crud import list_medications, create_medication, update_medication, delete_medication

st.title("Lijekovi")

search = st.text_input("Pretraga po nazivu lijeka")

meds = list_medications(search)

df = pd.DataFrame([{
    "ID": m.id,
    "Naziv": m.name,
    "Opis": m.description or ""
} for m in meds])

st.dataframe(df, width="stretch")

st.divider()
st.subheader("Dodaj lijek")

with st.form("add_med", clear_on_submit=True):
    name = st.text_input("Naziv*")
    desc = st.text_area("Opis", height=80)
    ok = st.form_submit_button("Spremi")

if ok:
    try:
        create_medication({"name": name, "description": desc})
        st.success("Lijek dodan.")
        st.rerun()
    except IntegrityError:
        st.error("Greška: naziv lijeka mora biti jedinstven (ili je prazno polje).")

st.divider()
st.subheader("Uredi / Obriši lijek")

if not meds:
    st.info("Nema lijekova za uređivanje.")
else:
    options = {f"{m.id} - {m.name}": m for m in meds}
    key = st.selectbox("Odaberi lijek", list(options.keys()))
    selected = options[key]

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Uredi")
        with st.form("edit_med"):
            e_name = st.text_input("Naziv", value=selected.name)
            e_desc = st.text_area("Opis", value=selected.description or "", height=80)
            save = st.form_submit_button("Spremi promjene")

        if save:
            try:
                update_medication(selected.id, {"name": e_name, "description": e_desc})
                st.success("Spremljeno.")
                st.rerun()
            except IntegrityError:
                st.error("Greška: naziv lijeka mora biti jedinstven.")

    with col2:
        st.markdown("### Obriši")
        st.warning("Ako je lijek korišten u terapijama, brisanje može failati zbog FK veza.")
        if st.button("Obriši odabrani lijek"):
            if delete_medication(selected.id):
                st.success("Obrisano.")
                st.rerun()
            else:
                st.error("Lijek nije pronađen.")
