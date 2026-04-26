from sqlalchemy import select
from db import SessionLocal
from models import Doctor

DEFAULT_DOCTORS = [
    ("Ana", "Anić", "Obiteljska medicina"),
    ("Marko", "Marić", "Radiologija"),
    ("Ivana", "Ivić", "Kardiologija"),
]

def seed_doctors_once():
    with SessionLocal() as db:
        exists = db.execute(select(Doctor.id).limit(1)).first()
        if exists:
            return
        for fn, ln, sp in DEFAULT_DOCTORS:
            db.add(Doctor(first_name=fn, last_name=ln, specialization=sp))
        db.commit()
