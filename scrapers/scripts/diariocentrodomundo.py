import cloudscraper
import csv
from bs4 import BeautifulSoup

arquivo_csv = "dataset/diariocentrodomundo.csv"
base_url = 'https://www.brasil247.com'
total_noticias = 100
html = ''
with open('scripts/diario.html', mode='r', encoding='utf-8') as f:
    html = f.read()


scraper = cloudscraper.create_scraper()
def extrair_conteudo_noticia(url):
    url = base_url+url
    try:
        res = scraper.get(url)
        soup = BeautifulSoup(res.content, "html.parser")
        
        titulo = soup.find("h1", class_='article__headline').get_text(strip=True)
        
        corpo = soup.find("div", attrs={"data-cy": "articleBody"})
        paragrafos = []

        for p in corpo.find_all("p"):
            first_tag = next((child for child in p.children if child.name), None)

            if first_tag and first_tag.name.lower() == "strong":
                continue  # pula esse <p>, pq o filho dele é o auto

            texto = p.get_text(strip=False).replace('\n', '')
            paragrafos.append(texto)

        texto = "\n".join(paragrafos)
        #print(f"[OK] {titulo}")
        return {"titulo": titulo, "texto": texto, "url": url}
    except Exception as e:
        #print(f"[ERRO] {url}: {e}")
        return {}
    

soup = BeautifulSoup(html, "html.parser")
noticias = []
for noticia in soup.find_all('article', class_='artGrid artGrid--small grid__item grid__item--col-12 gi-medium-4'):
    href = noticia.find('a').get('href')

    if href and href not in noticias:
        noticias.append(href)

    if len(noticias) >= total_noticias:
        break

#print(f'Noticias scrapadas: {len(noticias)}')

n = []
for i, noticia in enumerate(noticias):
    n.append(extrair_conteudo_noticia(noticia))

with open(arquivo_csv, mode="w+", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["id", "titulo", "corpo"])
    cont = 0
    for i, noticia in enumerate(n):
        try:
            writer.writerow([i, noticia["titulo"], noticia["texto"]])
            cont += 1
        except TypeError:
            #print(f'[ERRO] em {noticia}!!!')
            pass
            
    #print(f"CSV contém {cont} itens")
