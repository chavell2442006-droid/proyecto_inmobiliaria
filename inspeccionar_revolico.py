from pathlib import Path
from bs4 import BeautifulSoup

carpeta = Path("paginas_revolico")
archivos = sorted(carpeta.glob("*.html"))

archivo = archivos[0]

print("Analizando:", archivo.name)

with open(archivo, "r", encoding="utf-8", errors="ignore") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

enlaces = soup.find_all("a", href=True)

for enlace in enlaces:

    direccion = enlace.get("href", "")

    if "/item/" in direccion and "/item/publish" not in direccion:

        print("\nANUNCIO:")
        print(enlace.get_text(" ", strip=True))

        elemento = enlace

        for nivel in range(1, 7):

            elemento = elemento.parent

            if elemento is None:
                break

            enlaces_item = []

            for e in elemento.find_all("a", href=True):
                href = e.get("href", "")

                if "/item/" in href and "/item/publish" not in href:
                    enlaces_item.append(href)

            enlaces_unicos = set(enlaces_item)

            texto = elemento.get_text(" ", strip=True)

            print("\n" + "=" * 50)
            print("NIVEL:", nivel)
            print("ETIQUETA:", elemento.name)
            print("CLASES:", elemento.get("class"))
            print("ANUNCIOS DENTRO:", len(enlaces_unicos))
            print("LONGITUD DEL TEXTO:", len(texto))
            print("TEXTO:")
            print(texto[:700])

        break