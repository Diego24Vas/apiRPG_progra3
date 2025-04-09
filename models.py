from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


# Base de datos SQLAlchemy
Base = declarative_base()


# Relación muchos a muchos entre personajes y misiones
personaje_mision = Table(
    'personaje_mision',
    Base.metadata,
    Column('personaje_id', Integer, ForeignKey('personajes.id')),
    Column('mision_id', Integer, ForeignKey('misiones.id'))
)



# Representa a un personaje con XP y misiones asociadas.
class Personaje(Base):

    __tablename__ = 'personajes'
    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    nivel = Column(Integer, nullable=False)
    xp = Column(Integer, default=0)  # Puntos de XP

    misiones = relationship("Mision", secondary=personaje_mision, back_populates="personajes")



# Representa una misión con un nivel requerido y personajes asociados.
class Mision(Base):
    __tablename__ = 'misiones'
    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(String)
    nivel_requerido = Column(Integer, nullable=False)

    personajes = relationship("Personaje", secondary=personaje_mision, back_populates="misiones")
