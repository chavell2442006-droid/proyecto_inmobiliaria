from pathlib import Path
from bs4 import BeautifulSoup

carpeta = Path("paginas_revolico")
archivos = sorted(carpeta.glob("*.html"))

archivo = archivos[0]

print("Analizando:", archivo.name)

with open(archivo, "r", encoding="utf-8", errors="ignore") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

print("\n--- INFORMACIÓN GENERAL ---")
print("Tamaño del HTML:", len(html))
print("Cantidad de scripts:", len(soup.find_all("script")))

terminos = [
    "__NEXT_DATA__",
    "habitaciones",
    "habitacion",
    "cuartos",
    "bathroom",
    "bedroom",
    "municipio",
    "municipality",
    "location",
    "price",
    "precio"
]

print("\n--- BUSCANDO TÉRMINOS ---")

html_minusculas = html.lower()

for termino in terminos:

    cantidad = html_minusculas.count(termino.lower())

    print(termino, "->", cantidad)


print("\n--- SCRIPTS GRANDES ---")

scripts = soup.find_all("script")

for numero, script in enumerate(scripts):

    contenido = script.string

    if contenido and len(contenido) > 1000:

        print(
            "Script",
            numero,
            "- caracteres:",
            len(contenido)
        )

        print(contenido[:500])

        print("\n" + "-" * 70)