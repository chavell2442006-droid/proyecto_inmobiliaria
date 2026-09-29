import pandas as pd
datos = {"municipio": ["Playa","Vedado","Centro Habana"],
"precio": [95000, 120000, 75000],
"habitaciones": [3, 4, 2]}

viviendas = pd.DataFrame(datos)

print(viviendas)

print("\nCantidad de viviendas:")
print(len(viviendas))

print("\nPrecio promedio:")
print(viviendas["precio"].mean())

print("\nSolo los precios:")
print(viviendas["precio"])

print("\nPrecio máximo:")
print(viviendas["precio"].max())

print("\nPrecio mínimo:")
print(viviendas["precio"].min())

print("\nViviendas con precio mayor de 90000:")
caras = viviendas[viviendas["precio"] > 90000]
print(caras)

print("\nTamaño de la tabla:")
print(viviendas.shape)

print("\nNombres de las columnas:")
print(viviendas.columns)

print("\nViviendas de Playa:")
playa = viviendas[viviendas["municipio"] == "Playa"]
print(playa)

print("\nPrimeras 2 viviendas:")
print(viviendas.head(2))

print("\nGuardando datos en CSV...")

viviendas.to_csv("viviendas.csv", index=False)

print("Archivo viviendas.csv guardado correctamente.")

print("\nLeyendo el archivo CSV...")

datos_guardados = pd.read_csv("viviendas.csv")

print(datos_guardados)

print("\n--- EJEMPLO DE DATOS SUCIOS ---")

datos_sucios = {
    "municipio": ["Playa", "Vedado", "Playa", "Centro Habana"],
    "precio": [95000, 120000, 95000, None],
    "habitaciones": [3, 4, 3, 2]
}

viviendas_sucias = pd.DataFrame(datos_sucios)

print(viviendas_sucias)

print("\nDatos faltantes por columna:")
print(viviendas_sucias.isna().sum())

print("\nEliminando duplicados...")
sin_duplicados = viviendas_sucias.drop_duplicates()
print(sin_duplicados)

print("\nEliminando viviendas sin precio...")
viviendas_limpias = sin_duplicados.dropna(subset=["precio"])
print(viviendas_limpias)

viviendas_limpias.to_csv("viviendas_limpias.csv", index=False)

print("\nArchivo viviendas_limpias.csv guardado.")

print("\n--- NORMALIZACIÓN DE MUNICIPIOS ---")

datos_texto = {
    "municipio": ["Playa", "playa", " PLAYA ", "Centro Habana", "centro habana"],
    "precio": [95000, 87000, 110000, 75000, 82000]
}

ejemplo_normalizacion = pd.DataFrame(datos_texto)

print("\nANTES de normalizar:")
print(ejemplo_normalizacion)

ejemplo_normalizacion["municipio"] = (
    ejemplo_normalizacion["municipio"]
    .str.strip()
    .str.title()
)

print("\nDESPUÉS de normalizar:")
print(ejemplo_normalizacion)

print("\nMunicipios diferentes encontrados:")
print(ejemplo_normalizacion["municipio"].unique())

import json

print("\n--- EJEMPLO DE JSON ---")

anuncio = {
    "tipo": "Apartamento",
    "operacion": "Venta",
    "precio": 95000,
    "moneda": "USD",
    "municipio": "Playa",
    "habitaciones": 3,
    "banos": 2
}

print("\nDiccionario de Python:")
print(anuncio)

with open("anuncio.json", "w", encoding="utf-8") as archivo:
    json.dump(anuncio, archivo, ensure_ascii=False, indent=4)

print("\nArchivo anuncio.json guardado correctamente.")