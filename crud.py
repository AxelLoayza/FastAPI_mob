from sqlalchemy.orm import Session
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
def create_cita(db: Session, usuario_id: int, cita: CitaCreate):
    db_cita = Cita(
        id_usuario=usuario_id,
        id_barbero=cita.id_barbero,
        fecha=cita.fecha,
        hora=cita.hora,
        estado=cita.estado
    )
    db.add(db_cita)
    db.commit()
    db.refresh(db_cita)
    return db_cita

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
