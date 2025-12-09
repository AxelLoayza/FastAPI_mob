from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from datetime import datetime, timedelta
from models import Cliente, Barbero, Cita, Usuario
from schemas import CitaCreate, CitaUpdate, UsuarioCreate, UsuarioLogin
from passlib.context import CryptContext

# Optimizar bcrypt con rounds reducidos para performance en producción
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=10  # Default es 12, reducir a 10 acelera el hash
)

# CRUD Usuarios
def create_usuario(db: Session, usuario: UsuarioCreate):
    hashed_password = pwd_context.hash(usuario.contraseña)
    db_usuario = Usuario(
        nombre=usuario.nombre,
        email=usuario.email,
        contraseña=hashed_password,
        telefono=usuario.telefono
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def get_usuario_by_email(db: Session, email: str):
    return db.query(Usuario).filter(Usuario.email == email).first()

def get_usuario_by_id(db: Session, usuario_id: int):
    return db.query(Usuario).filter(Usuario.id_usuario == usuario_id).first()

def authenticate_usuario(db: Session, email: str, contraseña: str):
    usuario = get_usuario_by_email(db, email)
    if not usuario:
        return None
    if not pwd_context.verify(contraseña, usuario.contraseña):
        return None
    return usuario

# CRUD Citas
def verificar_disponibilidad_barbero(db: Session, id_barbero: int, fecha, hora, duracion_minutos: int) -> tuple[bool, dict]:
    """
    Verifica si el barbero está disponible considerando la duración real de la cita.
    Retorna (disponible: bool, info_conflicto: dict)
    """
    # Calcular hora de inicio y fin de la nueva cita
    hora_inicio_dt = datetime.combine(fecha, hora)
    hora_fin_dt = hora_inicio_dt + timedelta(minutes=duracion_minutos)
    
    # Buscar todas las citas del barbero en la misma fecha (excepto canceladas)
    citas_existentes = db.query(Cita).filter(
        and_(
            Cita.id_barbero == id_barbero,
            Cita.fecha == fecha,
            Cita.estado != "cancelada"
        )
    ).all()
    
    # Verificar solapamiento con cada cita existente
    for cita_existente in citas_existentes:
        cita_inicio_dt = datetime.combine(fecha, cita_existente.hora)
        cita_fin_dt = cita_inicio_dt + timedelta(minutes=cita_existente.duracion_minutos)
        
        # Hay solapamiento si:
        # - La nueva cita empieza antes de que termine la existente Y
        # - La nueva cita termina después de que empiece la existente
        if hora_inicio_dt < cita_fin_dt and hora_fin_dt > cita_inicio_dt:
            return False, {
                "id": cita_existente.id_cita,
                "hora_inicio": cita_existente.hora.strftime("%H:%M:%S"),
                "hora_fin": cita_fin_dt.time().strftime("%H:%M:%S"),
                "servicio": cita_existente.servicio or "No especificado"
            }
    
    return True, {}

def create_cita(db: Session, usuario_id: int, cita: CitaCreate):
    # Validar disponibilidad del barbero con duración real
    disponible, cita_conflicto = verificar_disponibilidad_barbero(
        db, cita.id_barbero, cita.fecha, cita.hora, cita.duracion_minutos
    )
    
    if not disponible:
        return None, cita_conflicto  # Retorna None y datos del conflicto
    
    db_cita = Cita(
        id_usuario=usuario_id,
        id_barbero=cita.id_barbero,
        fecha=cita.fecha,
        hora=cita.hora,
        estado=cita.estado,
        servicio=cita.servicio,
        duracion_minutos=cita.duracion_minutos
    )
    db.add(db_cita)
    db.commit()
    db.refresh(db_cita)
    return db_cita, {}

def get_citas(db: Session):
    return db.query(Cita).all()

def get_cita(db: Session, cita_id: int):
    return db.query(Cita).filter(Cita.id_cita == cita_id).first()

def get_citas_usuario(db: Session, usuario_id: int):
    return db.query(Cita).filter(Cita.id_usuario == usuario_id).all()

def update_cita(db: Session, cita_id: int, cita: CitaUpdate):
    db_cita = db.query(Cita).filter(Cita.id_cita == cita_id).first()
    if db_cita:
        cita_data = cita.dict(exclude_unset=True)
        for key, value in cita_data.items():
            if value is not None:
                setattr(db_cita, key, value)
        db.commit()
        db.refresh(db_cita)
    return db_cita

def delete_cita(db: Session, cita_id: int):
    db_cita = db.query(Cita).filter(Cita.id_cita == cita_id).first()
    if db_cita:
        db.delete(db_cita)
        db.commit()
        return True
    return False

# Datos estáticos
def init_static_data(db: Session):
    if db.query(Cliente).count() == 0:
        db.add_all([
            Cliente(nombre="Juan Perez", telefono="123456789"),
            Cliente(nombre="Maria Lopez", telefono="987654321")
        ])
    if db.query(Barbero).count() == 0:
        db.add_all([
            Barbero(nombre="Carlos"),
            Barbero(nombre="Luis")
        ])
    db.commit()
