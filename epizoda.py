from bs4 import BeautifulSoup
import requests
import json
import pandas as pd
import time
import re
from serija import Serija
from bralnik import Bralnik
from dopolni_igralci_filmi_serije import pridobi_reziserje_epizod

class Epizoda:
    
    def __init__(self, nadrejena_serija):
        if not isinstance(nadrejena_serija, Serija):
            raise Exception(f'{nadrejena_serija} ni objekt razreda Serija')
        else:
            self._nadrejena_serija = nadrejena_serija 
        pass
    
    def shrani_epizoda(self):
        '''Shrani epizodo v bazo.'''
        # TODO
        pass


def dodaj_reziserje(ime_serije):
    '''Pridobi režiserja epizode in ga doda ustrezni json datoteki serije.'''
    ime = Bralnik.preoblikuj_v_ime(ime_serije)
    with open(f'data/epizode/epizode_podrobno/{ime}.json', 'r') as f:
        vse_epizode = json.load(f)

    epizode_z_reziserji = dict()
    epizode_z_reziserji[ime_serije] = dict()
    for naslov_serija, epizode in vse_epizode.items():
        for epizoda_naslov, epizoda_podatki in epizode.items():
            imdb_id_epizode = epizoda_podatki['imdb_id']
            epizoda_podatki['Directors'] = pridobi_reziserje_epizod(imdb_id_epizode)
            epizode_z_reziserji[ime_serije][epizoda_naslov] = epizoda_podatki

    with open(f'data/epizode/epizode_podrobno/{ime}.json', 'w', encoding = 'utf8') as f:
        json.dump(epizode_z_reziserji, f)





def pridobi_html(url):
    """Pridobi html vsebino spletne strani."""
    odziv = requests.get(url, headers = {'Accept-Language': 'en-US,en;q=0.5', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6.1 Safari/605.1.15'})
    return odziv.text



def pridobi_epizode(vsebina) -> dict:
    """Prejme BeautifulSoup objekt. Pridobi naslov in imdb_id epizod na dani spletni strani in jih vrne v obliki slovarja."""
    rez = dict()
    epizode = vsebina.find('div', class_ = 'list detail eplist')
    linki = epizode.find_all('a', itemprop = 'name')
    regex_imdb_id = r'\/title\/([^\/]*)\/'
    for link in linki:
        naslov_epizode = link.contents[0]
        imdb_epizoda_id = re.findall(regex_imdb_id, link['href'])[0]
        rez[naslov_epizode] = imdb_epizoda_id
    return rez

def naslednja_sezona(vsebina):
    """Prejme BeautifulSoup objekt. Vrne link do naslednje sezone. Če naslednje sezone ni vrne None."""
    # TODO
    a_znacka = vsebina.find('a', id = 'load_next_episodes')
    if a_znacka is None:
        return None
    return a_znacka['href']

def zadnja_sezona(vsebina):
    """Vrne True če je sezona zadnja sezona. V nasprotnem primeru vrne False"""
    a_znacka = vsebina.find('a', id = 'load_next_episodes')
    if a_znacka is None:
        return True
    return False

def pridobi_vse_epizode_v2(imdb_id, sezona = 1) -> dict:
    """Glede na podan id serije, vrne vse naslove in pripadajoče id-je epizod."""
    vsebina = Bralnik.pridobi_html(f'https://www.imdb.com/title/{imdb_id}/episodes?season={sezona}')
    soup = BeautifulSoup(vsebina, "html.parser")
    if zadnja_sezona(soup):
        return pridobi_epizode(soup)
    return pridobi_epizode(soup) | pridobi_vse_epizode(imdb_id, sezona + 1)

def pridobi_vse_epizode(imdb_id, zacetek) -> dict:
    """Glede na podan id serije, vrne vse naslove in pripadajoče id-je epizod."""
    naslednja = f'?year={zacetek}'
    vsebina = Bralnik.pridobi_html(f'https://www.imdb.com/title/{imdb_id}/episodes{naslednja}')
    soup = BeautifulSoup(vsebina, 'html.parser')
    epizode = pridobi_epizode(soup)
    if not zadnja_sezona(soup):
        zastavica = False
        while True:
            if zastavica:
                break
            naslednja = naslednja_sezona(soup)
            vsebina = Bralnik.pridobi_html(f'https://www.imdb.com/title/{imdb_id}/episodes{naslednja}')
            soup = BeautifulSoup(vsebina, 'html.parser')
            epizode = epizode | pridobi_epizode(soup)
            if zadnja_sezona(soup):
                zastavica = not zastavica
    return epizode


if __name__ == '__main__':
    print('HELLO')
    with open('data/serija/serije.json', 'r') as f:
        serije = json.load(f)
    for naslov_serija, podatki_serija in serije.items():
        print(naslov_serija)
        dodaj_reziserje(naslov_serija)

    #with open('serije.json', 'r') as f:
    #    serije = json.load(f)
#
    #
    #epizode = dict()
    #for naslov, podatki in serije.items():
    #    print(naslov)
    #    leto_zacetka_predvanjanja = None if podatki['Released'] == 'N/A' else podatki['Released'].split()[-1]
    #    leto_zacetka = None if podatki['Year'] == 'N/A' else podatki['Year'][0:4]
    #    print(leto_zacetka)
    #    print(leto_zacetka_predvanjanja)
    #    imdb_id = podatki['imdbID']
    #    # Včasih se leti ne ujemata zato pogledamo oba in vrnemo tistega, ki vrne več epizod.
    #    ep_leto_zacetka = dict() if leto_zacetka == None else pridobi_vse_epizode(imdb_id, leto_zacetka)
    #    ep_leto_zacetka_predvajanja = dict() if leto_zacetka_predvanjanja == None else pridobi_vse_epizode(imdb_id, leto_zacetka_predvanjanja)
    #    ep = ep_leto_zacetka if len(ep_leto_zacetka) > len(ep_leto_zacetka_predvajanja) else ep_leto_zacetka_predvajanja
    #    epizode[naslov] = ep
    #    print(ep)
#
    #with open('epizode.json', 'w', encoding = 'utf-8') as f:
    #    json.dump(epizode, f)

    




