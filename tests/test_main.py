from datetime import date
from fastapi import status
import pytest
from app import schemas
import uuid

def test_create_patient(client):
    response = client.post(
        "/patients/",
        json={
            "first_name": "John",
            "last_name": "Doe",
            "date_of_birth": "1990-01-01",
            "sex": "male"
        }
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["first_name"] == "John"
    assert data["last_name"] == "Doe"
    assert data["date_of_birth"] == "1990-01-01"
    assert data["sex"] == "male"

def test_create_medication_request(client, db):
    # Create required entities first
    patient = client.post(
        "/patients/",
        json={
            "first_name": "John",
            "last_name": "Doe",
            "date_of_birth": "1990-01-01",
            "sex": "male"
        }
    ).json()
    
    clinician = client.post(
        "/clinicians/",
        json={
            "first_name": "Jane",
            "last_name": "Smith",
            "registration_id": "MD12345"
        }
    ).json()
    
    medication = client.post(
        "/medications/",
        json={
            "code": "12345",
            "code_name": "Paracetamol",
            "code_system": "SNOMED",
            "strength_value": 500,
            "strength_unit": "mg",
            "form": "tablet"
        }
    ).json()
    
    # Create medication request
    response = client.post(
        "/medication-requests/",
        json={
            "patient_id": patient["id"],
            "clinician_id": clinician["id"],
            "medication_id": medication["id"],
            "reason_text": "Headache",
            "prescribed_date": "2023-01-01",
            "start_date": "2023-01-01",
            "frequency": "3 times/day",
            "status": "active"
        }
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["reason_text"] == "Headache"
    assert data["status"] == "active"

def test_get_medication_requests(client):
    response = client.get("/medication-requests/")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)

def test_update_medication_request(client):
    # First create a request (simplified for test)
    patient = client.post("/patients/", json={
        "first_name": "Test", "last_name": "Patient", "date_of_birth": "2000-01-01", "sex": "female"
    }).json()
    
    clinician = client.post("/clinicians/", json={
        "first_name": "Test", "last_name": "Doctor", "registration_id": "TEST123"
    }).json()
    
    medication = client.post("/medications/", json={
        "code": "TEST", "code_name": "Test Med", "code_system": "TEST", 
        "strength_value": 1, "strength_unit": "mg", "form": "tablet"
    }).json()
    
    request = client.post("/medication-requests/", json={
        "patient_id": patient["id"],
        "clinician_id": clinician["id"],
        "medication_id": medication["id"],
        "reason_text": "Test",
        "prescribed_date": "2023-01-01",
        "start_date": "2023-01-01",
        "frequency": "once",
        "status": "active"
    }).json()
    
    # Update the request
    response = client.patch(
        f"/medication-requests/{request['id']}",
        json={
            "status": "completed",
            "end_date": "2023-01-10"
        }
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "completed"
    assert data["end_date"] == "2023-01-10"