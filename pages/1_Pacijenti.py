import streamlit as st
import pandas as pd
from sqlalchemy.exc import IntegrityError

from crud import list_patients, create_patient, update_patient, delete_patient

st.title("Pacijenti")

search = st.text_input("Pretraga (ime/prezime/OIB)")

patients = list_patients(search)
df = pd.DataFrame([{
    "ID": p.id,
    "Ime": p.first_name,
    "Prezime": p.last_name,
    "OIB": p.oib,
    "Datum rođenja": str(p.birth_date),
    "Spol": p.gender,
    "Boravište": p.residence_address,
    "Prebivalište": p.domicile_address,
} for p in patients])

st.dataframe(df, width="stretch")


st.divider()
st.subheader("Dodaj pacijenta")

with st.form("add_patient", clear_on_submit=True):
    fn = st.text_input("Ime*")
    ln = st.text_input("Prezime*")
    oib = st.text_input("OIB (11 znamenki)*")
    bd = st.date_input("Datum rođenja*")
    gender = st.selectbox("Spol*", ["M", "Ž", "Other"])
    res = st.text_input("Adresa boravišta*")
    dom = st.text_input("Adresa prebivališta*")
    ok = st.form_submit_button("Spremi")

if ok:
    try:
        create_patient({
            "first_name": fn,
            "last_name": ln,
            "oib": oib,
            "birth_date": bd,
            "gender": gender,
            "residence_address": res,
            "domicile_address": dom,
        })
        st.success("Pacijent dodan.")
        st.rerun()
    except IntegrityError:
        st.error("Greška: OIB mora biti jedinstven (ili nedostaju obavezna polja).")

st.divider()
st.subheader("Uredi / Obriši pacijenta")

if len(patients) == 0:
    st.info("Nema pacijenata za uređivanje.")
else:
    options = {f"{p.id} - {p.last_name} {p.first_name} ({p.oib})": p for p in patients}
    key = st.selectbox("Odaberi pacijenta", list(options.keys()))
    selected = options[key]

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Uredi")
        with st.form("edit_patient"):
            e_fn = st.text_input("Ime", value=selected.first_name)
            e_ln = st.text_input("Prezime", value=selected.last_name)
            e_oib = st.text_input("OIB", value=selected.oib)
            e_bd = st.date_input("Datum rođenja", value=selected.birth_date)
            e_gender = st.selectbox("Spol", ["M", "Ž", "Other"], index=["M","Ž","Other"].index(selected.gender))
            e_res = st.text_input("Adresa boravišta", value=selected.residence_address)
            e_dom = st.text_input("Adresa prebivališta", value=selected.domicile_address)
            save = st.form_submit_button("Spremi promjene")

        if save:
            try:
                update_patient(selected.id, {
                    "first_name": e_fn,
                    "last_name": e_ln,
                    "oib": e_oib,
                    "birth_date": e_bd,
                    "gender": e_gender,
                    "residence_address": e_res,
                    "domicile_address": e_dom,
                })
                st.success("Spremljeno.")
                st.rerun()
            except IntegrityError:
                st.error("Greška: OIB mora biti jedinstven.")

    with col2:
        st.markdown("### Obriši")
        st.warning("Brisanje je trajno.")
        if st.button("Obriši odabranog pacijenta"):
            if delete_patient(selected.id):
                st.success("Obrisano.")
                st.rerun()
            else:
                st.error("Pacijent nije pronađen.")
