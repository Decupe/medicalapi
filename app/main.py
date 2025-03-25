from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date
from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/patients/", response_model=schemas.Patient)
def create_patient(patient: schemas.PatientCreate, db: Session = Depends(get_db)):
    return crud.create_patient(db=db, patient=patient)

@app.post("/clinicians/", response_model=schemas.Clinician)
def create_clinician(clinician: schemas.ClinicianCreate, db: Session = Depends(get_db)):
    return crud.create_clinician(db=db, clinician=clinician)

@app.post("/medications/", response_model=schemas.Medication)
def create_medication(medication: schemas.MedicationCreate, db: Session = Depends(get_db)):
    return crud.create_medication(db=db, medication=medication)

@app.post("/medication-requests/", response_model=schemas.MedicationRequest)
def create_medication_request(
    medication_request: schemas.MedicationRequestCreate, 
    db: Session = Depends(get_db)
):
    # Validate referenced entities exist
    if not crud.get_patient(db, medication_request.patient_id):
        raise HTTPException(status_code=404, detail="Patient not found")
    if not crud.get_clinician(db, medication_request.clinician_id):
        raise HTTPException(status_code=404, detail="Clinician not found")
    if not crud.get_medication(db, medication_request.medication_id):
        raise HTTPException(status_code=404, detail="Medication not found")
    
    return crud.create_medication_request(db=db, medication_request=medication_request)

@app.get("/medication-requests/", response_model=list[schemas.MedicationRequestWithDetails])
def read_medication_requests(
    status: Optional[schemas.Status] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    requests = crud.get_medication_requests(
        db, 
        status=status, 
        start_date=start_date, 
        end_date=end_date,
        skip=skip, 
        limit=limit
    )
    
    return [
        schemas.MedicationRequestWithDetails(
            id=req.MedicationRequest.id,
            reason_text=req.MedicationRequest.reason_text,
            prescribed_date=req.MedicationRequest.prescribed_date,
            start_date=req.MedicationRequest.start_date,
            end_date=req.MedicationRequest.end_date,
            frequency=req.MedicationRequest.frequency,
            status=req.MedicationRequest.status,
            medication_code_name=req.code_name,
            clinician_first_name=req.first_name,
            clinician_last_name=req.last_name
        ) for req in requests
    ]

@app.patch("/medication-requests/{request_id}", response_model=schemas.MedicationRequest)
def update_medication_request(
    request_id: int,
    medication_request: schemas.MedicationRequestUpdate,
    db: Session = Depends(get_db)
):
    db_request = crud.update_medication_request(db, request_id=request_id, medication_request=medication_request)
    if db_request is None:
        raise HTTPException(status_code=404, detail="Medication request not found")
    return db_request