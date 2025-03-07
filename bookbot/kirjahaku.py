import json
import os

# Luo kansio, jos se ei ole olemassa
kansio = 'kirjat'
if not os.path.exists(kansio):
    os.makedirs(kansio)

# Tiedoston polku
TIEDOSTO_POLKU = 'kirjat/kirjatiedot.json'  # Oikea polku

# Funktio kirjan lisäämiseen
def lisaa_kirja(nimi, kirjailija, julkaisuvuosi, sisalto):
    # Luodaan kirja sanakirjana
    uusi_kirja = {
        'nimi': nimi,
        'kirjailija': kirjailija,
        'julkaisuvuosi': julkaisuvuosi,
        'sisalto': sisalto
    }

    try:
        # Avaa tiedosto luku- ja kirjoitustilassa
        with open(TIEDOSTO_POLKU, 'r+') as tiedosto:
            # Lue nykyiset kirjat tiedostosta
            kirjat = json.load(tiedosto)
            # Lisää uusi kirja listalle
            kirjat.append(uusi_kirja)
            # Siirrä tiedoston luku- ja kirjoituskurssi alkuun
            tiedosto.seek(0)
            # Kirjoita kaikki kirjat takaisin tiedostoon
            json.dump(kirjat, tiedosto, indent=4)
    except FileNotFoundError:
        # Jos tiedostoa ei löydy, luodaan uusi tiedosto ja lisätään kirja
        with open(TIEDOSTO_POLKU, 'w') as tiedosto:
            json.dump([uusi_kirja], tiedosto, indent=4)

# Funktio kirjojen hakemiseen kirjailijan nimellä
def hae_kirjat_kirjailijalta(kirjailija):
    try:
        with open(TIEDOSTO_POLKU, 'r') as tiedosto:
            kirjat = json.load(tiedosto)
            # Etsitään kaikki kirjailijan kirjat
            palautettavat_kirjat = [kirja for kirja in kirjat if kirja['kirjailija'] == kirjailija]
            return palautettavat_kirjat
    except FileNotFoundError:
        return []

# Lue kirjan teksti tiedostosta
def lue_kirja_tiedostosta(tiedostopolku):
    with open(tiedostopolku, 'r', encoding='utf-8') as tiedosto:
        return tiedosto.read()

# Esimerkki kirjan lisäämisestä
try:
    kirjan_sisalto = lue_kirja_tiedostosta('pride_and_prejudice.txt')
    lisaa_kirja('Pride and Prejudice', 'Jane Austen', 1813, kirjan_sisalto)
except Exception as e:
    print(f"Virhe: {e}")

# Esimerkki kirjojen hakemisesta
kirjailijan_kirjat = hae_kirjat_kirjailijalta('Jane Austen')
for kirja in kirjailijan_kirjat:
    print(f'Nimi: {kirja["nimi"]}, Julkaisuvuosi: {kirja["julkaisuvuosi"]}')
