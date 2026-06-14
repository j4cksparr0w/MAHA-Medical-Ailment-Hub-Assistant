# MAHA - Medical Ailment Hub Assistant

MAHA is a Streamlit medical data management application built with Python, PostgreSQL, SQLAlchemy ORM and Alembic. It was created as a student/portfolio project for managing patients, medications, therapies, disease history records and specialist appointments through a simple multi-page interface.

> This project is intended for educational and portfolio purposes only. It should not be used with real patient data or as a production medical system.

## Features

- Patient CRUD with search by first name, last name or OIB
- Medication CRUD with unique medication names
- Therapy records connected to patients, doctors and medications
- Disease history records with diagnosis, dates, optional doctor and notes
- Specialist appointment scheduling with referring and specialist doctors
- PostgreSQL database access through SQLAlchemy ORM
- Alembic migrations for database schema versioning
- Docker Compose setup for local PostgreSQL development
- Streamlit multi-page UI
- Eager vs lazy loading demo for ORM query behavior
- Basic seed data for default doctors

## Tech stack

- Python
- Streamlit
- PostgreSQL
- SQLAlchemy
- Alembic
- Pandas
- Docker Compose
- python-dotenv
- psycopg2-binary

## Project structure

```text
MAHA-Medical-Ailment-Hub-Assistant/
├── alembic/
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
├── pages/
│   ├── 1_Pacijenti.py
│   ├── 2_Lijekovi.py
│   ├── 3_Terapije.py
│   ├── 4_Povijest_bolesti.py
│   ├── 5_Pregledi.py
│   └── 6_Eager_Lazy.py
├── app.py
├── crud.py
├── db.py
├── models.py
├── query_counter.py
├── seed.py
├── docker-compose.yml
├── alembic.ini
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Requirements

- Python 3.11 or newer
- Docker Desktop
- Git

## Environment variables

The application reads database settings from a local `.env` file. The real `.env` file must not be committed.

Create it from the example file:

```bash
cp .env.example .env
```

For local Docker PostgreSQL, use:

```env
DB_TARGET=local
DATABASE_URL_LOCAL=postgresql+psycopg2://meduser:medpass@localhost:5432/meddb
DATABASE_URL_SUPABASE=
```

## Local setup

### 1. Clone the repository

```bash
git clone https://github.com/j4cksparr0w/MAHA-Medical-Ailment-Hub-Assistant.git
cd MAHA-Medical-Ailment-Hub-Assistant
```

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start PostgreSQL

```bash
docker compose up -d
```

Local database settings from `docker-compose.yml`:

```text
Database: meddb
User: meduser
Password: medpass
Port: 5432
```

### 5. Run migrations

```bash
alembic upgrade head
```

### 6. Run the app

```bash
streamlit run app.py
```

The app opens at:

```text
http://localhost:8501
```

## Database model overview

Main entities:

- `Doctor`
- `Patient`
- `Medication`
- `Prescription`
- `DiseaseEpisode`
- `SpecialistAppointment`

Relationships are handled with SQLAlchemy foreign keys and ORM relationships.

## Alembic migrations

Apply existing migrations:

```bash
alembic upgrade head
```

Create a new migration after model changes:

```bash
alembic revision --autogenerate -m "describe change"
```

Apply the new migration:

```bash
alembic upgrade head
```

## Security note

This repository must not contain real environment files, production database credentials, real patient information or private medical data.

Before committing, make sure these are not tracked:

```text
.env
.venv/
__pycache__/
*.pyc
```

Use `.env.example` for safe placeholder configuration.

## Author

Created by **j4cksparr0w**.
