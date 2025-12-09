# 📖 Documentación API Barbershop

**Versión:** 1.0  
**Autor:** Team Barbershop  
**Fecha:** Diciembre 2025  
**Base de Datos:** PostgreSQL (Supabase)  
**Framework:** FastAPI + SQLAlchemy + Alembic

---

## 📋 Tabla de Contenidos

1. [Introducción](#introducción)
2. [Configuración y Setup](#configuración-y-setup)
3. [Autenticación](#autenticación)
4. [Endpoints](#endpoints)
5. [Modelos de Datos](#modelos-de-datos)
6. [Códigos de Error](#códigos-de-error)
7. [Ejemplos de Uso](#ejemplos-de-uso)
8. [Despliegue](#despliegue)

---

## 🎯 Introducción

Esta es la API REST de la aplicación **Barbershop**, un sistema de gestión de citas para barberías. Permite:

- ✅ Registro y autenticación de usuarios
- ✅ Gestión completa de citas
- ✅ Consulta de perfiles y historial
- ✅ Documentación interactiva automática

**URL Base (Desarrollo):** `http://localhost:8000`  
**URL Base (Producción):** `https://tu-api.onrender.com`

---

## 🔧 Configuración y Setup

### Requisitos Previos

- Python 3.11+
- PostgreSQL (Supabase)
- Git

### Instalación Local

```bash
# 1. Clonar repositorio
git clone https://github.com/AxelLoayza/FastAPI_mob.git
cd API

# 2. Crear entorno virtual
python -m venv venv

# 3. Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Configurar variables de entorno
# Crear archivo .env con:
DATABASE_URL=postgresql://usuario:password@host:puerto/db?pgbouncer=true
DIRECT_URL=postgresql://usuario:password@host:puerto/db
ENVIRONMENT=development
DEBUG=True
SECRET_KEY=tu-clave-secreta

# 6. Ejecutar migraciones
alembic upgrade head

# 7. Iniciar servidor
python run_server.py
```

---

## 🔐 Autenticación

La API utiliza **autenticación basada en tokens implícitos**:

- Las contraseñas se hashean con **bcrypt**
- No hay JWT tokens implementados (validación por email/contraseña)
- CORS habilitado para todas las rutas

### Flujo de Autenticación

```
1. Usuario se registra: POST /registro/
2. Usuario hace login: POST /login/
3. Recibe id_usuario
4. Usa id_usuario en rutas que lo requieren
```

---

## 📡 Endpoints

### 🔓 Autenticación (Sin autenticación requerida)

#### 1. Registrar Usuario
```
POST /registro/
Content-Type: application/json

{
  "nombre": "Juan Pérez",
  "email": "juan@example.com",
  "contraseña": "MiPassword123!",
  "telefono": "987654321"
}
```

**Response (200):**
```json
{
  "id_usuario": 1,
  "nombre": "Juan Pérez",
  "email": "juan@example.com",
  "telefono": "987654321",
  "activo": true
}
```

**Errores:**
- `400`: Email ya registrado

---

#### 2. Login
```
POST /login/
Content-Type: application/json

{
  "email": "juan@example.com",
  "contraseña": "MiPassword123!"
}
```

**Response (200):**
```json
{
  "id_usuario": 1,
  "nombre": "Juan Pérez",
  "email": "juan@example.com",
  "mensaje": "Login exitoso"
}
```

**Errores:**
- `401`: Email o contraseña incorrectos

---

### 👤 Usuarios

#### 3. Obtener Perfil con Historial
```
GET /perfil/{usuario_id}
```

**Parámetros:**
- `usuario_id` (path, int, requerido): ID del usuario

**Response (200):**
```json
{
  "id_usuario": 1,
  "nombre": "Juan Pérez",
  "email": "juan@example.com",
  "telefono": "987654321",
  "citas": [
    {
      "id_cita": 1,
      "id_usuario": 1,
      "id_barbero": 1,
      "fecha": "2025-12-10",
      "hora": "14:30:00",
      "estado": "confirmada"
    }
  ]
}
```

**Errores:**
- `404`: Usuario no encontrado

---

### 📅 Citas

#### 4. Crear Cita
```
POST /citas/?usuario_id=1
Content-Type: application/json

{
  "id_barbero": 1,
  "fecha": "2025-12-10",
  "hora": "14:30:00",
  "estado": "pendiente"
}
```

**Parámetros:**
- `usuario_id` (query, int, requerido): ID del usuario

**Body:**
- `id_barbero` (int, requerido): ID del barbero
- `fecha` (date, requerido): Formato YYYY-MM-DD
- `hora` (time, requerido): Formato HH:MM:SS
- `estado` (string, requerido): pendiente, confirmada, cancelada

**Response (200):**
```json
{
  "id_cita": 1,
  "id_usuario": 1,
  "id_barbero": 1,
  "fecha": "2025-12-10",
  "hora": "14:30:00",
  "estado": "pendiente"
}
```

**Errores:**
- `404`: Usuario no encontrado

---

#### 5. Listar Todas las Citas
```
GET /citas/
```

**Response (200):**
```json
[
  {
    "id_cita": 1,
    "id_usuario": 1,
    "id_barbero": 1,
    "fecha": "2025-12-10",
    "hora": "14:30:00",
    "estado": "pendiente"
  },
  {
    "id_cita": 2,
    "id_usuario": 2,
    "id_barbero": 2,
    "fecha": "2025-12-11",
    "hora": "10:00:00",
    "estado": "confirmada"
  }
]
```

---

#### 6. Obtener Cita Específica
```
GET /citas/{cita_id}
```

**Parámetros:**
- `cita_id` (path, int, requerido): ID de la cita

**Response (200):**
```json
{
  "id_cita": 1,
  "id_usuario": 1,
  "id_barbero": 1,
  "fecha": "2025-12-10",
  "hora": "14:30:00",
  "estado": "pendiente"
}
```

**Errores:**
- `404`: Cita no encontrada

---

#### 7. Actualizar Cita
```
PUT /citas/{cita_id}
Content-Type: application/json

{
  "estado": "confirmada"
}
```

**Parámetros:**
- `cita_id` (path, int, requerido): ID de la cita

**Body:**
- `estado` (string, opcional): pendiente, confirmada, cancelada

**Response (200):**
```json
{
  "id_cita": 1,
  "id_usuario": 1,
  "id_barbero": 1,
  "fecha": "2025-12-10",
  "hora": "14:30:00",
  "estado": "confirmada"
}
```

**Errores:**
- `404`: Cita no encontrada

---

#### 8. Eliminar Cita
```
DELETE /citas/{cita_id}
```

**Parámetros:**
- `cita_id` (path, int, requerido): ID de la cita

**Response (200):**
```json
{
  "ok": true,
  "mensaje": "Cita eliminada exitosamente"
}
```

**Errores:**
- `404`: Cita no encontrada

---

### 📚 Documentación

#### Swagger UI (Interactivo)
```
GET /docs
```
Acceso: http://localhost:8000/docs

---

#### ReDoc
```
GET /redoc
```
Acceso: http://localhost:8000/redoc

---

#### OpenAPI JSON
```
GET /openapi.json
```
Esquema en formato JSON

---

## 💾 Modelos de Datos

### Usuario
```python
{
  "id_usuario": int,           # PK
  "nombre": str(100),          # Nombre completo
  "email": str(100),           # Email único
  "contraseña": str(255),      # Hash bcrypt
  "telefono": str(20),         # Opcional
  "activo": bool               # Estado del usuario
}
```

**Índices:**
- `email` (UNIQUE)
- `id_usuario` (PRIMARY KEY)

---

### Cita
```python
{
  "id_cita": int,              # PK
  "id_usuario": int,           # FK -> Usuario
  "id_barbero": int,           # FK -> Barbero
  "fecha": date,               # YYYY-MM-DD
  "hora": time,                # HH:MM:SS
  "estado": str(20)            # pendiente, confirmada, cancelada
}
```

**Índices:**
- `id_cita` (PRIMARY KEY)
- `id_usuario` (FOREIGN KEY)
- `id_barbero` (FOREIGN KEY)

---

### Barbero
```python
{
  "id_barbero": int,           # PK
  "nombre": str(100)           # Nombre del barbero
}
```

---

### Cliente
```python
{
  "id_cliente": int,           # PK
  "nombre": str(100),          # Nombre
  "telefono": str(20)          # Opcional
}
```

---

## ⚠️ Códigos de Error

| Código | Descripción |
|--------|-------------|
| `200` | OK - Solicitud exitosa |
| `400` | Bad Request - Datos inválidos o email duplicado |
| `401` | Unauthorized - Credenciales incorrectas |
| `404` | Not Found - Recurso no encontrado |
| `500` | Internal Server Error - Error del servidor |

---

## 💡 Ejemplos de Uso

### Con cURL

```bash
# 1. Registrar usuario
curl -X POST "http://localhost:8000/registro/" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Carlos Rodriguez",
    "email": "carlos@barbershop.com",
    "contraseña": "segura123",
    "telefono": "555123456"
  }'

# 2. Login
curl -X POST "http://localhost:8000/login/" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "carlos@barbershop.com",
    "contraseña": "segura123"
  }'

# 3. Crear cita
curl -X POST "http://localhost:8000/citas/?usuario_id=1" \
  -H "Content-Type: application/json" \
  -d '{
    "id_barbero": 1,
    "fecha": "2025-12-15",
    "hora": "14:30:00",
    "estado": "pendiente"
  }'

# 4. Obtener cita
curl -X GET "http://localhost:8000/citas/1"

# 5. Actualizar cita
curl -X PUT "http://localhost:8000/citas/1" \
  -H "Content-Type: application/json" \
  -d '{"estado": "confirmada"}'

# 6. Listar todas las citas
curl -X GET "http://localhost:8000/citas/"

# 7. Obtener perfil
curl -X GET "http://localhost:8000/perfil/1"

# 8. Eliminar cita
curl -X DELETE "http://localhost:8000/citas/1"
```

### Con Python

```python
import requests

BASE_URL = "http://localhost:8000"

# Registrar
response = requests.post(f"{BASE_URL}/registro/", json={
    "nombre": "Carlos",
    "email": "carlos@example.com",
    "contraseña": "pass123",
    "telefono": "123456"
})
usuario = response.json()
usuario_id = usuario['id_usuario']

# Login
response = requests.post(f"{BASE_URL}/login/", json={
    "email": "carlos@example.com",
    "contraseña": "pass123"
})
print(response.json())

# Crear cita
response = requests.post(f"{BASE_URL}/citas/?usuario_id={usuario_id}", json={
    "id_barbero": 1,
    "fecha": "2025-12-15",
    "hora": "14:30:00",
    "estado": "pendiente"
})
cita = response.json()
cita_id = cita['id_cita']

# Actualizar cita
response = requests.put(f"{BASE_URL}/citas/{cita_id}", json={
    "estado": "confirmada"
})
print(response.json())
```

### Con JavaScript

```javascript
const BASE_URL = "http://localhost:8000";

// Registrar
async function registrarUsuario() {
  const response = await fetch(`${BASE_URL}/registro/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      nombre: "Carlos",
      email: "carlos@example.com",
      contraseña: "pass123",
      telefono: "123456"
    })
  });
  return await response.json();
}

// Login
async function login(email, contraseña) {
  const response = await fetch(`${BASE_URL}/login/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, contraseña })
  });
  return await response.json();
}

// Crear cita
async function crearCita(usuarioId) {
  const response = await fetch(
    `${BASE_URL}/citas/?usuario_id=${usuarioId}`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        id_barbero: 1,
        fecha: "2025-12-15",
        hora: "14:30:00",
        estado: "pendiente"
      })
    }
  );
  return await response.json();
}
```

---

## 🚀 Despliegue

### Despliegue en Render

1. **Preparar repositorio:**
```bash
git add .
git commit -m "API lista para producción"
git push origin main
```

2. **En Render.com:**
   - Crear nuevo Web Service
   - Conectar repositorio de GitHub
   - Build Command: `bash build.sh`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

3. **Variables de entorno:**
```
DATABASE_URL=postgresql://...
DIRECT_URL=postgresql://...
ENVIRONMENT=production
DEBUG=False
SECRET_KEY=tu-clave-secreta
```

4. **Verificar:**
```
https://tu-api.onrender.com/docs
```

---

## 📊 Estructura de Carpetas

```
API/
├── main.py                 # Aplicación FastAPI
├── database.py             # Configuración de BD
├── models.py               # Modelos SQLAlchemy
├── schemas.py              # Schemas Pydantic
├── crud.py                 # Lógica CRUD
├── config.py               # Configuración
├── requirements.txt        # Dependencias
├── run_server.py           # Script para correr servidor
├── build.sh                # Script build para Render
├── alembic/                # Migraciones
│   ├── env.py
│   ├── versions/
│   │   └── *.py           # Archivos de migración
│   └── alembic.ini
├── .env                    # Variables de entorno
├── .gitignore              # Archivos a ignorar
└── API_DOCUMENTATION.md    # Esta documentación
```

---

## 🔍 Testing

Ejecutar tests:
```bash
python test_api_simple.py
```

---

## 📞 Soporte

Para reportar bugs o sugerencias, contacta al equipo de desarrollo.

---

**Última actualización:** Diciembre 8, 2025  
**Estado:** ✅ Producción Lista
