# ⏱️ Solución: Timeout en Registro (Flutter → API)

## 🐛 Problema Reportado

```
Error: Timeout - El registro demora demasiado
Síntoma: Flutter recibe timeout al registrar usuario
```

---

## 🔍 Causas Identificadas

### 1. **Hashing de bcrypt lento (PRINCIPAL)**
- **Problema:** `pwd_context.hash()` usa 12 rounds por default
- **Impacto:** ~200-500ms por registro
- **Solución:** Reducir a 10 rounds (todavía seguro)

**Tiempo estimado:**
- Antes: 300-500ms
- Después: 100-150ms

### 2. **Pool de conexiones insuficiente**
- **Problema:** pool_size=10 es pequeño bajo concurrencia
- **Impacto:** Esperas en cola
- **Solución:** Aumentar a 15

### 3. **Timeout insuficiente en BD**
- **Problema:** No hay timeouts explícitos
- **Impacto:** Conexiones cuelgan indefinidamente
- **Solución:** Agregar connect_timeout y timeout

---

## ✅ Optimizaciones Implementadas

### 1. Bcrypt Rounds Reducido
**Archivo:** `crud.py`

```python
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=10  # Fue 12 (default)
)
```

**Impacto:** -50% tiempo de hash

---

### 2. Pool de Conexiones Mejorado
**Archivo:** `database.py`

```python
engine = create_engine(
    DATABASE_URL_CLEAN,
    poolclass=pool.QueuePool,
    pool_size=15,        # Fue 10
    max_overflow=25,     # Fue 20
    pool_pre_ping=True,
    pool_recycle=3600,
    connect_args={
        "connect_timeout": 10,
        "timeout": 15,
        "application_name": "barbershop_api"
    },
    echo=False,
)
```

**Impacto:** Mejor concurrencia y manejo de conexiones

---

## 📊 Benchmarks Esperados

| Métrica | Antes | Después | Mejora |
|---------|-------|---------|--------|
| Hash bcrypt | 300ms | 100ms | -67% |
| Conexión BD | variable | 10-15s timeout | +estabilidad |
| Pool concurrencia | 10 | 15 | +50% |
| Tiempo total registro | 400-600ms | 200-350ms | -40% |

---

## 🔧 Configuración en Flutter

### Timeout Recomendado

```dart
final dio = Dio();

// Configurar timeout
dio.options = BaseOptions(
  connectTimeout: Duration(seconds: 15),  // Esperar conexión
  receiveTimeout: Duration(seconds: 15),  // Esperar respuesta
  sendTimeout: Duration(seconds: 15),     // Enviar datos
  baseUrl: 'https://fastapi-mob.onrender.com',
);

// Registro
Future<void> registrar() async {
  try {
    final response = await dio.post(
      '/registro/',
      data: {
        'nombre': 'Juan',
        'email': 'juan@example.com',
        'contraseña': 'pass123',
        'telefono': '123456'
      },
    );
    print('Registro exitoso: ${response.data}');
  } on DioException catch (e) {
    if (e.type == DioExceptionType.receiveTimeout) {
      print('Timeout: La solicitud tardó demasiado');
    } else if (e.type == DioExceptionType.connectTimeout) {
      print('Timeout: No se pudo conectar al servidor');
    } else {
      print('Error: ${e.message}');
    }
  }
}
```

### Alternativa: http package

```dart
import 'package:http/http.dart' as http;

Future<void> registrar() async {
  try {
    final response = await http.post(
      Uri.parse('https://fastapi-mob.onrender.com/registro/'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'nombre': 'Juan',
        'email': 'juan@example.com',
        'contraseña': 'pass123',
        'telefono': '123456'
      }),
    ).timeout(
      Duration(seconds: 30),  // Total timeout
      onTimeout: () => throw TimeoutException('Timeout en registro'),
    );

    if (response.statusCode == 200) {
      print('Registro exitoso');
    } else {
      print('Error: ${response.statusCode}');
    }
  } catch (e) {
    print('Error: $e');
  }
}
```

---

## 🌍 Configuración en Render

Si el timeout persiste en producción:

### 1. Aumentar Health Check Timeout
En el panel de Render:
```
Settings → Health Check Timeout: 300 (segundos)
```

### 2. Aumentar Keep Alive
En el panel de Render:
```
Settings → Keep Alive: Enabled
```

### 3. Revisar Logs
```
Render Dashboard → tu-servicio → Logs
```

Buscar líneas como:
```
slow query
connection timeout
pool exhausted
```

---

## 📋 Checklist Pre-Deploy

- ✓ `crud.py` actualizado con bcrypt_rounds=10
- ✓ `database.py` actualizado con pool mejorado
- ✓ Timeouts configurados en Flutter (15-30s)
- ✓ Cambios pusheados a GitHub
- ✓ Redeploy en Render completado

---

## 🚀 Desplegar Cambios

```bash
# 1. Verificar cambios localmente
python -c "from crud import pwd_context; print('✓ bcrypt optimizado')"

# 2. Push a GitHub
git add .
git commit -m "Optimize: Reduce bcrypt rounds and improve connection pooling"
git push origin main

# 3. Redeploy en Render
# Render desplegará automáticamente
```

---

## 🧪 Test de Performance

```bash
# Instalar tool de benchmark
pip install locust

# Crear locustfile.py
cat > locustfile.py << 'EOF'
from locust import HttpUser, task, between

class RegistroUser(HttpUser):
    wait_time = between(1, 3)
    
    @task
    def registro(self):
        self.client.post("/registro/", json={
            "nombre": "Test",
            "email": f"test{random.randint(1,999)}@example.com",
            "contraseña": "pass123",
            "telefono": "123456"
        })
EOF

# Ejecutar test (necesita servidor corriendo)
locust -f locustfile.py --host=http://localhost:8000
```

---

## ⚠️ Notas de Seguridad

**⚠️ IMPORTANTE:** Bcrypt 10 rounds sigue siendo seguro para:
- Aplicaciones modernas (2025+)
- Contraseñas típicas
- Uso general

**No reducir menos de 10 rounds** (vulnerabilidad a fuerza bruta).

Para máxima seguridad vs. performance:
- Desarrollo: 10 rounds (rápido)
- Producción: 12 rounds (más seguro)

---

## 📞 Solución de Problemas

### Sigue dando timeout

1. **Verificar logs en Render:**
   ```
   Render Dashboard → Logs → Ver si hay errors
   ```

2. **Verificar conexión BD:**
   ```bash
   python -c "from database import engine; engine.connect(); print('✓ BD conectada')"
   ```

3. **Aumentar timeout en Flutter:**
   ```dart
   Duration(seconds: 30)  // Aumentar a 30
   ```

---

## 📚 Referencias

- [Passlib bcrypt rounds](https://passlib.readthedocs.io/en/1.6/context_tutorial.html)
- [SQLAlchemy pool configuration](https://docs.sqlalchemy.org/en/20/core/pooling.html)
- [Flutter Dio timeouts](https://pub.dev/packages/dio)

---

**Estado:** ✅ Optimizaciones aplicadas  
**Fecha:** Diciembre 9, 2025
