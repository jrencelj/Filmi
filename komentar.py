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
