import requests
from bs4 import BeautifulSoup

url = "https://www.revolico.com/search?category=inmobiliaria&subcategory=inmobiliaria-casas&province=la-habana"

headers = {
    "User-Agent": "Mozilla/5.0"
}

respuesta = requests.get(url, headers=headers, timeout=20)

print("Estado de la página:", respuesta.status_code)
print("Cantidad de caracteres recibidos:", len(respuesta.text))

soup = BeautifulSoup(respuesta.text, "html.parser")

if soup.title:
    print("Título de la página:", soup.title.get_text(strip=True))
else:
    print("No encontré título.")