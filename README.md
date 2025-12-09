# 💈 API Barbershop - Gestión de Citas

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue?style=flat-square)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.124.0-green?style=flat-square)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Supabase-blue?style=flat-square)](https://supabase.com/)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen?style=flat-square)]()

Sistema REST API completo para gestionar citas de barbería. Construido con **FastAPI**, **SQLAlchemy** y **PostgreSQL**.

---

## ✨ Características

- ✅ **Autenticación de Usuarios** - Registro y login con bcrypt
- ✅ **CRUD Citas** - Crear, leer, actualizar, eliminar citas
- ✅ **Perfiles** - Ver perfil y historial de citas
- ✅ **Documentación Automática** - Swagger UI y ReDoc
- ✅ **Base de Datos** - PostgreSQL con migraciones Alembic
- ✅ **CORS Habilitado** - Para integraciones con frontend
- ✅ **Validación** - Schemas con Pydantic
- ✅ **Seguridad** - Hashing bcrypt, validación de datos

---

## 🚀 Quick Start

### 1. Clonar Repositorio
```bash
git clone https://github.com/AxelLoayza/FastAPI_mob.git
cd API
```

### 2. Crear Entorno Virtual
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar Variables de Entorno
```bash
# Crear archivo .env con:
DATABASE_URL=postgresql://usuario:password@host:puerto/db?pgbouncer=true
DIRECT_URL=postgresql://usuario:password@host:puerto/db
ENVIRONMENT=development
DEBUG=True
SECRET_KEY=tu-clave-secreta
```

### 5. Ejecutar Migraciones
```bash
alembic upgrade head
```

### 6. Iniciar Servidor
```bash
python run_server.py
```

### 7. Acceder a Documentación
```
http://localhost:8000/docs
```

---

## 📡 API Endpoints

### 🔐 Autenticación
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/registro/` | Registrar nuevo usuario |
| POST | `/login/` | Iniciar sesión |
| GET | `/perfil/{usuario_id}` | Obtener perfil + historial |

### 📅 Citas
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/citas/` | Crear cita |
| GET | `/citas/` | Listar todas las citas |
| GET | `/citas/{cita_id}` | Obtener cita específica |
| PUT | `/citas/{cita_id}` | Actualizar cita |
| DELETE | `/citas/{cita_id}` | Eliminar cita |

### 📚 Documentación
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/docs` | Swagger UI |
| GET | `/redoc` | ReDoc |
| GET | `/openapi.json` | OpenAPI Schema |

---

## 💡 Ejemplos de Uso

### Registrar Usuario
```bash
curl -X POST "http://localhost:8000/registro/" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Juan Pérez",
    "email": "juan@example.com",
    "contraseña": "MiPassword123!",
    "telefono": "987654321"
  }'
```

### Crear Cita
```bash
curl -X POST "http://localhost:8000/citas/?usuario_id=1" \
  -H "Content-Type: application/json" \
  -d '{
    "id_barbero": 1,
    "fecha": "2025-12-15",
    "hora": "14:30:00",
    "estado": "pendiente"
  }'
```

Más ejemplos en [QUICK_START.md](./QUICK_START.md)

---

## 📁 Estructura del Proyecto

```
API/
├── main.py                    # Aplicación FastAPI
├── database.py                # Configuración de BD
├── models.py                  # Modelos SQLAlchemy
├── schemas.py                 # Schemas Pydantic
├── crud.py                    # Lógica CRUD
├── config.py                  # Configuración
├── requirements.txt           # Dependencias
├── run_server.py              # Script servidor
├── build.sh                   # Build script para Render
├── alembic/                   # Migraciones
│   ├── env.py
│   ├── versions/
│   └── alembic.ini
├── .env                       # Variables de entorno
├── .gitignore
├── API_DOCUMENTATION.md       # Documentación completa
├── QUICK_START.md             # Guía rápida
├── test_api_simple.py         # Tests simples
└── test_api.py                # Tests completos
```

---

## 🔧 Tecnologías

- **Framework:** FastAPI 0.124.0
- **Server:** Uvicorn 0.38.0
- **ORM:** SQLAlchemy 2.0.44
- **DB Driver:** psycopg2-binary 2.9.9
- **Migrations:** Alembic 1.13.1
- **Security:** bcrypt 4.0.1, passlib 1.7.4
- **Validation:** Pydantic 2.12.5
- **Database:** PostgreSQL (Supabase)

---

## 📋 Modelos de Datos

### Usuario
```json
{
  "id_usuario": 1,
  "nombre": "Juan Pérez",
  "email": "juan@example.com",
  "contraseña": "hash_bcrypt",
  "telefono": "987654321",
  "activo": true
}
```

### Cita
```json
{
  "id_cita": 1,
  "id_usuario": 1,
  "id_barbero": 1,
  "fecha": "2025-12-15",
  "hora": "14:30:00",
  "estado": "pendiente"
}
```

### Barbero
```json
{
  "id_barbero": 1,
  "nombre": "Carlos"
}
```

---

## ✅ Testing

Ejecutar tests:
```bash
python test_api_simple.py
```

Todos los tests deben pasar con status 200 ✓

---

## 🌍 Despliegue en Render

### Configuración en Render

1. **Build Command:**
```bash
bash build.sh
```

2. **Start Command:**
```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

3. **Variables de Entorno:**
```
DATABASE_URL=...
DIRECT_URL=...
ENVIRONMENT=production
DEBUG=False
SECRET_KEY=...
```

4. **Python Version:** 3.11+

### Deploy
```bash
git add .
git commit -m "API ready for production"
git push origin main
```

Render desplegará automáticamente desde GitHub.

---

## 🔒 Seguridad

- ✅ Contraseñas hasheadas con bcrypt
- ✅ Validación de entrada con Pydantic
- ✅ CORS habilitado
- ✅ Variables de entorno protegidas
- ✅ SQL Inyection prevención (SQLAlchemy)

---

## 📖 Documentación

- **[API_DOCUMENTATION.md](./API_DOCUMENTATION.md)** - Documentación completa
- **[QUICK_START.md](./QUICK_START.md)** - Guía rápida
- **[RENDER_DEPLOYMENT.md](./RENDER_DEPLOYMENT.md)** - Despliegue en Render

---

## 🐛 Solución de Problemas

### Error: "DATABASE_URL no configurada"
→ Verifica archivo `.env` y variables en Render

### Error en migraciones
→ Ejecuta: `alembic upgrade head`

### Puerto en uso
→ Cambia puerto en `run_server.py`

### Error de conexión a BD
→ Verifica credenciales de Supabase

---

## 📞 Contacto

**Desarrollador:** Axel Loayza  
**Email:** axelloayza@example.com  
**GitHub:** [@AxelLoayza](https://github.com/AxelLoayza)

---

## 📄 Licencia

Este proyecto está bajo la licencia MIT.

---

**Última actualización:** Diciembre 8, 2025  
**Estado:** ✅ Listo para Producción
