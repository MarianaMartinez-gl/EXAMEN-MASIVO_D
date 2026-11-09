import os
import psycopg2
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


def conectar():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "db"),
        port=os.getenv("DB_PORT", "5432"),
        database=os.getenv("DB_NAME", "examen"),
        user=os.getenv("DB_USER", "admin"),
        password=os.getenv("DB_PASSWORD")
    )


@app.on_event("startup")
def crear_tabla():
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS resultados (
            id SERIAL PRIMARY KEY,
            producto VARCHAR(100) UNIQUE NOT NULL,
            ingreso_total NUMERIC(14,2) NOT NULL,
            creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conexion.commit()
    cursor.close()
    conexion.close()


class Resultado(BaseModel):
    producto: str
    ingreso_total: float


@app.get("/health")
def health():
    return {"estado": "API funcionando"}


@app.get("/resultados")
def obtener_resultados():
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT producto, ingreso_total, creado_en
        FROM resultados
        ORDER BY ingreso_total DESC
        LIMIT 10
    """)

    datos = cursor.fetchall()

    cursor.close()
    conexion.close()

    return [
        {
            "producto": fila[0],
            "ingreso_total": float(fila[1]),
            "creado_en": fila[2].isoformat()
        }
        for fila in datos
    ]


@app.post("/resultados")
def guardar_resultado(resultado: Resultado):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        INSERT INTO resultados (producto, ingreso_total)
        VALUES (%s, %s)
        ON CONFLICT (producto)
        DO UPDATE SET
            ingreso_total = EXCLUDED.ingreso_total,
            creado_en = CURRENT_TIMESTAMP
    """, (resultado.producto, resultado.ingreso_total))

    conexion.commit()
    cursor.close()
    conexion.close()

    return {"mensaje": "Producto guardado correctamente"}
