from datetime import date
from enum import Enum
from typing import Optional
from pydantic import BaseModel

class Sex(str, Enum):
    male = "male"
    female = "female"

class Form(str, Enum):
    powder = "powder"
    tablet = "tablet"
    capsule = "capsule"
    syrup = "syrup"

class Status(str, Enum):
    active = "active"
    on_hold = "on-hold"
    cancelled = "cancelled"
    completed = "completed"

class PatientBase(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: date
    sex: Sex

class PatientCreate(PatientBase):
    pass

class Patient(PatientBase):
    id: int

    class Config:
        orm_mode = True

class ClinicianBase(BaseModel):
    first_name: str
    last_name: str
    registration_id: str

class ClinicianCreate(ClinicianBase):
    pass

class Clinician(ClinicianBase):
    id: int

    class Config:
        orm_mode = True

class MedicationBase(BaseModel):
    code: str
    code_name: str
    code_system: str
    strength_value: float
    strength_unit: str
    form: Form

class MedicationCreate(MedicationBase):
    pass

class Medication(MedicationBase):
    id: int

    class Config:
        orm_mode = True

class MedicationRequestBase(BaseModel):
    patient_id: int
    clinician_id: int
    medication_id: int
    reason_text: str
    prescribed_date: date
    start_date: date
    end_date: Optional[date] = None
    frequency: str
    status: Status

class MedicationRequestCreate(MedicationRequestBase):
    pass

class MedicationRequestUpdate(BaseModel):
    end_date: Optional[date] = None
    frequency: Optional[str] = None
    status: Optional[Status] = None

class MedicationRequest(MedicationRequestBase):
    id: int

    class Config:
        orm_mode = True

class MedicationRequestWithDetails(BaseModel):
    id: int
    reason_text: str
    prescribed_date: date
    start_date: date
    end_date: Optional[date]
    frequency: str
    status: Status
    medication_code_name: str
    clinician_first_name: str
    clinician_last_name: str

    class Config:
        orm_mode = True