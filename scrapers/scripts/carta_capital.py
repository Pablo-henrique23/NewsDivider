import csv
from bs4 import BeautifulSoup
import cloudscraper
import threading

scraper = cloudscraper.create_scraper()

arquivo_csv = "dataset/cartacapital.csv"
base_url = "https://www.cartacapital.com.br/politica"

noticias = []
paginas = 10
total_noticias = 100
lock = threading.Lock()


def extrair_conteudo_noticia(url):
    try:
        res = scraper.get(url)
        if res.status_code != 200:
            print(f"[ERRO] {url}: {res.status_code}")
            return
        soup = BeautifulSoup(res.content, "html.parser")

        try:
            titulo = soup.find("h1").get_text(strip=True)
        except AttributeError:
            print(f'\033[31m[ERRO] em {url} cheque o titulo!!\033[m\n')
            return
        corpo = soup.find("div", class_="content-closed contentOpen")

        paragrafos = [p.get_text(strip=False) for p in corpo.find_all("p")]

        texto = "\n".join(paragrafos)

        if len(texto) == 0:
            del paragrafos
            paragrafos = [p.get_text(strip=False) for p in corpo.find_all("span", class_='cf0')]
            texto = "\n".join(paragrafos)
            
        if 'Senado aprova Wadih Damous para a presidência da ANS' in titulo:
            print(titulo)
            print(paragrafos)
            print(texto)
        # print(texto)
        
        # print(f'[PEGANDO] {titulo}')
        return {"titulo": titulo, "texto": texto, "url": url}

    except Exception as e:
        print(f"[ERRO] {url}: {e}")
        return {"titulo": titulo, "texto": texto, "url": url}
    

def proccess_page(pagina):
    url_pagina = base_url
    if pagina > 1:
        url_pagina = f"{base_url}/page/{pagina}/"

    res = scraper.get(url_pagina)

    if res.status_code != 200:
        print(f"[FIM] Página {pagina} não acessível. Encerrando.")
        return

    print(f"Scraping {url_pagina}")
    soup = BeautifulSoup(res.content, "html.parser")
    artigos = soup.find_all('a', class_='l-list__item')

    links = []
    for a in artigos:
        href = a.get("href")
        if href and href not in links:
            links.append(href)

    print(f'{url_pagina} -> {len(links)}')
    
    for link in links:
        with lock:
            if len(noticias) >= total_noticias:
                print(len(noticias))
                break
        noticia = extrair_conteudo_noticia(link)

        if noticia:
            with lock:
                noticias.append(noticia)


threads = []
for i in range(1, paginas + 1):
    t = threading.Thread(target=proccess_page, args=(i,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()


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
