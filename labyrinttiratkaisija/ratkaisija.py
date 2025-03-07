# labyrintit:
# 'S' on alku (Start).
# 'E' on loppu (End).
# '.' on kuljettavissa oleva tila.
# '#' on este.

# Labyrintinratkaisija Pythonilla (DFS)

# Funktio labyrintin lukemiseen tiedostosta
def lue_labyrintti(tiedosto):
    labyrintti = []
    with open(tiedosto, 'r', encoding='utf-8') as file:
        for rivi in file:
            labyrintti.append(list(rivi.strip()))
    return labyrintti

# Funktio, joka etsii ratkaisun labyrinttiin syvyyteen perustuvalla haulla (DFS)
def ratkaise_labyrintti(labyrintti):
    # Etsitään alku (S) ja loppu (E)
    alku = None
    loppu = None
    for i in range(len(labyrintti)):
        for j in range(len(labyrintti[i])):
            if labyrintti[i][j] == 'S':
                alku = (i, j)
            elif labyrintti[i][j] == 'E':
                loppu = (i, j)
    
    # Tarkistetaan, löytyikö alku ja loppu
    if alku is None or loppu is None:
        print("Alkua tai loppua ei löytynyt!")
        return None
    
    # Syvyyteen perustuva haku (DFS)
    visited = set()  # Käydyt solmut
    reitti = []      # Reitti, joka kuljetaan

    def dfs(x, y):
        # Jos ollaan ulkopuolella tai solmu on este, palataan
        if x < 0 or x >= len(labyrintti) or y < 0 or y >= len(labyrintti[0]) or labyrintti[x][y] == '#' or (x, y) in visited:
            return False
        visited.add((x, y))
        reitti.append((x, y))

        # Jos ollaan loppupisteessä, palataan True
        if (x, y) == loppu:
            return True
        
        # Liikutaan neljään suuntaan (ylös, alas, vasen, oikea)
        if (dfs(x - 1, y) or dfs(x + 1, y) or dfs(x, y - 1) or dfs(x, y + 1)):
            return True

        # Jos reitti ei johtanut loppuun, poistetaan solmu reitistä
        reitti.pop()
        return False

    # Käynnistetään DFS alkuperäisestä solmusta
    if dfs(alku[0], alku[1]):
        return reitti
    else:
        print("Ratkaisua ei löydy.")
        return None

# Funktio reitin tulostamiseen
def tulosta_reitti(reitti, labyrintti):
    if reitti is None:
        print("Ratkaisua ei löytynyt.")
        return

    for i in range(len(labyrintti)):
        for j in range(len(labyrintti[i])):
            if (i, j) in reitti:
                print('O', end=' ')  # Polku merkitään 'O':lla
            else:
                print(labyrintti[i][j], end=' ')  # Esteet ja tyhjät tilat alkuperäisinä
        print()

# Pääohjelma
if __name__ == '__main__':
    labyrintti = lue_labyrintti('labyrintit/labyrintti.txt')
    reitti = ratkaise_labyrintti(labyrintti)
    tulosta_reitti(reitti, labyrintti)

