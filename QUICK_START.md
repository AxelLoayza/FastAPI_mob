# 🚀 Guía Rápida - API Barbershop

## 📱 Endpoints Resumen

### Autenticación
```
POST   /registro/          - Crear usuario
POST   /login/             - Iniciar sesión
GET    /perfil/{id}        - Ver perfil + historial
```

### Citas
```
POST   /citas/?usuario_id=X    - Crear cita
GET    /citas/                 - Listar todas
GET    /citas/{id}             - Ver cita
PUT    /citas/{id}             - Actualizar cita
DELETE /citas/{id}             - Eliminar cita
```

### Documentación
```
GET    /docs       - Swagger UI interactivo
GET    /redoc      - ReDoc
GET    /openapi.json - Schema JSON
```

---

## 🔐 Flujo de Uso

### 1️⃣ Registrar Usuario
```bash
curl -X POST http://localhost:8000/registro/ \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Juan",
    "email": "juan@example.com",
    "contraseña": "pass123",
    "telefono": "123456"
  }'
```

**Respuesta:**
```json
{
  "id_usuario": 1,
  "nombre": "Juan",
  "email": "juan@example.com",
  "telefono": "123456",
  "activo": true
}
```

---

### 2️⃣ Hacer Login
```bash
curl -X POST http://localhost:8000/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "juan@example.com",
    "contraseña": "pass123"
  }'
```

**Respuesta:**
```json
{
  "id_usuario": 1,
  "nombre": "Juan",
  "email": "juan@example.com",
  "mensaje": "Login exitoso"
}
```

---

### 3️⃣ Crear una Cita
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

**Respuesta:**
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

---

### 4️⃣ Ver Historial de Usuario
```bash
curl -X GET http://localhost:8000/perfil/1
```

**Respuesta:**
```json
{
  "id_usuario": 1,
  "nombre": "Juan",
  "email": "juan@example.com",
  "telefono": "123456",
  "citas": [
    {
      "id_cita": 1,
      "id_usuario": 1,
      "id_barbero": 1,
      "fecha": "2025-12-15",
      "hora": "14:30:00",
      "estado": "pendiente"
    }
  ]
}
```

---

### 5️⃣ Actualizar Estado de Cita
```bash
curl -X PUT http://localhost:8000/citas/1 \
  -H "Content-Type: application/json" \
  -d '{
    "estado": "confirmada"
  }'
```

---

### 6️⃣ Eliminar Cita
```bash
curl -X DELETE http://localhost:8000/citas/1
```

**Respuesta:**
```json
{
  "ok": true,
  "mensaje": "Cita eliminada exitosamente"
}
```

---

## 📝 Valores Válidos

### Estados de Cita
- `pendiente` - Cita creada pero no confirmada
- `confirmada` - Cita confirmada
- `cancelada` - Cita cancelada

### Formatos
- **Fecha:** `YYYY-MM-DD` (2025-12-15)
- **Hora:** `HH:MM:SS` (14:30:00)

---

## ⚠️ Errores Comunes

| Error | Causa | Solución |
|-------|-------|----------|
| 400 Bad Request | Email duplicado | Usa otro email |
| 401 Unauthorized | Contraseña incorrecta | Verifica credenciales |
| 404 Not Found | ID no existe | Verifica el ID |
| 500 Server Error | Error servidor | Revisa logs |

---

## 🛠️ Desarrollo Local

```bash
# 1. Activar entorno
venv\Scripts\activate

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Ejecutar servidor
python run_server.py

# 4. Acceder a documentación
http://localhost:8000/docs
```

---

## 🌍 Producción (Render)

```bash
# Build Command
bash build.sh

# Start Command
uvicorn main:app --host 0.0.0.0 --port $PORT
```

---

## 📚 Más Información

- 📖 Documentación completa: `API_DOCUMENTATION.md`
- 🧪 Tests: `test_api_simple.py`
- 🔧 Configuración: `.env`
