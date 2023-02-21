import sqlite3 as dbapi
from bralnik import Bralnik
import json
from bs4 import BeautifulSoup
import re


class Kinoteka:

    def __init__(self, id, naziv_kinoteka, url_kinoteka):
        self._id = id
        self._naziv_kinoteka = naziv_kinoteka
        self._url_kinoteka = url_kinoteka

    def shrani_kinoteka(self):
        """Shrani kinoteko v bazo."""
        conn = dbapi.connect("filmi.db")
        with conn:
            conn.execute("""
            INSERT INTO kinoteka (naziv_kinoteka, url_kinoteka)
            VALUES (?, ?)
            """, [self._naziv_kinoteka, self._url_kinoteka])

    def pridobi_kinoteka_id(self):
        '''Pridobi id kinoteke iz baze'''
        conn = dbapi.connect('filmi.db')
        with conn:
            cursor = conn.execute("""
                SELECT id FROM kinoteka
                WHERE naziv_kinoteka=?
            """, [self._naziv_kinoteka])
            id = cursor.fetchone()[0]
            return id

    def pridobi_filme(self):
        '''Pridobi filme in jih shrani v json datoteko.'''
        kinoteke = {'HBO Max': 'hbo-max',
                    'Netflix': 'netflix',
                    'Disney+': 'disney-plus',
                    'SkyShowtime': 'skyshowtime'}
        kinoteka = kinoteke[self._naziv_kinoteka]
        vsebina_kinoteka = dict()
        vsebina_kinoteka[kinoteka] = list()
        for leto in range(1900, 2023):
            odziv = Bralnik.pridobi_html(
                f'https://www.justwatch.com/si/ponudnik/{kinoteka}/filmi?release_year_from={leto}&release_year_until={leto}&rating_imdb=8')
            soup = BeautifulSoup(odziv, 'html.parser')
            slike = soup.find_all(
                'picture', class_='picture-comp title-poster__image')
            for slika in slike:
                regex_naslov = r'<img alt=\"([^\"]*)\"[^>]*>'
                img = slika.find_all('img')
                naslov = re.findall(regex_naslov, str(img))
                vsebina_kinoteka[kinoteka].append(naslov[0])
        with open(f'data/film/kinoteka/{kinoteka}.json', 'w', encoding='utf8') as f:
            json.dump(vsebina_kinoteka, f)

    def pridobi_serije(self):
        '''Pridobi serije in jih shrani v json datoteko.'''
        kinoteke = {'HBO Max': 'hbo-max',
                    'Netflix': 'netflix',
                    'Disney+': 'disney-plus',
                    'SkyShowtime': 'skyshowtime'}
        kinoteka = kinoteke[self._naziv_kinoteka]
        vsebina_kinoteka = dict()
        vsebina_kinoteka[kinoteka] = list()
        for leto in range(1900, 2023):
            odziv = Bralnik.pridobi_html(
                f'https://www.justwatch.com/si/ponudnik/{kinoteka}/serije?release_year_from={leto}&release_year_until={leto}&rating_imdb=8.4')
            soup = BeautifulSoup(odziv, 'html.parser')
            slike = soup.find_all(
                'picture', class_='picture-comp title-poster__image')
            for slika in slike:
                regex_naslov = r'<img alt=\"([^\"]*)\"[^>]*>'
                img = slika.find_all('img')
                naslov = re.findall(regex_naslov, str(img))
                vsebina_kinoteka[kinoteka].append(naslov[0])
        with open(f'data/serija/kinoteka/{kinoteka}.json', 'w', encoding='utf8') as f:
            json.dump(vsebina_kinoteka, f)

    
    @staticmethod
    def pridobi_id_kinoteka_po_naziv(naziv):
        conn = dbapi.connect("filmi.db")
        with conn:
            cursor = conn.execute("""
                SELECT id FROM kinoteka WHERE naziv_kinoteka=?
            """, [naziv])
            id = cursor.fetchone()[0]
        return id 
    
    @property
    def id(self):
        return self._id
            
    @property
    def naziv_kinoteka(self):
        return self._naziv_kinoteka

    @property
    def url_kinoteka(self):
        return self._url_kinoteka

    @id.setter
    def id(self, vrednost):
        self._id = vrednost

    @naziv_kinoteka.setter
    def ime(self, vrednost):
        self._naziv_kinoteka = vrednost

    @url_kinoteka.setter
    def url(self, vrednost):
        self._url_kinoteka = vrednost
