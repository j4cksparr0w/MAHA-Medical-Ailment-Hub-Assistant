# MAHA — Medical Ailment Hub Assistant

Educational medical management app built with **Streamlit** + **SQLAlchemy (ORM)** and **PostgreSQL** (Docker).
Includes CRUD pages for **patients**, **medications**, **prescriptions/therapies**, **medical history**, and **specialist appointments**, plus an **Eager vs Lazy** loading demo (N+1).

> Doctors are seeded on first run; CRUD is implemented for all other entities.

## Run locally
```bash
docker compose up -d
cp .env.example .env
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install streamlit sqlalchemy psycopg2-binary python-dotenv alembic pandas
streamlit run app.py
