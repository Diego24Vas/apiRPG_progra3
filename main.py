from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
from models import Personaje, Mision, Base
from cola import Cola

# Configuración de la aplicación FastAPI
app = FastAPI()

# Configuración de la base de datos SQLite
DATABASE_URL = "sqlite:///./apiRPG.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Diccionario para gestionar las colas de misiones por personaje
colas_misiones = {}

# Modelo para crear un personaje.
class PersonajeCrear(BaseModel):
    nombre: str
    nivel: int


# Modelo para crear una misión.
class MisionCrear(BaseModel):
    nombre: str
    descripcion: str
    nivel_requerido: int


# Crea un personaje y asigna una cola de misiones vacía.
@app.post("/personajes/")
def crear_personaje(personaje: PersonajeCrear):
    
    db = SessionLocal()
    nuevo_personaje = Personaje(nombre=personaje.nombre, nivel=personaje.nivel)
    db.add(nuevo_personaje)
    db.commit()
    db.refresh(nuevo_personaje)
    colas_misiones[nuevo_personaje.id] = Cola()
    return nuevo_personaje


# Crea una misión en la base de datos.
@app.post("/misiones/")
def crear_mision(mision: MisionCrear):
    db = SessionLocal()
    nueva_mision = Mision(
        nombre=mision.nombre,
        descripcion=mision.descripcion,
        nivel_requerido=mision.nivel_requerido
    )
    db.add(nueva_mision)
    db.commit()
    db.refresh(nueva_mision)
    return nueva_mision


# Un personaje acepta una misión y la agrega a su cola.
@app.post("/personajes/{personaje_id}/misiones/{mision_id}")
def aceptar_mision(personaje_id: int, mision_id: int):

    db = SessionLocal()
    personaje = db.query(Personaje).filter_by(id=personaje_id).first()
    mision = db.query(Mision).filter_by(id=mision_id).first()

    if not personaje or not mision:
        raise HTTPException(status_code=404, detail="Personaje o misión no encontrados")

    personaje.misiones.append(mision)
    db.commit()

    if personaje_id not in colas_misiones:
        colas_misiones[personaje_id] = Cola()
    colas_misiones[personaje_id].agregar(mision.nombre)

    return {"message": f"Misión '{mision.nombre}' aceptada por {personaje.nombre}"}



# Un personaje completa una misión y gana XP.
@app.post("/personajes/{personaje_id}/completar")
def completar_mision(personaje_id: int):
    db = SessionLocal()
    personaje = db.query(Personaje).filter_by(id=personaje_id).first()

    if personaje_id not in colas_misiones or colas_misiones[personaje_id].esta_vacia():
        raise HTTPException(status_code=404, detail="No hay misiones en cola")

    mision_completada = colas_misiones[personaje_id].eliminar()

    # Sumar XP al personaje
    xp_ganado = 10
    personaje.xp += xp_ganado

    db.commit()

    return {"message": f"Misión completada: {mision_completada}. {personaje.nombre} ha ganado {xp_ganado} XP."}



# Lista las misiones en espera de un personaje.
@app.get("/personajes/{personaje_id}/misiones")
def listar_misiones(personaje_id: int):


    if personaje_id not in colas_misiones:
        return {"misiones": []}
    return {"misiones": colas_misiones[personaje_id].items}