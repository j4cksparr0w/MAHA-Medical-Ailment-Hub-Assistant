# MAHA — Medical Ailment Hub Assistant

MAHA is an educational medical management app built with **Streamlit** and **SQLAlchemy (ORM)**, backed by **PostgreSQL** (Docker).
It provides CRUD pages for **patients**, **medications**, **prescriptions/therapies**, **medical history**, and **specialist appointments**, plus a small **Eager vs Lazy loading** demo to illustrate the **N+1 query problem**.

> Note: **Doctors are seeded on app startup** (first run). CRUD is implemented for all other entities.

---

## Table of Contents
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Data Model](#data-model)
- [Getting Started](#getting-started)
- [Configuration](#configuration)
- [Database Migrations (Alembic)](#database-migrations-alembic)
- [Running the App](#running-the-app)
- [Notes](#notes)
- [License](#license)

---

## Features

### Patients
File: `pages/1_Pacijenti.py`
- Create / list / update / delete patients
- Search by first name / last name / OIB (11 digits)
- Fields: first name, last name, OIB (unique), birth date, gender, residence address, domicile address

### Medications
File: `pages/2_Lijekovi.py`
- Create / list / update / delete medications
- Search by medication name
- Medication name is unique

### Prescriptions / Therapies
File: `pages/3_Terapije.py`
- Create / list / update / delete prescriptions
- Links **patient + doctor + medication**
- Fields: condition/indication, dosage (amount + unit), frequency, start date, optional end date

### Medical History (Disease Episodes)
File: `pages/4_Povijest_bolesti.py`
- Create / list / update / delete disease episodes
- Optional doctor link
- Filter by selected patient or show all patients
- Fields: diagnosis, start date, optional end date, optional doctor, notes

### Specialist Appointments
File: `pages/5_Pregledi.py`
- Create / list / update / delete specialist appointments
- Appointment types: `CT`, `MR`, `ULTRA`, `EKG`, `ECHO`, `OKO`, `DERM`, `DENTA`, `MAMMO`, `EEG`
- Fields: patient, referring doctor, specialist doctor, exam type, scheduled date/time

### Eager vs Lazy Demo (N+1 Problem)
File: `pages/6_Eager_Lazy.py`
- Compares:
  - LAZY (default)
  - EAGER (joinedload)
  - EAGER (selectinload)
- Shows total SQL query count and can optionally display SQL statements

---

## Tech Stack
- Python (3.10+)
- Streamlit (UI)
- SQLAlchemy (ORM)
- PostgreSQL (Docker)
- Alembic (migration scripts included)
- python-dotenv (reads `.env`)
- pandas (tables in UI)

---

## Project Structure

