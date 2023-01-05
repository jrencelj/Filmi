import sqlite3 as dbapi
from bralnik import Bralnik
import json
from bs4 import BeautifulSoup
import re
class Kinoteka:

    def __init__(self, ime, url):
        self._ime = ime
        self._url = url

    def shrani_kinoteka(self):
        '''Shrani kinoteko v bazo.'''
        conn = dbapi.connect('filmi.db') 
        with conn:
            conn.execute("""
            INSERT INTO kinoteka (ime, url)
            VALUES (?, ?)
            """, [self._ime, self._url])

    def pridobi_filme(self):
        '''Pridobi filme in jih shrani v json datoteko.'''
        kinoteke = {'HBO Max': 'hbo-max',
                    'Netflix': 'netflix',
                    'Disney+': 'disney-plus',
                    'SkyShowtime': 'skyshowtime'}
        kinoteka = kinoteke[self._ime]
        vsebina_kinoteka = dict()
        vsebina_kinoteka[kinoteka] = list()
        for leto in range(1900, 2023):
            odziv = Bralnik.pridobi_html(f'https://www.justwatch.com/si/ponudnik/{kinoteka}/filmi?release_year_from={leto}&release_year_until={leto}&rating_imdb=8')
            soup = BeautifulSoup(odziv, 'html.parser')
            slike = soup.find_all('picture', class_ = 'picture-comp title-poster__image')
            for slika in slike:
                regex_naslov = r'<img alt=\"([^\"]*)\"[^>]*>'
                img = slika.find_all('img')
                naslov = re.findall(regex_naslov, str(img))
                vsebina_kinoteka[kinoteka].append(naslov[0])
        with open(f'data/film/kinoteka/{kinoteka}.json', 'w', encoding = 'utf8') as f:
            json.dump(vsebina_kinoteka, f)

    def pridobi_serije(self):
        '''Pridobi serije in jih shrani v json datoteko.'''
        kinoteke = {'HBO Max': 'hbo-max',
                    'Netflix': 'netflix',
                    'Disney+': 'disney-plus',
                    'SkyShowtime': 'skyshowtime'}
        kinoteka = kinoteke[self._ime]
        vsebina_kinoteka = dict()
        vsebina_kinoteka[kinoteka] = list()
        for leto in range(1900, 2023):
            odziv = Bralnik.pridobi_html(f'https://www.justwatch.com/si/ponudnik/{kinoteka}/serije?release_year_from={leto}&release_year_until={leto}&rating_imdb=8.4')
            soup = BeautifulSoup(odziv, 'html.parser')
            slike = soup.find_all('picture', class_ = 'picture-comp title-poster__image')
            for slika in slike:
                regex_naslov = r'<img alt=\"([^\"]*)\"[^>]*>'
                img = slika.find_all('img')
                naslov = re.findall(regex_naslov, str(img))
                vsebina_kinoteka[kinoteka].append(naslov[0])
        with open(f'data/serija/kinoteka/{kinoteka}.json', 'w', encoding = 'utf8') as f:
            json.dump(vsebina_kinoteka, f)