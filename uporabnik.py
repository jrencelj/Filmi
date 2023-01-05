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