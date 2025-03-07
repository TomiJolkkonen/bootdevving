import os
import markdown

# Funktio, joka lukee pohjatiedoston ja korvataan muuttujat
def luo_html(pohjatiedosto, otsikko, sisalto):
    with open(pohjatiedosto, 'r', encoding='utf-8') as file:
        pohja = file.read()
    
    # Korvataan muuttujat
    html = pohja.replace("{{otsikko}}", otsikko).replace("{{sisalto}}", sisalto)
    
    return html

# Funktio, joka lukee markdown-tiedoston ja muuntaa sen HTML:ksi
def lue_markdown(sisalto_tiedosto):
    with open(sisalto_tiedosto, 'r', encoding='utf-8') as file:
        markdown_sisalto = file.read()
    
    # Muunnetaan Markdown HTML:ksi
    html_sisalto = markdown.markdown(markdown_sisalto)
    
    return html_sisalto

# Pääfunktio, joka generoi kaikki sivut
def generoi_sivut():
    sisallot_kansio = 'sisallot'
    pohja_tiedosto = 'pohjat/pohja.html'
    generoitu_kansio = 'generoitu'

    # Varmistetaan, että generoitu-kansio on olemassa
    if not os.path.exists(generoitu_kansio):
        os.makedirs(generoitu_kansio)

    # Käydään kaikki Markdown-tiedostot läpi
    for tiedosto in os.listdir(sisallot_kansio):
        if tiedosto.endswith('.md'):
            tiedosto_polku = os.path.join(sisallot_kansio, tiedosto)
            
            # Lue Markdown-tiedosto ja muunna se HTML:ksi
            sisalto_html = lue_markdown(tiedosto_polku)

            # Otsikko löytyy Markdown-tiedostosta
            otsikko = "Tuntematon otsikko"
            with open(tiedosto_polku, 'r', encoding='utf-8') as file:
                eka_rivi = file.readline()
                otsikko = eka_rivi.replace('Otsikko: ', '').strip()
            
            # Luo HTML-tiedosto pohjasta ja korvataan sisältö
            html_sivu = luo_html(pohja_tiedosto, otsikko, sisalto_html)

            # Tallenna generoitu HTML-tiedosto
            generoitu_tiedosto = os.path.join(generoitu_kansio, tiedosto.replace('.md', '.html'))
            with open(generoitu_tiedosto, 'w', encoding='utf-8') as file:
                file.write(html_sivu)
            print(f'{generoitu_tiedosto} luotu.')

# Suorita generaattori
if __name__ == '__main__':
    generoi_sivut()
