import json, os, re
from urllib.request import Request, urlopen
from urllib.parse import urlparse

BASE = 'https://gostec.com'
UA = {'User-Agent':'Mozilla/5.0'}

SLUGS = [
    'software','servizi','grafica-aziendale','gostec-academy','noleggi','mailnews','statistiche','x360cloud-backup','internet-professional','setup-della-posta','setup-accesso-internet','connettiti-a-gostec','siti-e-web-design','siti-e-commerce','i-portali','web-hosting','data-center','la-pec-di-gostec','soluzione-web-activity','forniture','servizi-e-sistemi','cablaggi-e-networking','assistenza-tecnica','assistenza-sistemistica','consulenza-e-adeguamenti-legge-privacy','privacy-e-sicurezza-dei-dati','la-nostra-storia','info-su-gostec','visione-e-filosofia-aziendali','etica-e-impegno-sociale','info-su-stefano-cherchi','il-marchio','cerchiamo-personale','tirocini-e-convenzioni','il-team-gostec','mappa','contattaci','info-legali-e-copyright','privacy-policy'
]


def fetch_json(url):
    req = Request(url, headers=UA)
    return json.loads(urlopen(req, timeout=30).read().decode('utf-8', 'ignore'))

home = fetch_json(f'{BASE}/wp-json/wp/v2/pages/1987')
pages = [{'slug':'', 'title':home['title']['rendered'], 'content':home['content']['rendered']}]
for slug in SLUGS:
    arr = fetch_json(f'{BASE}/wp-json/wp/v2/pages?slug={slug}')
    if not arr:
        print('missing',slug)
        continue
    p = arr[0]
    pages.append({'slug':slug, 'title':p['title']['rendered'], 'content':p['content']['rendered']})

nav = [('Home','/')] + [(p['title'], f"/{p['slug']}/") for p in pages if p['slug']][:12]
nav_html = ''.join([f'<a href="{href}">{title}</a>' for title,href in nav])

tpl = '''<!DOCTYPE html>
<html lang="it">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title} | GoStec</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/styles.css" />
</head>
<body>
  <header class="site-header">
    <div class="container header-inner">
      <a class="brand" href="/">GoStec</a>
      <button class="menu-toggle" aria-label="Open menu">☰</button>
      <nav class="menu">{nav}</nav>
    </div>
  </header>
  <main>
    <section class="hero container">
      <p class="eyebrow">Innovazione digitale</p>
      <h1>{title}</h1>
      <p>Contenuti originali del sito GoStec, presentati con una nuova esperienza moderna e fluida.</p>
    </section>
    <section class="content container">
      <article class="legacy-content">{content}</article>
    </section>
  </main>
  <footer class="site-footer">
    <div class="container">© GoStec</div>
  </footer>
  <script src="/script.js"></script>
</body>
</html>'''

for p in pages:
    outdir = '.' if p['slug']=='' else p['slug']
    os.makedirs(outdir, exist_ok=True)
    outfile = 'index.html' if p['slug']=='' else f'{outdir}/index.html'
    with open(outfile,'w',encoding='utf-8') as f:
        f.write(tpl.format(title=p['title'], content=p['content'], nav=nav_html))

print('generated',len(pages),'pages')
