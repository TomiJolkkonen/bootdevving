import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin

# Funktio, joka lataa ja jäsentää verkkosivun
def lataa_sivu(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Heittää virheen, jos sivu ei vastaa oikein
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Virhe ladattaessa sivua {url}: {e}")
        return None

# Funktio, joka etsii kaikki linkit sivulta
def hae_linkit(sivu_html, sivu_url):
    soup = BeautifulSoup(sivu_html, 'html.parser')
    linkit = []

    # Etsitään kaikki <a> tagit ja kerätään href-attribuutit
    for a_tag in soup.find_all('a', href=True):
        linkki = a_tag['href']
        
        # Käytetään urljoinia yhdistämään suhteelliset URL:t täyteen URL:iin
        linkit.append(urljoin(sivu_url, linkki))

    return linkit

# Funktio, joka suorittaa crawlauksen
def crawl(sivut, max_sivut=10):
    vierailtu_sivut = set()  # Tallennetaan vierailtuja sivuja
    linkit_jonossa = list(sivut)  # Alkuperäinen URL-osoite lista
    tulokset = []

    while linkit_jonossa and len(vierailtu_sivut) < max_sivut:
        url = linkit_jonossa.pop(0)  # Otetaan ensimmäinen linkki jonosta
        if url not in vierailtu_sivut:
            print(f"Vieraillaan sivulla: {url}")
            vierailtu_sivut.add(url)
            sivu_html = lataa_sivu(url)
            
            if sivu_html:
                # Etsitään linkit sivulta ja liitetään suhteelliset linkit täydellisiin URL:ihin
                linkit = hae_linkit(sivu_html, url)
                tulokset.append(f"Linkit sivulta {url}:")
                tulokset.extend(linkit)
                tulokset.append("")  # Tyhjä rivi erottelemaan eri sivuja
                
                # Lisää löydetyt linkit jonoon (ilman duplikaatteja)
                for linkki in linkit:
                    if linkki not in vierailtu_sivut and linkki not in linkit_jonossa:
                        linkit_jonossa.append(linkki)

            # Odotetaan vähän ennen seuraavaa pyyntöä, jotta ei kuormiteta palvelinta
            time.sleep(1)

    return tulokset

# Pääfunktio, joka kutsuu crawl-funktiota ja tallentaa tulokset tiedostoon
def tallenna_tulokset(tulokset):
    with open("tulokset.txt", "w", encoding="utf-8") as f:
        for rivi in tulokset:
            f.write(rivi + "\n")
    print("Crawlauksen tulokset tallennettu tiedostoon 'tulokset.txt'.")

# Pääohjelma
if __name__ == "__main__":
    aloitus_url = "http://quotes.toscrape.com"  # Käytetään Quotes to Scrape -sivustoa
    tulokset = crawl([aloitus_url], max_sivut=10)  # Max 10 sivua
    tallenna_tulokset(tulokset)
