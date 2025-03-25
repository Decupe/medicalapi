from datetime import date
import pytest
from app import crud, schemas
from app.models import Patient, Clinician, Medication, MedicationRequest
from app.schemas import Sex, Form, Status
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

def test_create_patient(db):
    patient_data = schemas.PatientCreate(
        first_name="John",
        last_name="Doe",
        date_of_birth=date(1990, 1, 1),
        sex=Sex.male
    )
    patient = crud.create_patient(db, patient=patient_data)
    assert patient.first_name == "John"
    assert patient.last_name == "Doe"
    assert patient.date_of_birth == date(1990, 1, 1)
    assert patient.sex == Sex.male
    assert patient.id is not None

def test_get_patient(db):
    # First create a patient
    patient_data = schemas.PatientCreate(
        first_name="Jane",
        last_name="Smith",
        date_of_birth=date(1985, 5, 15),
        sex=Sex.female
    )
    created_patient = crud.create_patient(db, patient=patient_data)
    
    # Now retrieve it
    retrieved_patient = crud.get_patient(db, patient_id=created_patient.id)
    assert retrieved_patient is not None
    assert retrieved_patient.first_name == "Jane"
    assert retrieved_patient.id == created_patient.id

def test_create_clinician(db):
    clinician_data = schemas.ClinicianCreate(
        first_name="Dr. Sarah",
        last_name="Johnson",
        registration_id="MD12345"
    )
    clinician = crud.create_clinician(db, clinician=clinician_data)
    assert clinician.first_name == "Dr. Sarah"
    assert clinician.registration_id == "MD12345"
    assert clinician.id is not None

def test_get_clinician(db):
    clinician_data = schemas.ClinicianCreate(
        first_name="Dr. Michael",
        last_name="Brown",
        registration_id="MD67890"
    )
    created_clinician = crud.create_clinician(db, clinician=clinician_data)
    
    retrieved_clinician = crud.get_clinician(db, clinician_id=created_clinician.id)
    assert retrieved_clinician is not None
    assert retrieved_clinician.last_name == "Brown"
    assert retrieved_clinician.registration_id == "MD67890"

def test_create_medication(db):
    medication_data = schemas.MedicationCreate(
        code="12345",
        code_name="Paracetamol",
        code_system="SNOMED",
        strength_value=500,
        strength_unit="mg",
        form=Form.tablet
    )
    medication = crud.create_medication(db, medication=medication_data)
    assert medication.code_name == "Paracetamol"
    assert medication.strength_value == 500
    assert medication.form == Form.tablet
   