from film import Film
from uporabnik import Uporabnik


class Komentar:
    def __init__(self, uporabnik, naslov_komentar, besedilo_komentar, ocena, film, ura_datum):
        self._uporabnik = uporabnik
        self._naslov_komentar = naslov_komentar
        self._besedilo_komentar = besedilo_komentar
        self._ocena = ocena
        if not isinstance(film, Film):
            raise Exception(f'{film} ni objekt razreda Film')
        else:
            self._film = film
        if not isinstance(uporabnik, Uporabnik):
            raise Exception(f'{uporabnik} ni objekt razreda Uporabnik')
        else:
            self._uporabnik = uporabnik
        self._ura_datum = ura_datum

    def vstavi_komentar(self):
        '''Vstavi komentar v bazo.'''
        # TODO
        pass

    @property
    def uporabnik(self):
        return self._uporabnik

    @property
    def naslov_komentar(self):
        return self._naslov_komentar

    @property
    def besedilo_komentar(self):
        return self._besedilo_komentar

    @property
    def ocena(self):
        return self._ocena

    @property
    def film(self):
        return self._film

    @property
    def ura_datum(self):
        return self._ura_datum

    @property.setter
    def uporabnik(self, vrednost):
        self._uporabnik = vrednost

    @property.setter
    def naslov_komentar(self, vrednost):
        self._naslov_komentar = vrednost

    @property.setter
    def besedilo_komentar(self, vrednost):
        self._besedilo_komentar = vrednost

    @property.setter
    def ocena(self, vrednost):
        self._ocena = vrednost

    @property.setter
    def film(self, vrednost):
        self._film = vrednost

    @property.setter
    def ura_datum(self, vrednost):
        self._ura_datum = vrednost
