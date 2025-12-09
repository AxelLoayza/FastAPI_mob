import requests
import json

BASE_URL = "https://fastapi-mob.onrender.com"

# Crear una cita nueva con servicio y duración
payload = {
    "id_barbero": 1,
    "fecha": "2025-12-16",
    "hora": "10:00:00",
    "estado": "pendiente",
    "servicio": "Corte Premium",
    "duracion_minutos": 45
}

print("=== Creando cita nueva con servicio y duración ===")
print(f"Request: {json.dumps(payload, indent=2)}")

response = requests.post(
    f"{BASE_URL}/citas/?usuario_id=1",
    json=payload
)

print(f"\nStatus Code: {response.status_code}")
print(f"Response:\n{json.dumps(response.json(), indent=2)}")

if response.status_code in [200, 201]:
    cita = response.json()
    print("\n✅ RESULTADO:")
    print(f"  - servicio: {'✅ PRESENTE' if 'servicio' in cita else '❌ FALTANTE'} = {cita.get('servicio')}")
    print(f"  - duracion_minutos: {'✅ PRESENTE' if 'duracion_minutos' in cita else '❌ FALTANTE'} = {cita.get('duracion_minutos')}")
