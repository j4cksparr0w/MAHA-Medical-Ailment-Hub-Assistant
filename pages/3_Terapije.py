import streamlit as st
import pandas as pd
from datetime import datetime
from decimal import Decimal

from crud import (
    list_patients, list_doctors, list_medications,
    list_prescriptions, create_prescription,
    update_prescription, delete_prescription
)

st.title("Terapije (Recepti)")

patients = list_patients()
doctors = list_doctors()
meds = list_medications()
pres = list_prescriptions()

patient_map = {p.id: f"{p.last_name} {p.first_name} ({p.oib})" for p in patients}
doctor_map = {d.id: f"{d.last_name} {d.first_name} - {d.specialization}" for d in doctors}
med_map = {m.id: m.name for m in meds}

rows = []
for r in pres:
    rows.append({
        "ID": r.id,
        "Pacijent": patient_map.get(r.patient_id, f"#{r.patient_id}"),
        "Liječnik": doctor_map.get(r.doctor_id, f"#{r.doctor_id}"),
        "Lijek": med_map.get(r.medication_id, f"#{r.medication_id}"),
        "Stanje": r.condition,
        "Doza": f"{r.dosage_amount} {r.dosage_unit}",
        "Učestalost": r.frequency,
        "Od": str(r.start_date),
        "Do": str(r.end_date) if r.end_date else ""
    })

df = pd.DataFrame(rows)
st.dataframe(df, width="stretch")

st.divider()
st.subheader("Dodaj terapiju")

if not patients:
    st.warning("Nema pacijenata. Prvo dodaj pacijenta.")
elif not doctors:
    st.warning("Nema liječnika (seed).")
elif not meds:
    st.warning("Nema lijekova. Prvo dodaj lijek.")
else:
    with st.form("add_rx", clear_on_submit=True):
        p_choice = st.selectbox("Pacijent*", options=patients, format_func=lambda p: patient_map[p.id])
        d_choice = st.selectbox("Liječnik*", options=doctors, format_func=lambda d: doctor_map[d.id])
        m_choice = st.selectbox("Lijek*", options=meds, format_func=lambda m: m.name)

        condition = st.text_input("Za koje stanje* (npr. hipertenzija)")
        dosage_amount = st.number_input("Količina doze*", min_value=0.0, value=1.0, step=0.5)
        dosage_unit = st.text_input("Jedinica* (npr. mg, tableta)")
        frequency = st.text_input("Učestalost* (npr. 3x dnevno)")

        start_date = st.date_input("Početak*")
        has_end = st.checkbox("Ima završetak terapije?")
        end_date = st.date_input("Završetak", value=start_date) if has_end else None

        ok = st.form_submit_button("Spremi")

    if ok:
        create_prescription({
            "patient_id": p_choice.id,
            "doctor_id": d_choice.id,
            "medication_id": m_choice.id,
            "condition": condition,
            "dosage_amount": Decimal(str(dosage_amount)),
            "dosage_unit": dosage_unit,
            "frequency": frequency,
            "start_date": start_date,
            "end_date": end_date
        })
        st.success("Terapija dodana.")
        st.rerun()

st.divider()
st.subheader("Uredi / Obriši terapiju")

if not pres:
    st.info("Nema terapija za uređivanje.")
else:
    options = {f"{r.id} - {patient_map.get(r.patient_id,'?')} | {med_map.get(r.medication_id,'?')} | {r.start_date}": r for r in pres}
    key = st.selectbox("Odaberi terapiju", list(options.keys()))
    selected = options[key]

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Uredi")
        with st.form("edit_rx"):
            e_patient = st.selectbox("Pacijent", options=patients,
                                     index=[p.id for p in patients].index(selected.patient_id),
                                     format_func=lambda p: patient_map[p.id])
            e_doctor = st.selectbox("Liječnik", options=doctors,
                                    index=[d.id for d in doctors].index(selected.doctor_id),
                                    format_func=lambda d: doctor_map[d.id])
            e_med = st.selectbox("Lijek", options=meds,
                                 index=[m.id for m in meds].index(selected.medication_id),
                                 format_func=lambda m: m.name)

            e_condition = st.text_input("Stanje", value=selected.condition)
            e_dose = st.number_input("Količina doze", min_value=0.0,
                                     value=float(selected.dosage_amount), step=0.5)
            e_unit = st.text_input("Jedinica", value=selected.dosage_unit)
            e_freq = st.text_input("Učestalost", value=selected.frequency)

            e_start = st.date_input("Početak", value=selected.start_date)
            e_has_end = st.checkbox("Ima završetak?", value=selected.end_date is not None)
            e_end = st.date_input("Završetak", value=selected.end_date or selected.start_date) if e_has_end else None

            save = st.form_submit_button("Spremi promjene")

        if save:
            update_prescription(selected.id, {
                "patient_id": e_patient.id,
                "doctor_id": e_doctor.id,
                "medication_id": e_med.id,
                "condition": e_condition,
                "dosage_amount": Decimal(str(e_dose)),
                "dosage_unit": e_unit,
                "frequency": e_freq,
                "start_date": e_start,
                "end_date": e_end
            })
            st.success("Spremljeno.")
            st.rerun()

    with col2:
        st.markdown("### Obriši")
        st.warning("Brisanje je trajno.")
        if st.button("Obriši odabranu terapiju"):
            if delete_prescription(selected.id):
                st.success("Obrisano.")
                st.rerun()
            else:
                st.error("Terapija nije pronađena.")
