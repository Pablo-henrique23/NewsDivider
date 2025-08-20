import csv
from bs4 import BeautifulSoup
import cloudscraper

scraper = cloudscraper.create_scraper()

arquivo_csv = "dataset/cartacapital.csv"
base_url = "https://www.cartacapital.com.br/politica/"

noticias = []
pagina = 1
total_noticias = 100


def extrair_conteudo_noticia(url):
    try:
        res = scraper.get(url)
        soup = BeautifulSoup(res.content, "html.parser")

        try:
            titulo = soup.find("h1").get_text(strip=True)
        except AttributeError:
            print(f'\033[31m[ERRO] em {url} cheque o titulo!!\033[m\n')
            return
        
        corpo = soup.find("div", class_="content-closed contentOpen")
        try:
            paragrafos = [p.get_text(strip=False) for p in corpo.find_all("p", class_='pf0')]
        except AttributeError:
            return None
        if len(paragrafos) == 0:
            del paragrafos
            paragrafos = [p.get_text(strip=False) for p in corpo.find_all("span", class_='cf0')]
            return
        texto = "\n".join(paragrafos)
        # print(texto)
        
        return {"titulo": titulo, "texto": texto, "url": url}

    except Exception as e:
        print(f"[ERRO] {url}: {e}")
        return {"titulo": titulo, "texto": texto, "url": url}


while len(noticias) < total_noticias:

    url_pagina = f"{base_url}/"
    if pagina > 1:
        url_pagina = f"{base_url}/page/{pagina}/"

    res = scraper.get(url_pagina)

    if res.status_code != 200:
        print(f"[FIM] Página {pagina} não acessível. Encerrando.")
        break

    soup = BeautifulSoup(res.content, "html.parser")
    artigos = soup.find_all('a', class_='l-list__item')

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

    pagina += 1

print(f"\nTotal coletado: {len(noticias)} notícias")

with open(arquivo_csv, mode="w+", newline="", encoding="utf-8") as f:
    
    writer = csv.writer(f)
    writer.writerow(["id", "titulo", "corpo"])
    cont = 0 
    for i, noticia in enumerate(noticias):
        try:
            writer.writerow([i, noticia["titulo"], noticia["texto"]])
            cont += 1
        except:
            print(f'[ERRO] em {noticia}!!!')
    
    print(f"CSV contém {cont} itens")
