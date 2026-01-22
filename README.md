# MAHA — Medical Ailment Hub Assistant

MAHA is an educational medical management application built with **Streamlit** and **SQLAlchemy (ORM)**, backed by **PostgreSQL** (Docker).  
It provides a clean CRUD-based workflow for managing patients and related medical records, and includes a demo page that explains **LAZY vs EAGER loading** (N+1 queries).

## Key Features
- **Patients (CRUD):** first/last name, OIB (unique), date of birth, gender, residence & domicile address
- **Medications (CRUD):** unique name + description
- **Prescriptions/Therapies (CRUD):** patient + doctor + medication, dosage (amount/unit), frequency, start/end dates, condition/indication
- **Medical History (CRUD):** disease episodes (diagnosis, period, notes, optional doctor), patient filtering
- **Specialist Appointments (CRUD):** patient, referring doctor, specialist doctor, exam type, scheduled date/time
- **Eager vs Lazy Demo:** query counting + joinedload/selectinload examples

> Doctors are **seeded on first run**; CRUD is implemented for all other entities.

## Tech Stack
Python, Streamlit, SQLAlchemy, PostgreSQL (Docker), Alembic, python-dotenv, pandas

## Run Locally
```bash
docker compose up -d
cp .env.example .env
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install streamlit sqlalchemy psycopg2-binary python-dotenv alembic pandas
streamlit run app.py
