# distancia_ciudades_graphhopper.py

import requests
from geopy.geocoders import Nominatim
import time

API_KEY = "c1b6d842-4f73-41b2-881c-264a06e2fb55"

TRANSPORTES = {
    "1": ("car", "Automóvil"),
    "2": ("bike", "Bicicleta"),
    "3": ("foot", "Caminando")
}

def obtener_coordenadas(ciudad):
    geolocator = Nominatim(user_agent="geoapi")
    location = geolocator.geocode(ciudad)
    if location:
        return (location.latitude, location.longitude)
    else:
        return None

def calcular_ruta(origen_coord, destino_coord, medio):
    url = "https://graphhopper.com/api/1/route"
    params = {
        "point": [f"{origen_coord[0]},{origen_coord[1]}", f"{destino_coord[0]},{destino_coord[1]}"],
        "vehicle": medio,
        "locale": "es",
        "key": API_KEY,
        "instructions": "true",
        "calc_points": "true"
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print("❌ Error en la API:", response.status_code, response.text)
        return None

def main():
    while True:
        print("\n=== Calculadora de Distancia entre Ciudades (GraphHopper) ===")
        print("Ingrese 's' para salir.")

        origen = input("Ciudad de origen: ")
        if origen.lower() == "s":
            break

        destino = input("Ciudad de destino: ")
        if destino.lower() == "s":
            break

        print("\nMedios de transporte disponibles:")
        for k, v in TRANSPORTES.items():
            print(f"{k}. {v[1]}")

        tipo = input("Seleccione el número del medio de transporte: ")
        if tipo.lower() == "s":
            break

        if tipo not in TRANSPORTES:
            print("Opción inválida.")
            continue

        vehiculo, medio_nombre = TRANSPORTES[tipo]

        origen_coord = obtener_coordenadas(origen + ", Chile")
        destino_coord = obtener_coordenadas(destino + ", Argentina")

        if not origen_coord or not destino_coord:
            print("❌ No se encontraron las coordenadas.")
            continue

        datos_ruta = calcular_ruta(origen_coord, destino_coord, vehiculo)

        if datos_ruta:
            path = datos_ruta["paths"][0]
            distancia_km = path["distance"] / 1000
            distancia_mi = distancia_km * 0.621371
            duracion_horas = path["time"] / 1000 / 3600

            print(f"\n📍 Ruta desde {origen} hasta {destino} en {medio_nombre}:")
            print(f"→ Distancia: {distancia_km:.2f} km / {distancia_mi:.2f} millas")
            print(f"→ Duración estimada: {duracion_horas:.2f} horas")

            print("\n🧭 Indicaciones:")
            for instr in path["instructions"]:
                print(f"- {instr['text']}")

        time.sleep(2)

if __name__ == "__main__":
    main()
