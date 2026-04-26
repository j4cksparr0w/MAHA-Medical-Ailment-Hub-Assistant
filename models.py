from datetime import datetime
from sqlalchemy import String, Integer, Date, DateTime, ForeignKey, Numeric, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db import Base


class Doctor(Base):
    __tablename__ = "doctors"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(80), nullable=False)
    last_name: Mapped[str] = mapped_column(String(80), nullable=False)
    specialization: Mapped[str] = mapped_column(String(120), nullable=False)
    prescriptions = relationship("Prescription", back_populates="doctor")


class Patient(Base):
    __tablename__ = "patients"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(80), nullable=False)
    last_name: Mapped[str] = mapped_column(String(80), nullable=False)
    oib: Mapped[str] = mapped_column(String(11), nullable=False, unique=True)
    birth_date: Mapped[datetime] = mapped_column(Date, nullable=False)
    gender: Mapped[str] = mapped_column(String(10), nullable=False)
    residence_address: Mapped[str] = mapped_column(String(255), nullable=False)
    domicile_address: Mapped[str] = mapped_column(String(255), nullable=False)
    prescriptions = relationship("Prescription", back_populates="patient")


class Medication(Base):
    __tablename__ = "medications"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False, unique=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    prescriptions = relationship("Prescription", back_populates="medication")


class Prescription(Base):
    __tablename__ = "prescriptions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey("patients.id"), nullable=False)
    doctor_id: Mapped[int] = mapped_column(ForeignKey("doctors.id"), nullable=False)
    medication_id: Mapped[int] = mapped_column(ForeignKey("medications.id"), nullable=False)

    condition: Mapped[str] = mapped_column(String(200), nullable=False)
    dosage_amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    dosage_unit: Mapped[str] = mapped_column(String(30), nullable=False)
    frequency: Mapped[str] = mapped_column(String(60), nullable=False)
    start_date: Mapped[datetime] = mapped_column(Date, nullable=False)
    end_date: Mapped[datetime | None] = mapped_column(Date, nullable=True)
    patient = relationship("Patient", back_populates="prescriptions")
    doctor = relationship("Doctor", back_populates="prescriptions")
    medication = relationship("Medication", back_populates="prescriptions")


class DiseaseEpisode(Base):
    __tablename__ = "disease_episodes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey("patients.id"), nullable=False)
    doctor_id: Mapped[int | None] = mapped_column(ForeignKey("doctors.id"), nullable=True)

    diagnosis: Mapped[str] = mapped_column(String(200), nullable=False)
    start_date: Mapped[datetime] = mapped_column(Date, nullable=False)
    end_date: Mapped[datetime | None] = mapped_column(Date, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)


class SpecialistAppointment(Base):
    __tablename__ = "appointments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey("patients.id"), nullable=False)

    referring_doctor_id: Mapped[int] = mapped_column(ForeignKey("doctors.id"), nullable=False)
    specialist_doctor_id: Mapped[int] = mapped_column(ForeignKey("doctors.id"), nullable=False)

    exam_type: Mapped[str] = mapped_column(String(20), nullable=False)  # CT, MR, ...
    scheduled_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
