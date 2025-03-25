from sqlalchemy import Column, Integer, String, Date, Float, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

# Define enums using strings directly for SQLAlchemy
sex_enum = Enum('male', 'female', name='sex')
form_enum = Enum('powder', 'tablet', 'capsule', 'syrup', name='form')
status_enum = Enum('active', 'on-hold', 'cancelled', 'completed', name='status')

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    date_of_birth = Column(Date, nullable=False)
    sex = Column(sex_enum, nullable=False)

    medication_requests = relationship("MedicationRequest", back_populates="patient")

class Clinician(Base):
    __tablename__ = "clinicians"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    registration_id = Column(String, unique=True, nullable=False)

    medication_requests = relationship("MedicationRequest", back_populates="clinician")

class Medication(Base):
    __tablename__ = "medications"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, nullable=False)
    code_name = Column(String, nullable=False)
    code_system = Column(String, nullable=False)
    strength_value = Column(Float, nullable=False)
    strength_unit = Column(String, nullable=False)
    form = Column(form_enum, nullable=False)

    medication_requests = relationship("MedicationRequest", back_populates="medication")

class MedicationRequest(Base):
    __tablename__ = "medication_requests"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    clinician_id = Column(Integer, ForeignKey("clinicians.id"), nullable=False)
    medication_id = Column(Integer, ForeignKey("medications.id"), nullable=False)
    reason_text = Column(String, nullable=False)
    prescribed_date = Column(Date, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    frequency = Column(String, nullable=False)
    status = Column(status_enum, nullable=False)

    patient = relationship("Patient", back_populates="medication_requests")
    clinician = relationship("Clinician", back_populates="medication_requests")
    medication = relationship("Medication", back_populates="medication_requests")