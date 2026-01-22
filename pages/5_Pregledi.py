import streamlit as st
import pandas as pd
from datetime import datetime

from crud import (
    list_patients, list_doctors,
    list_appointments, create_appointment,
    update_appointment, delete_appointment
)

EXAM_TYPES = ["CT", "MR", "ULTRA", "EKG", "ECHO", "OKO", "DERM", "DENTA", "MAMMO", "EEG"]

st.title("Specijalistički pregledi")

patients = list_patients()
doctors = list_doctors()
apps = list_appointments()

patient_map = {p.id: f"{p.last_name} {p.first_name} ({p.oib})" for p in patients}
doctor_map = {d.id: f"{d.last_name} {d.first_name} - {d.specialization}" for d in doctors}

rows = []
for a in apps:
    rows.append({
        "ID": a.id,
        "Pacijent": patient_map.get(a.patient_id, f"#{a.patient_id}"),
        "Tip": a.exam_type,
        "Termin": a.scheduled_at.strftime("%Y-%m-%d %H:%M"),
        "Uputio": doctor_map.get(a.referring_doctor_id, f"#{a.referring_doctor_id}"),
        "Specijalist": doctor_map.get(a.specialist_doctor_id, f"#{a.specialist_doctor_id}"),
    })

df = pd.DataFrame(rows)
st.dataframe(df, width="stretch")


st.divider()

st.subheader("Zakaži novi pregled")

if not patients:
    st.warning("Nema pacijenata. Prvo dodaj pacijenta u 'Pacijenti'.")
elif not doctors:
    st.warning("Nema liječnika (seed). Provjeri da se seed izvršio.")
else:
    with st.form("add_appointment", clear_on_submit=True):
        p_choice = st.selectbox("Pacijent*", options=patients,
                               format_func=lambda p: patient_map[p.id])

        ref_doc = st.selectbox("Liječnik koji upućuje*", options=doctors,
                               format_func=lambda d: doctor_map[d.id])

        spec_doc = st.selectbox("Specijalist*", options=doctors,
                                format_func=lambda d: doctor_map[d.id])

        exam_type = st.selectbox("Tip pregleda*", EXAM_TYPES)

        d = st.date_input("Datum*", value=datetime.today().date())
        t = st.time_input("Vrijeme*", value=datetime.now().time().replace(second=0, microsecond=0))

        ok = st.form_submit_button("Spremi")

    if ok:
        scheduled_at = datetime.combine(d, t)
        create_appointment({
            "patient_id": p_choice.id,
            "referring_doctor_id": ref_doc.id,
            "specialist_doctor_id": spec_doc.id,
            "exam_type": exam_type,
            "scheduled_at": scheduled_at
        })
        st.success("Pregled zakazan.")
        st.rerun()

st.divider()

st.subheader("Uredi / Obriši pregled")

if not apps:
    st.info("Nema pregleda za uređivanje.")
else:
    options = {f"{a.id} - {patient_map.get(a.patient_id,'?')} | {a.exam_type} | {a.scheduled_at:%Y-%m-%d %H:%M}": a for a in apps}
    key = st.selectbox("Odaberi pregled", list(options.keys()))
    selected = options[key]

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Uredi")
        with st.form("edit_appointment"):
            e_exam = st.selectbox("Tip pregleda", EXAM_TYPES, index=EXAM_TYPES.index(selected.exam_type))
            e_d = st.date_input("Datum", value=selected.scheduled_at.date())
            e_t = st.time_input("Vrijeme", value=selected.scheduled_at.time().replace(second=0, microsecond=0))

            e_ref = st.selectbox("Uputio", options=doctors,
                                 index=[d.id for d in doctors].index(selected.referring_doctor_id),
                                 format_func=lambda d: doctor_map[d.id])

            e_spec = st.selectbox("Specijalist", options=doctors,
                                  index=[d.id for d in doctors].index(selected.specialist_doctor_id),
                                  format_func=lambda d: doctor_map[d.id])

            save = st.form_submit_button("Spremi promjene")

        if save:
            update_appointment(selected.id, {
                "exam_type": e_exam,
                "scheduled_at": datetime.combine(e_d, e_t),
                "referring_doctor_id": e_ref.id,
                "specialist_doctor_id": e_spec.id,
            })
            st.success("Spremljeno.")
            st.rerun()

    with col2:
        st.markdown("### Obriši")
        st.warning("Brisanje je trajno.")
        if st.button("Obriši odabrani pregled"):
            if delete_appointment(selected.id):
                st.success("Obrisano.")
                st.rerun()
            else:
                st.error("Pregled nije pronađen.")
