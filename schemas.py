from pydantic import BaseModel, EmailStr
from datetime import date, time
from typing import Optional, List

# Esquemas de Usuario
class UsuarioCreate(BaseModel):
    nombre: str
    email: EmailStr
    contraseña: str
    telefono: Optional[str] = None

class UsuarioLogin(BaseModel):
    email: EmailStr
    contraseña: str

class UsuarioRead(BaseModel):
    id_usuario: int
    nombre: str
    email: str
    telefono: Optional[str]
    
    class Config:
        from_attributes = True

# Esquemas de Cita
class CitaCreate(BaseModel):
    id_barbero: int
    fecha: date
    hora: time
    estado: str = "pendiente"

class CitaRead(BaseModel):
    id_cita: int
    id_usuario: int
    id_barbero: int
    fecha: date
    hora: time
    estado: str
    
    class Config:
        from_attributes = True

class CitaUpdate(BaseModel):
    id_barbero: int = None
    fecha: date = None
    hora: time = None
    estado: str = None

# Esquema para Perfil con Historial
class PerfilUsuario(BaseModel):
    id_usuario: int
    nombre: str
    email: str
    telefono: Optional[str]
    citas: List[CitaRead] = []
    
    class Config:
        from_attributes = True
