from vsebina import Vsebina


class Serija(Vsebina):
    def __init__(self, naslov, dolzina, imdb_id, opis, datum_prvega_predvajanja, leto_izida,
                 certifikat, vsebina_tip):
        super()._naslov = naslov
        super()._dolzina = dolzina
        # TODO

    def vstavi_serija(self):
        '''Vstavi serijo v bazo.'''
        # TODO
        pass

    @property
    def imdb_id(self):
        return self._imdb_id

    @property
    def leto_izida(self):
        return self._leto_izida

    @property
    def certifikat(self):
        return self._certifikat

    @property.setter
    def imdb_id(self, vrednost):
        self._imdb_id = vrednost

    @property.setter
    def leto_izida(self, vrednost):
        self._leto_izida = vrednost

    @property.setter
    def certifikat(self, vrednost):
        self._certifikat = vrednost
