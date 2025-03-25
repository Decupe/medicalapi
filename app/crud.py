from sqlalchemy.orm import Session
from . import models, schemas
from datetime import date
from typing import Optional

def get_patient(db: Session, patient_id: int):
    return db.query(models.Patient).filter(models.Patient.id == patient_id).first()

def create_patient(db: Session, patient: schemas.PatientCreate):
    db_patient = models.Patient(**patient.dict())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

def get_clinician(db: Session, clinician_id: int):
    return db.query(models.Clinician).filter(models.Clinician.id == clinician_id).first()

def create_clinician(db: Session, clinician: schemas.ClinicianCreate):
    db_clinician = models.Clinician(**clinician.dict())
    db.add(db_clinician)
    db.commit()
    db.refresh(db_clinician)
    return db_clinician

def get_medication(db: Session, medication_id: int):
    return db.query(models.Medication).filter(models.Medication.id == medication_id).first()

def create_medication(db: Session, medication: schemas.MedicationCreate):
    db_medication = models.Medication(**medication.dict())
    db.add(db_medication)
    db.commit()
    db.refresh(db_medication)
    return db_medication

def get_medication_request(db: Session, request_id: int):
    return db.query(models.MedicationRequest).filter(models.MedicationRequest.id == request_id).first()

def get_medication_requests(
    db: Session, 
    status: Optional[schemas.Status] = None, 
    start_date: Optional[date] = None, 
    end_date: Optional[date] = None,
    skip: int = 0, 
    limit: int = 100
):
    query = db.query(
        models.MedicationRequest,
        models.Medication.code_name,
        models.Clinician.first_name,
        models.Clinician.last_name
    ).join(
        models.Medication, 
        models.MedicationRequest.medication_id == models.Medication.id
    ).join(
        models.Clinician,
        models.MedicationRequest.clinician_id == models.Clinician.id
    )
    
    if status:
        query = query.filter(models.MedicationRequest.status == status)
    if start_date:
        query = query.filter(models.MedicationRequest.prescribed_date >= start_date)
    if end_date:
        query = query.filter(models.MedicationRequest.prescribed_date <= end_date)
    
    return query.offset(skip).limit(limit).all()

def create_medication_request(db: Session, medication_request: schemas.MedicationRequestCreate):
    db_medication_request = models.MedicationRequest(**medication_request.dict())
    db.add(db_medication_request)
    db.commit()
    db.refresh(db_medication_request)
    return db_medication_request

def update_medication_request(
    db: Session, 
    request_id: int, 
    medication_request: schemas.MedicationRequestUpdate
):
    db_request = get_medication_request(db, request_id)
    if not db_request:
        return None
    
    update_data = medication_request.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_request, key, value)
    
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request