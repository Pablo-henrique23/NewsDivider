import cloudscraper
from bs4 import BeautifulSoup
import csv
from time import sleep
import threading

# Criando o scraper com headers personalizados
scraper = cloudscraper.create_scraper()


arquivo_csv = "../dataset/jovempan.csv"
base_url = "https://jovempan.com.br/noticias/politica"

noticias = []
paginas = 10
total_noticias = 100
lock = threading.Lock()


def extrair_conteudo_noticia(url):
    try:
        res = scraper.get(url)
        sleep(0.2)
        print(res.status_code)
        soup = BeautifulSoup(res.content, "html.parser")

        try:
            titulo = soup.find("h1", class_='post-title').get_text(strip=True)
        except AttributeError:
            print(f'[ERRO] em {url} cheque o titulo!!\n')
            return
        corpo = soup.find("div", class_="context")
        paragrafos = [p.get_text(strip=True) for p in corpo.find_all("p")]
        texto = "\n".join(paragrafos)

        return {"titulo": titulo, "texto": texto, "url": url}
    except Exception as e:
        print(f"[ERRO] {url}: {e}")
        return {"titulo": titulo, "texto": texto, "url": url}


def proccess_page(pagina):
    
    url_pagina = base_url
    if pagina > 1:
        url_pagina = f"{base_url}/page/{pagina}/"

    res = scraper.get(url_pagina)
    sleep(0.2)

    if res.status_code != 200:
        print(f"[FIM] Página {pagina} não acessível. Encerrando.")
        return

    soup = BeautifulSoup(res.content, "html.parser")
    artigos = soup.find_all('article')
    
    #print(artigos)
    links = []
    for artigo in artigos:
        a = artigo.find('a')
        href = a.get("href")
        print(href)
        if href and href not in links:
            links.append(href)

    for link in links:
        print(link)
        with lock:
            if len(noticias) >= total_noticias:
                break
        noticia = extrair_conteudo_noticia(link)
        if noticia:
            with lock:
                noticias.append(noticia)
                print(f"[OK] {noticia['titulo']}")


# Iniciando as threads
threads = []
for i in range(1, paginas + 1):
    t = threading.Thread(target=proccess_page, args=(i,))
    t.start()
    threads.append(t)

# Esperar todas as threads terminarem
for t in threads:
    t.join()
#print(noticias)
print(f"\nTotal coletado: {len(noticias)} notícias")

# Exemplo de saída
for i, n in enumerate(noticias):
    print(f"\n--- Notícia {i} ---")
    print(f"Título: {n['titulo']}")
    print(f"Texto: {n['texto']}")

print(f"\nTotal coletado: {len(noticias)} notícias")

with open(arquivo_csv, mode="w", newline="", encoding="utf-8") as f:
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