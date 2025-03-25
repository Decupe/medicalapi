from datetime import date
from app.models import Patient, Clinician, Medication, MedicationRequest
from app.schemas import Sex, Form, Status

def test_patient_model():
    patient = Patient(
        first_name="John",
        last_name="Doe",
        date_of_birth=date(1990, 1, 1),
        sex=Sex.male
    )
    assert patient.first_name == "John"
    assert patient.sex == Sex.male

def test_medication_request_model(db):
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    
    patient = Patient(
        first_name="John",
        last_name="Doe",
        date_of_birth=date(1990, 1, 1),
        sex="male"
    )

    clinician = Clinician(
        first_name="Jane",
        last_name="Smith",
        registration_id=f"MD{timestamp}"  # Unique ID
    )

    medication = Medication(
        code=f"CODE{timestamp}",  # Also make this unique
        code_name="Paracetamol",
        code_system="SNOMED",
        strength_value=500,
        strength_unit="mg",
        form="tablet"
    )
    
    db.add_all([patient, clinician, medication])
    db.commit()
    
    request = MedicationRequest(
        patient_id=patient.id,
        clinician_id=clinician.id,
        medication_id=medication.id,
        reason_text="Headache",
        prescribed_date=date(2023, 1, 1),
        start_date=date(2023, 1, 1),
        frequency="3 times/day",
        status=Status.active
    )
    
    db.add(request)
    db.commit()
    
    assert request.reason_text == "Headache"
    assert request.status == Status.active
    assert request.patient.first_name == "John"
    assert request.medication.code_name == "Paracetamol"