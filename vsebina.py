from bralnik import Bralnik
from bs4 import BeautifulSoup
import re
import json
from komentarIMDB import KomentarIMDB
import os
from vsebina_tip import Vsebina_Tip


class Vsebina:
    def __init__(self, id, naslov, dolzina, url_slika, imdb_id_vsebina, opis,
                 datum_prvega_predvajanja, vsebina_tip):
        self._id = id
        self._naslov = naslov
        self._imdb_id_vsebina = imdb_id_vsebina
        self._dolzina = dolzina
        self._url_slika = url_slika
        if not isinstance(vsebina_tip, Vsebina_Tip):
            raise Exception(f'{vsebina_tip} ni objekt razreda Vsebina_Tip')
        else:
            self._vsebina_tip = vsebina_tip
        self._opis = opis
        self._datum_prvega_predvajanja = datum_prvega_predvajanja

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, vrednost):
        self._id = vrednost

    @property
    def naslov(self):
        return self._naslov

    @property
    def dolzina(self):
        return self._dolzina

    @property
    def url_slika(self):
        return self._url_slika

    @property
    def imdb_id_vsebina(self):
        return self._imdb_id_vsebina

    @property
    def opis(self):
        return self._opis

    @property
    def datum_prvega_predvajanja(self):
        return self._datum_prvega_predvajanja

    @property
    def vsebina_tip(self):
        return self._vsebina_tip

    @naslov.setter
    def naslov(self, vrednost):
        self._naslov = vrednost

    @dolzina.setter
    def dolzina(self, vrednost):
        self._dolzina = vrednost

    @url_slika.setter
    def url_slika(self, vrednost):
        self._url_slika = vrednost

    @imdb_id_vsebina.setter
    def imdb_id_vsebina(self, vrednost):
        self._imdb_id_vsebina = vrednost

    @opis.setter
    def opis(self, vrednost):
        self._opis = vrednost

    @datum_prvega_predvajanja.setter
    def datum_prvega_predvajanja(self, vrednost):
        self._datum_prvega_predvajanja = vrednost

    @vsebina_tip.setter
    def vsebina_tip(self, vrednost):
        self._vsebina_tip = vrednost

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
    def preoblikuj_v_ime(ime_vsebine):
        '''Prejme ime vsebine (ime serije, filma ali epizode). Preoblikuje ime vsebine v ime datoeke.'''
        return ime_vsebine.lower().replace(': ', '_').replace(' ', '_').replace('\'', '_').replace('/', '_') + '_komentarji'

    @staticmethod
    def pridobi_naslednji_seznam_komentarjev(vsebina_strani, vsebina_imdb_id):
        '''Pridobi link do naslednjih komentarjev. Kot parameter vzame HTML vsebino spletne strani, ki je BeautifulSoup objekt in
            IMDB identifikator vsebine (film, serija, epizoda) in vrne link do naslednjega seznama komentarjev za podano vsebino.'''
        data_key = Vsebina.pridobi_data_key(vsebina_strani)
        if data_key is None:
            return None
        url = "https://www.imdb.com/title/" + vsebina_imdb_id + \
            "/reviews/_ajax?ref_=undefined&paginationKey=" + data_key
        return url

    def pridobi_komentarje(self):
        '''Prejme objekt razreda Vsebina vrne vse komentarje za dani film v obliki slovarja.'''
        vsebina = dict()
        url = f'https://www.imdb.com/title/{self._imdb_id}/reviews'
        print(url)
        odziv = Bralnik.pridobi_html(url)
        vsebina_strani = BeautifulSoup(odziv, 'html.parser')
        div_komentarji = vsebina_strani.find_all(
            'div', class_='review-container')
        komentarji = dict()
        zastavica = False
        stevec = 0
        while True:
            if zastavica:
                break
            for div_komentar in div_komentarji:
                stevec += 1
                print(stevec)
                komentar_podatki = dict()
                komentar_imdb_id = KomentarIMDB.pridobi_imdb_id_komentarja(
                    div_komentar)
                komentar_podatki['Title'] = KomentarIMDB.pridobi_naslov_komentarja(
                    div_komentar)
                komentar_podatki['Comment'] = KomentarIMDB.pridobi_vsebino_komentarja(
                    div_komentar)
                komentar_podatki['Mark'] = KomentarIMDB.pridobi_oceno(
                    div_komentar)
                komentar_podatki['Date'] = KomentarIMDB.pridobi_datum_komentarja(
                    div_komentar)
                komentar_podatki['Weight'] = KomentarIMDB.pridobi_tezo_komentarja(
                    div_komentar)
                komentar_podatki['User'] = KomentarIMDB.pridobi_pisca_komentarja(
                    div_komentar)
                komentar_podatki['User ImdbID'] = KomentarIMDB.pridobi_imdbID_pisca_komentarja(
                    div_komentar)
                komentarji[komentar_imdb_id] = komentar_podatki
            naslednji_url = Vsebina.pridobi_naslednji_seznam_komentarjev(
                vsebina_strani, self._imdb_id)
            print(naslednji_url)
            if naslednji_url is None:
                zastavica = True
            else:
                odziv = Bralnik.pridobi_html(naslednji_url)
                vsebina_strani = BeautifulSoup(odziv, 'html.parser')
                div_komentarji = vsebina_strani.find_all(
                    'div', class_='review-container')
        vsebina[self._naslov] = komentarji
        return vsebina

    def shrani_komentarje_v_json(self):
        '''Shrani komentarje vsebine v json datoteko.'''
        ime_datoteke = Vsebina.preoblikuj_v_ime(self._naslov)
        podatki = self.pridobi_komentarje()
        with open(f'data/komentar/komentar_film/{ime_datoteke}.json', 'w', encoding='utf8') as f:
            json.dump(podatki, f)

    def shrani_komentarje_serij_v_json(self):
        '''Shrani komentarje vsebine v json datoteko.'''
        ime_datoteke = Vsebina.preoblikuj_v_ime(self._naslov)
        podatki = self.pridobi_komentarje()
        with open(f'data/komentar/komentar_serija/{ime_datoteke}.json', 'w', encoding='utf8') as f:
            json.dump(podatki, f)

    @staticmethod
    def shrani_komentarje_vsi_filmi():
        '''Shrani komentarje vseh filmo v ustrezne json datoteke.'''
        with open('data/film/filmi.json', 'r') as f:
            filmi = json.load(f)
        for naslov, podatki in filmi.items():
            vsebina = Vsebina(
                naslov, podatki['imdbID'], None, None, None, None, None, None, None, None)
            ime_datoteke = Vsebina.preoblikuj_v_ime(naslov)
            if os.path.exists(f'data/komentar/komentar_film/{ime_datoteke}.json'):
                continue
            else:
                print(naslov)
                vsebina.shrani_komentarje_v_json()

    @staticmethod
    def shrani_komentarje_vse_serije():
        '''Shrani komentarje vseh serij v ustrezne json datoteke.'''
        with open('data/serija/serije.json', 'r') as f:
            serije = json.load(f)
        for naslov, podatki in serije.items():
            vsebina = Vsebina(
                naslov, podatki['imdbID'], None, None, None, None, None, None, None, None)
            ime_datoteke = Vsebina.preoblikuj_v_ime(naslov)
            if os.path.exists(f'data/komentar/komentar_serija/{ime_datoteke}.json'):
                continue
            else:
                print(naslov)
                vsebina.shrani_komentarje_serij_v_json()
