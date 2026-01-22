import streamlit as st
import pandas as pd

from crud import (
    list_patients, list_doctors,
    list_disease_episodes, create_disease_episode,
    update_disease_episode, delete_disease_episode
)

st.title("Povijest bolesti")

patients = list_patients()
doctors = list_doctors()

patient_map = {p.id: f"{p.last_name} {p.first_name} ({p.oib})" for p in patients}
doctor_map = {d.id: f"{d.last_name} {d.first_name} - {d.specialization}" for d in doctors}

st.subheader("Filter")
if not patients:
    st.warning("Nema pacijenata. Prvo dodaj pacijenta.")
    st.stop()

filter_options = ["Svi pacijenti"] + [patient_map[p.id] for p in patients]
chosen = st.selectbox("Prikaži povijest za", filter_options)

patient_id = None
if chosen != "Svi pacijenti":
    patient_id = next(pid for pid, label in patient_map.items() if label == chosen)

episodes = list_disease_episodes(patient_id)

rows = []
for e in episodes:
    rows.append({
        "ID": e.id,
        "Pacijent": patient_map.get(e.patient_id, f"#{e.patient_id}"),
        "Dijagnoza": e.diagnosis,
        "Početak": str(e.start_date),
        "Završetak": str(e.end_date) if e.end_date else "",
        "Liječnik": doctor_map.get(e.doctor_id, "") if e.doctor_id else "",
        "Napomena": e.notes or ""
    })

df = pd.DataFrame(rows)
st.dataframe(df, width="stretch")

st.divider()
st.subheader("Dodaj zapis u povijest bolesti")

with st.form("add_episode", clear_on_submit=True):
    p_choice = st.selectbox("Pacijent*", options=patients, format_func=lambda p: patient_map[p.id])

    doctor_choices = [None] + doctors
    d_choice = st.selectbox(
        "Liječnik (opcionalno)",
        options=doctor_choices,
        format_func=lambda d: "—" if d is None else doctor_map[d.id]
    )

    diagnosis = st.text_input("Dijagnoza*")
    start_date = st.date_input("Datum početka*")
    has_end = st.checkbox("Ima datum završetka?")
    end_date = st.date_input("Datum završetka", value=start_date) if has_end else None
    notes = st.text_area("Napomena", height=90)

    ok = st.form_submit_button("Spremi")

if ok:
    create_disease_episode({
        "patient_id": p_choice.id,
        "doctor_id": d_choice.id if d_choice else None,
        "diagnosis": diagnosis,
        "start_date": start_date,
        "end_date": end_date,
        "notes": notes
    })
    st.success("Zapis dodan.")
    st.rerun()

st.divider()
st.subheader("Uredi / Obriši zapis")

if not episodes:
    st.info("Nema zapisa za uređivanje.")
else:
    options = {
        f"{e.id} - {patient_map.get(e.patient_id,'?')} | {e.diagnosis} | {e.start_date}": e
        for e in episodes
    }
    key = st.selectbox("Odaberi zapis", list(options.keys()))
    selected = options[key]

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Uredi")
        with st.form("edit_episode"):
            e_patient = st.selectbox(
                "Pacijent",
                options=patients,
                index=[p.id for p in patients].index(selected.patient_id),
                format_func=lambda p: patient_map[p.id]
            )

            doctor_choices = [None] + doctors
            if selected.doctor_id is None:
                idx = 0
            else:
                idx = 1 + [d.id for d in doctors].index(selected.doctor_id)

            e_doctor = st.selectbox(
                "Liječnik (opcionalno)",
                options=doctor_choices,
                index=idx,
                format_func=lambda d: "—" if d is None else doctor_map[d.id]
            )

            e_diag = st.text_input("Dijagnoza", value=selected.diagnosis)
            e_start = st.date_input("Početak", value=selected.start_date)
            e_has_end = st.checkbox("Ima završetak?", value=selected.end_date is not None)
            e_end = st.date_input("Završetak", value=selected.end_date or selected.start_date) if e_has_end else None
            e_notes = st.text_area("Napomena", value=selected.notes or "", height=90)

            save = st.form_submit_button("Spremi promjene")

        if save:
            update_disease_episode(selected.id, {
                "patient_id": e_patient.id,
                "doctor_id": e_doctor.id if e_doctor else None,
                "diagnosis": e_diag,
                "start_date": e_start,
                "end_date": e_end,
                "notes": e_notes
            })
            st.success("Spremljeno.")
            st.rerun()

    with col2:
        st.markdown("### Obriši")
        st.warning("Brisanje je trajno.")
        if st.button("Obriši odabrani zapis"):
            if delete_disease_episode(selected.id):
                st.success("Obrisano.")
                st.rerun()
            else:
                st.error("Zapis nije pronađen.")
