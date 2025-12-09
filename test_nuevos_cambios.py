"""
Script de prueba para verificar los cambios de Prioridad Alta:
1. Campo servicio en respuestas
2. Campo duracion_minutos
3. Validación de solapamiento con duración real
"""
import requests
import json
from datetime import date, time

BASE_URL = "http://localhost:8000"

def test_crear_cita_con_servicio_y_duracion():
    """Test: Crear cita con servicio y duración, verificar que se devuelven en la respuesta"""
    print("\n=== TEST 1: Crear cita con servicio y duración ===")
    
    # Datos de prueba
    payload = {
        "id_barbero": 1,
        "fecha": "2025-12-15",
        "hora": "14:00:00",
        "estado": "pendiente",
        "servicio": "Corte Premium",
        "duracion_minutos": 45
    }
    
    response = requests.post(f"{BASE_URL}/citas/?usuario_id=1", json=payload)
    
    if response.status_code == 201 or response.status_code == 200:
        cita = response.json()
        print(f"✅ Cita creada exitosamente:")
        print(f"   ID: {cita['id_cita']}")
        print(f"   Servicio: {cita.get('servicio', 'NO DEVUELTO')}")
        print(f"   Duración: {cita.get('duracion_minutos', 'NO DEVUELTO')} minutos")
        return cita['id_cita']
    else:
        print(f"❌ Error: {response.status_code}")
        print(f"   Detalle: {response.text}")
        return None

def test_verificar_campo_servicio(cita_id):
    """Test: Verificar que GET /citas/{id} devuelve el campo servicio"""
    print(f"\n=== TEST 2: Verificar campo servicio en GET /citas/{cita_id} ===")
    
    response = requests.get(f"{BASE_URL}/citas/{cita_id}")
    
    if response.status_code == 200:
        cita = response.json()
        if 'servicio' in cita:
            print(f"✅ Campo 'servicio' presente: {cita['servicio']}")
        else:
            print(f"❌ Campo 'servicio' NO presente en la respuesta")
            
        if 'duracion_minutos' in cita:
            print(f"✅ Campo 'duracion_minutos' presente: {cita['duracion_minutos']} min")
        else:
            print(f"❌ Campo 'duracion_minutos' NO presente en la respuesta")
    else:
        print(f"❌ Error al obtener cita: {response.status_code}")

def test_validacion_solapamiento():
    """Test: Intentar crear una cita que se solape con otra existente"""
    print("\n=== TEST 3: Validación de solapamiento ===")
    
    # Crear primera cita: 15:00 - 15:45 (45 min)
    print("Paso 1: Crear cita de 15:00 a 15:45 (45 min)")
    payload1 = {
        "id_barbero": 1,
        "fecha": "2025-12-16",
        "hora": "15:00:00",
        "servicio": "Corte + Barba",
        "duracion_minutos": 45
    }
    
    response1 = requests.post(f"{BASE_URL}/citas/?usuario_id=1", json=payload1)
    
    if response1.status_code in [200, 201]:
        print(f"✅ Primera cita creada (ID: {response1.json()['id_cita']})")
    else:
        print(f"❌ Error creando primera cita: {response1.status_code}")
        return
    
    # Intentar crear segunda cita que se solape: 15:30 - 16:00 (30 min)
    print("\nPaso 2: Intentar crear cita solapada (15:30 - 16:00)")
    payload2 = {
        "id_barbero": 1,
        "fecha": "2025-12-16",
        "hora": "15:30:00",
        "servicio": "Corte Clásico",
        "duracion_minutos": 30
    }
    
    response2 = requests.post(f"{BASE_URL}/citas/?usuario_id=1", json=payload2)
    
    if response2.status_code == 409:
        print(f"✅ Validación funcionó correctamente - Conflicto detectado (409)")
        error_detail = response2.json()
        print(f"   Mensaje: {json.dumps(error_detail, indent=2, ensure_ascii=False)}")
    else:
        print(f"❌ La validación NO funcionó - Status: {response2.status_code}")
        print(f"   Se esperaba 409 Conflict")
    
    # Intentar crear tercera cita que NO se solape: 15:45 - 16:15 (30 min)
    print("\nPaso 3: Crear cita válida (15:45 - 16:15)")
    payload3 = {
        "id_barbero": 1,
        "fecha": "2025-12-16",
        "hora": "15:45:00",
        "servicio": "Afeitado",
        "duracion_minutos": 30
    }
    
    response3 = requests.post(f"{BASE_URL}/citas/?usuario_id=1", json=payload3)
    
    if response3.status_code in [200, 201]:
        print(f"✅ Cita válida creada exitosamente (ID: {response3.json()['id_cita']})")
    else:
        print(f"❌ Error: {response3.status_code} - {response3.text}")

def test_listar_todas_citas():
    """Test: Verificar que GET /citas devuelve los nuevos campos"""
    print("\n=== TEST 4: Listar todas las citas ===")
    
    response = requests.get(f"{BASE_URL}/citas/")
    
    if response.status_code == 200:
        citas = response.json()
        print(f"✅ Total de citas: {len(citas)}")
        
        if len(citas) > 0:
            primera_cita = citas[0]
            print(f"\nEjemplo de cita:")
            print(f"  ID: {primera_cita.get('id_cita')}")
            print(f"  Servicio: {primera_cita.get('servicio', 'NO PRESENTE')}")
            print(f"  Duración: {primera_cita.get('duracion_minutos', 'NO PRESENTE')} min")
            print(f"  Fecha: {primera_cita.get('fecha')}")
            print(f"  Hora: {primera_cita.get('hora')}")
    else:
        print(f"❌ Error: {response.status_code}")

if __name__ == "__main__":
    print("=" * 60)
    print("PRUEBAS DE REQUERIMIENTOS DE PRIORIDAD ALTA")
    print("=" * 60)
    
    try:
        # Test 1: Crear cita con nuevos campos
        cita_id = test_crear_cita_con_servicio_y_duracion()
        
        # Test 2: Verificar campos en GET
        if cita_id:
            test_verificar_campo_servicio(cita_id)
        
        # Test 3: Validación de solapamiento
        test_validacion_solapamiento()
        
        # Test 4: Listar todas las citas
        test_listar_todas_citas()
        
        print("\n" + "=" * 60)
        print("RESUMEN DE PRUEBAS COMPLETADO")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error general: {e}")
