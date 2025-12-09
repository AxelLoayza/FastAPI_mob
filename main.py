from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager

from database import engine, get_db, Base
from models import Cliente, Barbero, Cita, Usuario
from schemas import (CitaCreate, CitaRead, CitaUpdate, UsuarioCreate, 
                     UsuarioLogin, UsuarioRead, PerfilUsuario)
from crud import (create_cita, get_citas, get_cita, update_cita, delete_cita, 
                  init_static_data, create_usuario, authenticate_usuario, 
                  get_usuario_by_email, get_usuario_by_id, get_citas_usuario)

# Las tablas se crean ahora vía Alembic migrations
# Base.metadata.create_all(bind=engine)  # Comentado: usar 'alembic upgrade head' en su lugar

# Inicializar datos estáticos en startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    db = next(get_db())
    try:
        init_static_data(db)
    finally:
        db.close()
    yield

app = FastAPI(lifespan=lifespan, title="Barber API", version="1.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============= RUTAS DE AUTENTICACION =============

@app.post("/registro/", response_model=UsuarioRead)
def registrar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    usuario_existente = get_usuario_by_email(db, usuario.email)
    if usuario_existente:
        raise HTTPException(status_code=400, detail="Email ya registrado")
    return create_usuario(db, usuario)

@app.post("/login/")
def login_usuario(credenciales: UsuarioLogin, db: Session = Depends(get_db)):
    usuario = authenticate_usuario(db, credenciales.email, credenciales.contraseña)
    if not usuario:
        raise HTTPException(status_code=401, detail="Email o contraseña incorrectos")
    return {
        "id_usuario": usuario.id_usuario,
        "nombre": usuario.nombre,
        "email": usuario.email,
        "mensaje": "Login exitoso"
    }

@app.get("/perfil/{usuario_id}", response_model=PerfilUsuario)
def obtener_perfil(usuario_id: int, db: Session = Depends(get_db)):
    usuario = get_usuario_by_id(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    citas = get_citas_usuario(db, usuario_id)
    return {
        "id_usuario": usuario.id_usuario,
        "nombre": usuario.nombre,
        "email": usuario.email,
        "telefono": usuario.telefono,
        "citas": citas
    }

# ============= RUTAS CRUD CITAS =============

@app.post("/citas/", response_model=CitaRead)
def crear_cita_endpoint(usuario_id: int, cita: CitaCreate, db: Session = Depends(get_db)):
    usuario = get_usuario_by_id(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return create_cita(db, usuario_id, cita)

@app.get("/citas/", response_model=list[CitaRead])
def listar_citas(db: Session = Depends(get_db)):
    return get_citas(db)

@app.get("/citas/{cita_id}", response_model=CitaRead)
def obtener_cita(cita_id: int, db: Session = Depends(get_db)):
    cita = get_cita(db, cita_id)
    if not cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    return cita

@app.put("/citas/{cita_id}", response_model=CitaRead)
def actualizar_cita(cita_id: int, cita: CitaUpdate, db: Session = Depends(get_db)):
    cita_actualizada = update_cita(db, cita_id, cita)
    if not cita_actualizada:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    return cita_actualizada

@app.delete("/citas/{cita_id}")
def eliminar_cita(cita_id: int, db: Session = Depends(get_db)):
    success = delete_cita(db, cita_id)
    if not success:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    return {"ok": True, "mensaje": "Cita eliminada exitosamente"}
