from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from db import SessionLocal
from models import Patient, Doctor, SpecialistAppointment, Medication, Prescription, DiseaseEpisode

def list_patients(search: str | None = None):
    with SessionLocal() as db:
        stmt = select(Patient)
        if search:
            s = f"%{search.strip()}%"
            stmt = stmt.where(
                (Patient.first_name.ilike(s)) |
                (Patient.last_name.ilike(s)) |
                (Patient.oib.ilike(s))
            )
        stmt = stmt.order_by(Patient.last_name, Patient.first_name)
        return db.execute(stmt).scalars().all()

def create_patient(data: dict):
    with SessionLocal() as db:
        p = Patient(**data)
        db.add(p)
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            raise
        db.refresh(p)
        return p

def update_patient(patient_id: int, data: dict):
    with SessionLocal() as db:
        p = db.get(Patient, patient_id)
        if not p:
            return None
        for k, v in data.items():
            setattr(p, k, v)
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            raise
        db.refresh(p)
        return p

def delete_patient(patient_id: int) -> bool:
    with SessionLocal() as db:
        p = db.get(Patient, patient_id)
        if not p:
            return False
        db.delete(p)
        db.commit()
        return True
    

def list_doctors():
    with SessionLocal() as db:
        stmt = select(Doctor).order_by(Doctor.last_name, Doctor.first_name)
        return db.execute(stmt).scalars().all()

def list_appointments():
    with SessionLocal() as db:
        stmt = select(SpecialistAppointment).order_by(SpecialistAppointment.scheduled_at.desc())
        return db.execute(stmt).scalars().all()

def create_appointment(data: dict):
    with SessionLocal() as db:
        a = SpecialistAppointment(**data)
        db.add(a)
        db.commit()
        db.refresh(a)
        return a

def update_appointment(appointment_id: int, data: dict):
    with SessionLocal() as db:
        a = db.get(SpecialistAppointment, appointment_id)
        if not a:
            return None
        for k, v in data.items():
            setattr(a, k, v)
        db.commit()
        db.refresh(a)
        return a

def delete_appointment(appointment_id: int) -> bool:
    with SessionLocal() as db:
        a = db.get(SpecialistAppointment, appointment_id)
        if not a:
            return False
        db.delete(a)
        db.commit()
        return True

def list_medications(search: str | None = None):
    with SessionLocal() as db:
        stmt = select(Medication)
        if search:
            s = f"%{search.strip()}%"
            stmt = stmt.where(Medication.name.ilike(s))
        stmt = stmt.order_by(Medication.name)
        return db.execute(stmt).scalars().all()

def create_medication(data: dict):
    with SessionLocal() as db:
        m = Medication(**data)
        db.add(m)
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            raise
        db.refresh(m)
        return m

def update_medication(medication_id: int, data: dict):
    with SessionLocal() as db:
        m = db.get(Medication, medication_id)
        if not m:
            return None
        for k, v in data.items():
            setattr(m, k, v)
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            raise
        db.refresh(m)
        return m

def delete_medication(medication_id: int) -> bool:
    with SessionLocal() as db:
        m = db.get(Medication, medication_id)
        if not m:
            return False
        db.delete(m)
        db.commit()
        return True


def list_prescriptions():
    with SessionLocal() as db:
        stmt = select(Prescription).order_by(Prescription.start_date.desc(), Prescription.id.desc())
        return db.execute(stmt).scalars().all()

def create_prescription(data: dict):
    with SessionLocal() as db:
        p = Prescription(**data)
        db.add(p)
        db.commit()
        db.refresh(p)
        return p

def update_prescription(prescription_id: int, data: dict):
    with SessionLocal() as db:
        p = db.get(Prescription, prescription_id)
        if not p:
            return None
        for k, v in data.items():
            setattr(p, k, v)
        db.commit()
        db.refresh(p)
        return p

def delete_prescription(prescription_id: int) -> bool:
    with SessionLocal() as db:
        p = db.get(Prescription, prescription_id)
        if not p:
            return False
        db.delete(p)
        db.commit()
        return True
 
def list_disease_episodes(patient_id: int | None = None):
    with SessionLocal() as db:
        stmt = select(DiseaseEpisode).order_by(DiseaseEpisode.start_date.desc(), DiseaseEpisode.id.desc())
        if patient_id:
            stmt = stmt.where(DiseaseEpisode.patient_id == patient_id)
        return db.execute(stmt).scalars().all()

def create_disease_episode(data: dict):
    with SessionLocal() as db:
        e = DiseaseEpisode(**data)
        db.add(e)
        db.commit()
        db.refresh(e)
        return e

def update_disease_episode(episode_id: int, data: dict):
    with SessionLocal() as db:
        e = db.get(DiseaseEpisode, episode_id)
        if not e:
            return None
        for k, v in data.items():
            setattr(e, k, v)
        db.commit()
        db.refresh(e)
        return e

def delete_disease_episode(episode_id: int) -> bool:
    with SessionLocal() as db:
        e = db.get(DiseaseEpisode, episode_id)
        if not e:
            return False
        db.delete(e)
        db.commit()
        return True


