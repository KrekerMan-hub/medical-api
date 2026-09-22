#=============
# DataBase
#=============


import sqlite3
from pathlib import Path

DB_Path = Path(__file__).parent/"medical.db"

class DatabaseConnection:
    def __enter__(self):
        self.connection = sqlite3.connect(DB_Path)
        return self.connection

    def __exit__(self, exc_type, exc, tb):
        try:
            if exc_type is None:
                self.connection.commit()
            else:
                self.connection.rollback()
        finally:
            self.connection.close()

def init_db() -> None:
    with DatabaseConnection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS patients (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                age INTEGER NOT NULL CHECK(age BETWEEN 0 AND 120),
                diagnosis TEXT NOT NULL
            );
        """)

def add_patient(name: str, age: int, diagnosis: str) -> dict:
    with DatabaseConnection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO patients (name, age, diagnosis)
            VALUES (?, ?, ?);
            """,
            (name, age, diagnosis),
        )

        patient_id = cursor.lastrowid

        return {
            "id": patient_id,
            "name": name,
            "age": age,
            "diagnosis": diagnosis
        }

def get_patients() -> list[dict]:
    with DatabaseConnection() as connection:
        cursor = connection.execute(
            "SELECT id, name, age, diagnosis FROM patients ORDER BY id;"
        )

        rows = cursor.fetchall()


    patients = []

    for patient_id, name, age, diagnosis in rows:
        patients.append({
            "id": patient_id,
            "name": name,
            "age": age,
            "diagnosis": diagnosis
        })
    return patients


def get_patient_by_id(patient_id: int) -> dict | None:
    with DatabaseConnection() as connection:
        cursor = connection.execute(
            """
            SELECT id, name, age, diagnosis FROM patients WHERE id = ?;
            """,
            (patient_id,)
        )

        row = cursor.fetchone()

    if row is None:
        return None

    patient_id, name, age, diagnosis = row

    return {
        "id": patient_id,
        "name": name,
        "age": age,
        "diagnosis": diagnosis,
    }


def update_diagnosis(patient_id: int, new_diagnosis: str) -> bool:
    with DatabaseConnection() as connection:
        cursor = connection.execute(
            """
            UPDATE patients SET diagnosis = ? WHERE id = ?;
            """,
            (new_diagnosis, patient_id)
        )

        update = cursor.rowcount > 0

    return update


def delete_patient(patient_id: int) -> bool:
    with DatabaseConnection() as connection:
        cursor = connection.execute(
            """
            DELETE FROM patients WHERE id = ?;
            """,
            (patient_id,)
        )

        deleted = cursor.rowcount > 0

        return deleted