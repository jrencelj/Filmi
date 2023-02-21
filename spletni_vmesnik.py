import bottle
from film import Film
from serija import Serija
from vsebina import Vsebina
from uporabnik import Uporabnik
from uporabnik_tip import Uporabnik_Tip
import hashlib

def hash_geslo(geslo):
    tekst = geslo.encode("utf-8")
    d = hashlib.sha256(tekst)
    hash = d.hexdigest()
    return hash

def pridobi_uporabnika():
    """Kdo je uporabnik."""
    uporabnisko_ime = bottle.request.get_cookie('uporabnisko_ime', secret='skrivnost')
    if uporabnisko_ime is not None:
        return uporabnisko_ime
    else:
        return None

@bottle.route('/<filename>.css')
def stylesheets(filename):
    return bottle.static_file(f'{filename}.css', root='static')

@bottle.route('/static/<filename>.jpeg')
def jpeg(filename):
    return bottle.static_file(f'{filename}.jpeg', root='static')

@bottle.route('/static/default_avatar.png')
def default_avatar():
    return bottle.static_file('default_avatar.png', root='static')

@bottle.route("/")
def glavna_stran():
    return bottle.template('index.html', root='Projekt', uporabnisko_ime = pridobi_uporabnika())

@bottle.post('/do_prijava')
def do_prijava():
    uporabnisko_ime = bottle.request.forms.getunicode("username")
    geslo = bottle.request.forms.getunicode("pass")
    if Uporabnik.je_uporabnik(uporabnisko_ime):
        uporabnik = Uporabnik.pridobi_uporabnika_po_username(uporabnisko_ime)
        if hash_geslo(geslo + uporabnik.sol) == uporabnik.geslo:
            bottle.response.set_cookie("uporabnisko_ime", uporabnisko_ime, path='/', secret='skrivnost')
            bottle.redirect('/')
        else:
            return bottle.template('index.html', uporabnisko_ime = pridobi_uporabnika())
    else:
        return bottle.template('index.html', uporabnisko_ime = pridobi_uporabnika())
    
    


@bottle.route("/odjava")
def odjava():
    bottle.response.delete_cookie('uporabnisko_ime')
    bottle.redirect('/')

@bottle.post('/do_registracija')
def do_registracija():
    email = bottle.request.forms.getunicode("email")
    uporabnisko_ime = bottle.request.forms.getunicode("username")
    pass1 = bottle.request.forms.getunicode("pass1")
    pass2 = bottle.request.forms.getunicode("pass2")
    if pass1 == pass2:
        sol = "sol"
        geslo = hash_geslo(pass1 + sol)
        datum_rojstva = bottle.request.forms.getunicode("bday")
        uporabnik = Uporabnik(None, uporabnisko_ime, email, datum_rojstva, geslo, sol, Uporabnik_Tip("U", "uporabnik", None))
        uporabnik.shrani_uporabnik()
        return bottle.template('index.html', uporabnisko_ime = pridobi_uporabnika())
    else:
        return bottle.template('index.html', uporabnisko_ime = pridobi_uporabnika(), napake = 'Gesli se ne ujemata.')

@bottle.route("/registracija")
def registracija():
    return bottle.template('registracija.html')

@bottle.route("/filmi")
def filmi():
    filmi = Film.pridobi_vse_filme()
    return bottle.template('filmi.html', filmi=filmi, uporabnisko_ime = pridobi_uporabnika())

@bottle.route("/generator_film")
def generator_film():
    filmi = Film.pridobi_vse_filme()
    predlogi = []
    return bottle.template('generator_film.html', filmi=filmi, predlogi=predlogi, uporabnisko_ime = pridobi_uporabnika())

@bottle.route("/generator_serija")
def generator_serija():
    serije = Serija.pridobi_vse_serije()
    predlogi = []
    return bottle.template('generator_serija.html', serije=serije, predlogi=predlogi, uporabnisko_ime = pridobi_uporabnika())

@bottle.post("/generator_serija")
def do_predlaga_serija():
    serija1 = bottle.request.forms.getunicode("izberi_serija1")
    serija2 = bottle.request.forms.getunicode("izberi_serija2")
    serija3 = bottle.request.forms.getunicode("izberi_serija3")
    serije = Serija.pridobi_vse_serije()
    predlogi = Serija.pridobi_predloge_za_serijo(serija1, serija2, serija3)
    return bottle.template("generator_serija", serije=serije, predlogi = predlogi, uporabnisko_ime = pridobi_uporabnika())


@bottle.post("/generator_film")
def do_predlaga_filmi():
    film1 = bottle.request.forms.getunicode("izberi_film1")
    film2 = bottle.request.forms.getunicode("izberi_film2")
    film3 = bottle.request.forms.getunicode("izberi_film3")
    filmi = Film.pridobi_vse_filme()
    predlogi = Film.pridobi_predloge_za_film(film1, film2, film3)
    return bottle.template("generator_film", filmi=filmi, predlogi = predlogi, uporabnisko_ime = pridobi_uporabnika())

@bottle.route("/serije")
def serije():
    serije = Serija.pridobi_vse_serije()
    return bottle.template('serije.html', serije=serije, uporabnisko_ime = pridobi_uporabnika())

@bottle.route("/filmi/<id:int>")
def podrobno_film(id):
    film = Film.pridobi_film_z_id(id)
    komentarji_filma = Film.pridobi_komentarje_po_id_film(id)
    reziserji = Vsebina.pridobi_reziserje_za_vsebino(id)
    igralci = Vsebina.pridobi_igralce_za_vsebino(id)
    kinoteke = Vsebina.pridobi_kinoteke_za_vsebino(id)
    return bottle.template('podrobno_film.html', film = film, komentarji_filma = komentarji_filma, reziserji = reziserji, igralci = igralci, kinoteke=kinoteke,
                           uporabnisko_ime = pridobi_uporabnika())

@bottle.route("/serije/<id:int>")
def podrobno_serija(id):
    serija = Serija.pridobi_serijo_z_id(id)
    komentarji_serije = Serija.pridobi_komentarje_po_id_serija(id)
    reziserji = Vsebina.pridobi_reziserje_za_vsebino(id)
    igralci = Vsebina.pridobi_igralce_za_vsebino(id)
    kinoteke = Vsebina.pridobi_kinoteke_za_vsebino(id)
    return bottle.template('podrobno_serija.html', serija=serija, komentarji_serije = komentarji_serije, reziserji = reziserji, igralci = igralci,
                           kinoteke = kinoteke, uporabnisko_ime = pridobi_uporabnika())

bottle.run(debug=True, reloader=True)
