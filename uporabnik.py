from uporabnik_tip import Uporabnik_Tip


class Uporabnik:
    def __init__(self, uporabnisko_ime, e_naslov, datum_rojstva, geslo, uporabnik_tip):
        self._uporabnisko_ime = uporabnisko_ime
        self._e_naslov = e_naslov
        self._datum_rojstva = datum_rojstva
        self._geslo = geslo
        if not isinstance(uporabnik_tip, Uporabnik_Tip):
            raise Exception(f'{uporabnik_tip} ni objekt razreda Uporabnik_Tip')
        else:
            self._uporabnik_tip = uporabnik_tip

    def shrani_uporabnik(self):
        '''Shrani uporabnika v bazo.'''
        # TODO
        pass

    @property
    def uporabnisko_ime(self):
        return self._uporabnisko_ime

    @property
    def e_naslov(self):
        return self._e_naslov

    @property
    def datum_rojstva(self):
        return self._datum_rojstva

    @property
    def geslo(self):
        return self._geslo

    @property
    def uporabnik_tip(self):
        return self._uporabnik_tip

    @uporabnisko_ime.setter
    def uporabnisko_ime(self, vrednost):
        self._uporabnisko_ime = vrednost

    @e_naslov.setter
    def e_naslov(self, vrednost):
        self._e_naslov = vrednost

    @datum_rojstva.setter
    def datum_rojstva(self, vrednost):
        self._datum_rojstva = vrednost

    @geslo.setter
    def geslo(self, vrednost):
        self._geslo = vrednost

    @uporabnik_tip.setter
    def uporabnik_tip(self, vrednost):
        self._uporabnik_tip = vrednost
