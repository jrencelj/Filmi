from bralnik import Bralnik
from bs4 import BeautifulSoup
import re
import time
import sqlite3 as dbapi


class KomentarIMDB:

    def __init__(self, imdb_id_komentar, imdb_id_uporabnik, naslov_komentarja, komentar, imdb_uporabnik, datum,
                 se_strinja, se_ne_strinja, ocena):
        self._imdb_id_komentar = imdb_id_komentar
        self._imdb_id_uporabnik = imdb_id_uporabnik
        self._naslov_komentarja = naslov_komentarja
        self._komentar = komentar
        self._imdb_uporabnik = imdb_uporabnik
        self._datum = datum
        self._se_strinja = se_strinja
        self._se_ne_strinja = se_ne_strinja
        self._ocena = ocena


    def shrani_komentar(self):
        '''Shrani IMDB komentar v bazo.'''
        conn = dbapi.connect('filmi.db')
        with conn:
            conn.execute("""
            INSERT OR IGNORE INTO imdb_komentar (imdb_id_komentar, imdb_id_uporabnik, naslov_komentarja, komentar,
                    imdb_uporabnik, datum, se_strinja, se_ne_strinja, ocena)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, [self._imdb_id_komentar, self._imdb_id_uporabnik, self._naslov_komentarja,
                  self._komentar, self._imdb_uporabnik, self._datum, self._se_strinja, self._se_ne_strinja, self._ocena])

    @property
    def imdb_id_komentar(self):
        return self._imdb_id_komentar

    @property
    def imdb_id_uporabnik(self):
        return self._imdb_id_uporabnik

    @property
    def naslov_komentarja(self):
        return self._naslov_komentarja

    @property
    def komentar(self):
        return self._komentar

    @property
    def imdb_uporabnik(self):
        return self._imdb_uporabnik

    @property
    def datum(self):
        return self._datum

    @property
    def se_strinja(self):
        return self._se_strinja

    @property
    def se_ne_strinja(self):
        return self._se_ne_strinja

    @property
    def ocena(self):
        return self._ocena

    @imdb_id_komentar.setter
    def imdb_id_komentar(self, vrednost):
        self._imdb_id_komentar = vrednost

    @imdb_id_uporabnik.setter
    def imdb_id_uporabnik(self, vrednost):
        self._imdb_id_uporabnik = vrednost

    @naslov_komentarja.setter
    def naslov_komentarja(self, vrednost):
        self._naslov_komentarja = vrednost

    @komentar.setter
    def komentar(self, vrednost):
        self._komentar = vrednost

    @imdb_uporabnik.setter
    def imdb_uporabnik(self, vrednost):
        self._imdb_uporabnik = vrednost

    @datum.setter
    def datum(self, vrednost):
        self._datum = vrednost

    @se_strinja.setter
    def se_strinja(self, vrednost):
        self._se_strinja = vrednost

    @se_ne_strinja.setter
    def se_ne_strinja(self, vrednost):
        self._se_ne_strinja = vrednost

    @ocena.setter
    def ocena(self, vrednost):
        self._ocena = vrednost

    @staticmethod
    def pridobi_datum_komentarja(div_znacka_komentar):
        '''Prejme vsebino div znacke (class = review-container), 
            ki je objekt BeautifulSoup. Iz njega izlušči datum kdaj je bil komentar napisan.'''
        span_datum = div_znacka_komentar.find_all('span', class_='review-date')
        span_datum = None if span_datum == [] else span_datum[0]
        if span_datum is None:
            return None
        datum = span_datum.contents
        datum = None if datum == [] else datum[0]
        return datum

    @staticmethod
    def pridobi_tezo_komentarja(div_znacka):
        '''Prejme vsebino div znacke (class = review-container), 
            ki je objekt BeautifulSoup. Iz njega izlušči težo komentarja.'''
        div_moc = div_znacka.find_all('div', class_='actions text-muted')
        div_moc = None if div_moc == [] else div_moc[0]
        if div_moc is None:
            return None
        regex_teza_komentarja = r'\>([^\<]*)<span>'
        teza_komentarja = re.findall(regex_teza_komentarja, str(div_moc))
        teza_komentarja = None if teza_komentarja == [] else teza_komentarja[0]
        return teza_komentarja.strip()

    @staticmethod
    def pridobi_vsebino_komentarja(div_znacka_komentar):
        '''Prejme vsebino div znacke (class = review-container), 
            ki je objekt BeautifulSoup. Iz njega izlušči vsebino komentarja.'''
        div_vsebina = div_znacka_komentar.find_all(
            'div', class_='text show-more__control')
        div_vsebina = None if div_vsebina == [] else div_vsebina[0]
        if div_vsebina is None:
            return None
        regex_html = r'<[\w]{0,2}[\/]?>'
        div_vsebina = re.sub(regex_html, ' ', str(div_vsebina))
        div_vsebina = BeautifulSoup(div_vsebina, 'html.parser')
        div_vsebina = div_vsebina.find_all('div')[0]
        komentar_html = div_vsebina.contents
        komentar_html = None if komentar_html == [] else komentar_html[0]
        if komentar_html is None:
            return None
        regex_html = r'<[^>]*>'
        komentar = re.sub(regex_html, ' ', str(komentar_html))
        komentar = komentar.replace('  ', ' ')
        return komentar.strip()

    @staticmethod
    def pridobi_naslov_komentarja(div_znacka_komentar):
        '''Prejme vsebino div_znacke (class = review-container), 
            ki je objekt BeautifulSoup. Iz njega izlušči naslov komentarja.'''
        a_naslov = div_znacka_komentar.find_all('a', class_='title')
        a_naslov = None if a_naslov == [] else a_naslov[0]
        if a_naslov is None:
            return None
        naslov = a_naslov.contents
        naslov = None if naslov == [] else naslov[0]
        return naslov.replace('\n', ' ').strip()

    @staticmethod
    def pridobi_oceno(div_znacka_komentar):
        '''Prejme vsebino div_znacke (class = review-container), 
            ki je objekt BeautifulSoup. Iz njega izlušči oceno imdb uporabnika.'''
        span_ocena = div_znacka_komentar(
            'span', class_='rating-other-user-rating')
        regex_ocena = r'<span>([^<]*)<\/span>'
        ocena = re.findall(regex_ocena, str(span_ocena))
        ocena = None if ocena == [] else ocena[0]
        return ocena

    @staticmethod
    def pridobi_pisca_komentarja(div_znacka_komentar):
        '''Prejme vsebino div_znacke (class = review-container), 
            ki je objekt BeautifulSoup. Iz njega izlušči uporabnika, ki je napisal komentar.'''
        span_uporabnik = div_znacka_komentar.find_all(
            'span', class_='display-name-link')
        span_uporabnik = None if span_uporabnik == [] else span_uporabnik[0]
        if span_uporabnik is None:
            return None
        a_uporabnik = span_uporabnik.find_all('a')
        a_uporabnik = None if a_uporabnik == [] else a_uporabnik[0]
        if a_uporabnik is None:
            return None
        uporabnik = a_uporabnik.contents[0]
        return uporabnik

    @staticmethod
    def pridobi_imdbID_pisca_komentarja(div_znacka_komentar):
        '''Prejme vsebino div_znacke (class = review-container), 
            ki je objekt BeautifulSoup. Iz njega izlušči imdbID uporabnika, ki je napisal komentar.'''
        regex_imdbID_uporabnik = r'\/user\/([^\/]*)\/'
        span_uporabnik = div_znacka_komentar.find_all(
            'span', class_='display-name-link')
        span_uporabnik = None if span_uporabnik == [] else span_uporabnik[0]
        if span_uporabnik is None:
            return None
        a_uporabnik = span_uporabnik.find_all('a')
        a_uporabnik = None if a_uporabnik == [] else a_uporabnik[0]
        if a_uporabnik is None:
            return None
        uporabnik_imdbID = re.findall(regex_imdbID_uporabnik, str(a_uporabnik))
        return None if uporabnik_imdbID == [] else uporabnik_imdbID[0]

    @staticmethod
    def pridobi_imdb_id_komentarja(div_znacka_komentar):
        '''Prejme vsebino div_znacke (class = review-container), 
            ki je objekt BeautifulSoup. Iz njega izlušči imdb identifikator komentarja.'''
        a_imdb_id = div_znacka_komentar.find_all('a', class_='title')
        a_imdb_id = None if a_imdb_id == [] else a_imdb_id[0]
        if a_imdb_id is None:
            return None
        link_imdb_id = a_imdb_id['href']
        regex_imdb_id = r'\/review\/([^\/]*)\/'
        imdb_id = re.findall(regex_imdb_id, link_imdb_id)
        imdb_id = None if imdb_id == [] else imdb_id[0]
        return imdb_id

    @staticmethod
    def pridobi_data_key(vsebina_strani):
        '''Prejme HTML vsebino strani, ki je BeautifulSoup objekt in vrne ključ do naslednjega seznama komentarjev.
            Če ključa ne najde vrne None.'''
        regex_data_key = r'data-key=\"([^\"]*)'
        data_key = re.findall(regex_data_key, str(vsebina_strani))
        if data_key == []:
            return None
        return data_key[0]

    @staticmethod
    def pridobi_naslednji_seznam_komentarjev(vsebina_strani, vsebina_imdb_id):
        '''Pridobi link do naslednjih komentarjev. Kot parameter vzame HTML vsebino spletne strani, ki je BeautifulSoup objekt in
            IMDB identifikator vsebine (film, serija, epizoda) in vrne link do naslednjega seznama komentarjev za podano vsebino.'''
        data_key = KomentarIMDB.pridobi_data_key(vsebina_strani)
        url = "https://www.imdb.com/title/" + vsebina_imdb_id + \
            "/reviews/_ajax?ref_=undefined&paginationKey=" + data_key
        return url

    @staticmethod
    def pridobi_komentarje(vsebina_naslov, vsebina_imdb_id):
        '''Prjme IMDB identifikator filma in naslov ter vrne vse komentarje za dani film v obliki slovarja.'''
        url = f'https://www.imdb.com/title/{vsebina_imdb_id}/reviews'
        odziv = Bralnik.pridobi_html(url)
        vsebina_strani = BeautifulSoup(odziv, 'html.parser')
        komentarji = vsebina_strani.findall('div', class_='review-container')
