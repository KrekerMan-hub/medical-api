#==========================
# FastAPI
#==========================

from fastapi import FastAPI, HTTPException, Query
from schemas import PatientCreate, PatientResponse, DiagnosisUpdate
from database import init_db, add_patient, get_patients, get_patient_by_id, update_diagnosis, delete_patient

init_db()

app = FastAPI(title="Medical API", version="1.0")

@app.get("/")
def home() -> dict[str, str]:
    return {"message": "Мой первый API работает!"}

@app.get("/about")
def about():
    return {
        "project": "Medical API",
        "author": "Тарас"
    }

@app.post(
    "/patients",
    response_model=PatientResponse,
    status_code=201,
)
def receive_patients(patient: PatientCreate):
    return add_patient(
        name=patient.name,
        age=patient.age,
        diagnosis=patient.diagnosis,
    )

@app.get("/patients", response_model=list[PatientResponse])
def show_patients(
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0)
):
    return get_patients(limit=limit, offset=offset)

@app.get("/patients/{patient_id}", response_model=PatientResponse)
def show_patient(patient_id: int):
    patient = get_patient_by_id(patient_id)

    if patient is None:
        raise HTTPException(
            status_code=404,
            detail="Пациент не найден",
        )

    return patient


@app.patch("/patients/{patient_id}/diagnosis")
def change_diagnosis(
    patient_id: int,
    data: DiagnosisUpdate,
) -> dict[str, str]:
    updated = update_diagnosis(patient_id, data.diagnosis)

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Пациент не найден",
        )

    return {"message": "Диагноз обновлён"}    

@app.delete("/patients/{patient_id}")
def remove_patient(patient_id: int) -> dict[str, str]:
    deleted = delete_patient(patient_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Пациент не найден",
        )

    return {"message": "Пациент удалён"}