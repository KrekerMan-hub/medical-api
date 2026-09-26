#=============
# Routers
#=============


from fastapi import APIRouter, Query, HTTPException

from schemas import PatientCreate, PatientResponse, DiagnosisUpdate
from database import get_patients, get_patient_by_id, add_patient, update_diagnosis, delete_patient

router = APIRouter(
    prefix="/patients",
    tags=["Пациенты"]
)

@router.get("", response_model=list[PatientResponse])
def show_patients(
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    min_age: int | None = Query(default=None, ge=0, le=120),
    name: str | None = Query(default=None, min_length=0, max_length=100),
):
    return get_patients(
        limit=limit,
        offset=offset,
        min_age=min_age,
        name=name,
    )

@router.post(
    "",
    response_model=PatientResponse,
    status_code=201,
)
def receive_patients(patient: PatientCreate):
    return add_patient(
        name=patient.name,
        age=patient.age,
        diagnosis=patient.diagnosis,
    )

@router.get("/{patient_id}", response_model=PatientResponse)
def show_patient(patient_id: int):
    patient = get_patient_by_id(patient_id)

    if patient is None:
        raise HTTPException(
            status_code=404,
            detail="Пациент не найден",
        )

    return patient


@router.patch("/{patient_id}/diagnosis")
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


@router.delete("/{patient_id}")
def remove_patient(patient_id: int) -> dict[str, str]:
    deleted = delete_patient(patient_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Пациент не найден",
        )

    return {"message": "Пациент удалён"}