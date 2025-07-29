import cloudscraper
from bs4 import BeautifulSoup
import time

# Criando o scraper com headers personalizados
scraper = cloudscraper.create_scraper()


base_url = "https://oantagonista.com.br/brasil"

def extrair_conteudo_noticia(url):
    try:
        res = scraper.get(url)
        soup = BeautifulSoup(res.content, "html.parser")

        titulo = soup.find("h1", class_='p-name').get_text(strip=True)
        

        corpo = soup.find("div", class_="post-interna__content__corpo")
        paragrafos = [p.get_text(strip=True) for p in corpo.find_all("p")]
        texto = "\n".join(paragrafos)

        return {"titulo": titulo, "texto": texto, "url": url}
    except Exception as e:
        print(f"[ERRO] {url}: {e}")
        return {"titulo": titulo, "texto": texto, "url": url}

noticias = []
pagina = 1
total_noticias = 100

while len(noticias) < total_noticias:
    print(f"[INFO] Página {pagina}")
    url_pagina = f"{base_url}/"
    if pagina > 1:
        url_pagina = f"{base_url}/page/{pagina}/"

    res = scraper.get(url_pagina)

    if res.status_code != 200:
        print(f"[FIM] Página {pagina} não acessível. Encerrando.")
        break

    soup = BeautifulSoup(res.content, "html.parser")
    artigos = soup.find_all('a', class_='ultimas-noticias-area__link')

    links = []
    for a in artigos:
        href = a.get("href")
        if href and href not in links:
            links.append(href)

    for link in links:
        if len(noticias) >= total_noticias:
            break
        noticia = extrair_conteudo_noticia(link)
        if noticia:
            noticias.append(noticia)
            print(f"[OK] {noticia['titulo']}")
            time.sleep(1)

    pagina += 1

print(f"\nTotal coletado: {len(noticias)} notícias")

# Exemplo de saída
for i, n in enumerate(noticias):
    print(f"\n--- Notícia {i} ---")
    print(f"Título: {n['titulo']}")
    print(f"Texto: {n['texto']}")
