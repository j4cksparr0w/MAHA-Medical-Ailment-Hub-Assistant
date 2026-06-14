import streamlit as st
import pandas as pd
from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload

from db import SessionLocal
from models import Prescription
from query_counter import count_queries

st.title("Eager vs Lazy demo")

mode = st.radio(
    "Način dohvaćanja povezanih podataka",
    ["LAZY (default)", "EAGER (joinedload)", "EAGER (selectinload)"],
    horizontal=True
)

show_sql = st.checkbox("Prikaži SQL upite ")


with SessionLocal() as db, count_queries(capture_sql=show_sql) as qc:
    stmt = select(Prescription).order_by(Prescription.id.desc())

    if mode == "EAGER (joinedload)":
        stmt = stmt.options(
            joinedload(Prescription.patient),
            joinedload(Prescription.doctor),
            joinedload(Prescription.medication),
        )
    elif mode == "EAGER (selectinload)":
        stmt = stmt.options(
            selectinload(Prescription.patient),
            selectinload(Prescription.doctor),
            selectinload(Prescription.medication),
        )

    prescriptions = db.execute(stmt).scalars().all()


    rows = []
    for p in prescriptions:
        rows.append({
            "ID": p.id,
            "Pacijent": f"{p.patient.last_name} {p.patient.first_name}",
            "Liječnik": f"{p.doctor.last_name} {p.doctor.first_name}",
            "Lijek": p.medication.name,
            "Stanje": p.condition,
            "Doza": f"{p.dosage_amount} {p.dosage_unit}",
            "Učestalost": p.frequency,
        })

st.info(f"Broj SQL upita u ovom renderu: **{qc['n']}**")
st.dataframe(pd.DataFrame(rows), width="stretch")
if show_sql:
    st.code("\n\n---\n\n".join(qc["sql"]), language="sql")