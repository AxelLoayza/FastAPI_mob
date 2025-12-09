from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    id_usuario = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    contraseña = Column(String(255), nullable=False)
    telefono = Column(String(20))
    activo = Column(Boolean, default=True)

class Cliente(Base):
    __tablename__ = "clientes"
    id_cliente = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    telefono = Column(String(20))

class Barbero(Base):
    __tablename__ = "barberos"
    id_barbero = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)

class Cita(Base):
    __tablename__ = "citas"
    id_cita = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)
    id_barbero = Column(Integer, ForeignKey("barberos.id_barbero"), nullable=False)
    fecha = Column(Date, nullable=False)
    hora = Column(Time, nullable=False)
    estado = Column(String(20), default="pendiente")
    servicio = Column(String(100), nullable=True)  # Nuevo campo
    duracion_minutos = Column(Integer, default=30)  # Nuevo campo con default 30 min

    usuario = relationship("Usuario")
    barbero = relationship("Barbero")
