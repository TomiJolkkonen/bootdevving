import feedparser

# Funktio, joka lukee RSS-syötteen ja hakee artikkeleiden tiedot
def lue_rss_syote(rss_url):
    syote = feedparser.parse(rss_url)
    artikkelit = []
    
    for entry in syote.entries:
        artikkelit.append({
            'otsikko': entry.title,
            'linkki': entry.link,
            'yhteenveto': entry.summary,
            'julkaisupäivämäärä': entry.published
        })
    
    return artikkelit

# Funktio HTML-sivun luomiseen
def luo_html_sivu(artikkelit):
    html = '''<html lang="fi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Blogiagreggointi</title>
</head>
<body>
    <header>
        <h1>Blogiagreggointi</h1>
    </header>
    <main>
        <ul>'''
    
    for artikkeli in artikkelit:
        html += f'''
            <li>
                <h2><a href="{artikkeli['linkki']}">{artikkeli['otsikko']}</a></h2>
                <p>{artikkeli['yhteenveto']}</p>
                <small>{artikkeli['julkaisupäivämäärä']}</small>
            </li>'''
    
    html += '''
        </ul>
    </main>
</body>
</html>'''
    
    return html

# Pääfunktio blogien yhdistämiseen ja HTML-sivun luomiseen
def aggregoi_blogit():
    # RSS-syötteet
    syotteet = [
        'syotteet/blogi1.rss',
        'syotteet/blogi2.rss'
    ]
    
    kaikki_artikkelit = []
    
    for syote in syotteet:
        artikkelit = lue_rss_syote(syote)
        kaikki_artikkelit.extend(artikkelit)  # Yhdistetään artikkelit
    
    # Järjestetään artikkelit julkaisupäivämäärän mukaan (uusin ensin)
    kaikki_artikkelit.sort(key=lambda x: x['julkaisupäivämäärä'], reverse=True)
    
    # Luodaan HTML-sivu
    html_sivu = luo_html_sivu(kaikki_artikkelit)
    
    # Tallenna HTML-sivu tiedostoon
    with open('blogi.html', 'w', encoding='utf-8') as file:
        file.write(html_sivu)
    
    print("Blogiagreggointisivu luotu tiedostoon 'blogi.html'.")

# Suorita blogiagreggointi
if __name__ == '__main__':
    aggregoi_blogit()
