# MAHA - Medical Ailment Hub Assistant

MAHA is a Streamlit-based medical data management application built with Python, PostgreSQL, SQLAlchemy, and Alembic. The application is designed as a portfolio/student project for managing patients, medications, therapies, disease history records, and specialist appointments through a simple multi-page web interface.

> This project is intended for educational and portfolio purposes only. It should not be used with real patient data or as a production medical system.

## Repository description

Python Streamlit medical management app with PostgreSQL, SQLAlchemy ORM, Alembic migrations, patient CRUD, medication tracking, therapy records, disease history, appointments, and eager/lazy loading demo.

## Features

- Patient management with search, create, update, and delete functionality
- Medication management with unique medication names
- Therapy and prescription records connected to patients, doctors, and medications
- Disease history tracking with diagnosis, dates, optional doctor, and notes
- Specialist appointment scheduling with referral and specialist doctor relationships
- PostgreSQL database support through SQLAlchemy ORM
- Alembic database migrations
- Docker Compose setup for local PostgreSQL development
- Streamlit multi-page interface
- Eager vs lazy loading demonstration for ORM query behavior
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
- psycopg2

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

Before running the project, install:

- Python 3.11 or newer
- Docker Desktop
- Git

The project was developed as a local Streamlit application using PostgreSQL as the database backend.

## Environment variables

The application uses environment variables from a `.env` file.

Create your own `.env` file in the root folder by copying `.env.example`:

```bash
cp .env.example .env
```

For local Docker PostgreSQL, use:

```env
DB_TARGET=local
DATABASE_URL_LOCAL=postgresql+psycopg2://meduser:medpass@localhost:5432/meddb
DATABASE_URL_SUPABASE=
```

Do not commit the real `.env` file to GitHub.

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

### 4. Create the `.env` file

```bash
cp .env.example .env
```

On Windows, you can also manually copy `.env.example`, rename the copy to `.env`, and edit it in a text editor.

### 5. Start PostgreSQL with Docker Compose

```bash
docker compose up -d
```

This starts a local PostgreSQL container with:

```text
Database: meddb
User: meduser
Password: medpass
Port: 5432
```

### 6. Run database migrations

```bash
alembic upgrade head
```

### 7. Run the Streamlit app

```bash
streamlit run app.py
```

The application should open in your browser at:

```text
http://localhost:8501
```

## Database model overview

The database contains the following main entities:

- `Doctor` - default doctors seeded when the app starts
- `Patient` - patient personal and address information
- `Medication` - medication catalog
- `Prescription` - therapy records connected to patient, doctor, and medication
- `DiseaseEpisode` - disease history entries
- `SpecialistAppointment` - scheduled specialist appointments

Relationships are handled through SQLAlchemy foreign keys and ORM relationships.

## Alembic migrations

Alembic is used for database schema versioning.

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

## Important security note

This repository should not contain real environment files, production database credentials, real patient information, or private medical data.

Before committing, make sure these files and folders are not included:

```text
.env
.venv/
__pycache__/
*.pyc
```

Use `.env.example` for safe placeholder configuration.

## Author

Created by **j4cksparr0w**.
