# test_insertar_dicotomico.py
import sys
import os

if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from fastapi.testclient import TestClient
from src.api.app import app

client = TestClient(app)

print("=" * 70)
print("🧪 PRUEBA END-TO-END: INSERCIÓN DE ESPECIE Y VERIFICACIÓN EN MOTOR DICOTÓMICO")
print("=" * 70)

# 1. Crear una nueva especie mediante POST /api/especies
nueva_especie_payload = {
    "nombre_cientifico": "Porites roques_filiformis",
    "nombre_comun": "Coral Dedo Filiforme de Los Roques",
    "familia": "Poritidae",
    "orden": "Scleractinia",
    "tipo": "Escleractinio",
    "descripcion": "Especie endémica descubierta durante expedición en Los Roques",
    "habitat": "Zona somera de arrecife de barrera en Los Roques",
    "caracteristicas": {
        "tiene_coralitos": True,
        "forma": "ramificada_conica",
        "numero_septos": 10,
        "superficie": "copas"
    }
}

print(f"\n1. 🪸 Insertando nueva especie vía API POST /api/especies...")
print(f"   Nombre Científico: {nueva_especie_payload['nombre_cientifico']}")
print(f"   Nombre Común: {nueva_especie_payload['nombre_comun']}")
print(f"   Familia: {nueva_especie_payload['familia']}")

res_post = client.post("/api/especies", json=nueva_especie_payload)

if res_post.status_code == 200:
    data_post = res_post.json()
    print(f"   ✅ Éxito al insertar en la Base de Conocimientos:")
    print(f"      ID Generado: {data_post['especie']['id']}")
    print(f"      Mensaje: {data_post['mensaje']}")
elif res_post.status_code == 400:
    print(f"   ℹ️  La especie ya existía en la base de datos (Validación de duplicados OK).")
else:
    print(f"   ❌ Error al insertar: Status {res_post.status_code} - {res_post.text}")

# 2. Ejecutar inferencia en el Motor Dicotómico con el patrón dinámico de la especie
respuestas_cuestionario = {
    "p1": "s",
    "p4": "colonial",
    "p6": "ramificado",
    "p7": "toda",
    "p10": "conicas",
    "p14": "10"
}

print(f"\n2. ⚙️  Probando acceso en el Motor Dicotómico (Cuestionario Guiado)...")
print(f"   Respuestas del cuestionario enviadas: {respuestas_cuestionario}")

res_inferencia = client.post("/api/inferencia/paso", json={"respuestas": respuestas_cuestionario})

if res_inferencia.status_code == 200:
    data_inf = res_inferencia.json()
    print(f"\n3. 🏆 RESPUESTA DEL MOTOR DICOTÓMICO:")
    print(f"   Estado del Motor: {data_inf.get('estado')}")
    print(f"   Éxito: {'✅ Sí' if data_inf.get('success') else '❌ No'}")
    print(f"   Especie Identificada: {data_inf.get('especie')}")
    print(f"   Nombre Común: {data_inf.get('nombre_comun')}")
    print(f"   Familia Taxonómica: {data_inf.get('familia')}")
else:
    print(f"   ❌ Error en el motor de inferencia: Status {res_inferencia.status_code} - {res_inferencia.text}")

print("=" * 70)
