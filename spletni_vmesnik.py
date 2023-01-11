import bottle
from film import Film
from serija import Serija


@bottle.route('/<filename>.css')
def stylesheets(filename):
    return bottle.static_file(f'{filename}.css', root='static')


@bottle.route("/")
def glavna_stran():
    return bottle.template('index.html', root='Projekt')


@bottle.route("/filmi")
def filmi():
    filmi = Film.pridobi_vse_filme()
    return bottle.template('filmi.html', filmi=filmi)


@bottle.route("/serije")
def serije():
    serije = Serija.pridobi_vse_serije()
    return bottle.template('serije.html', serije=serije)

@bottle.route("/filmi/<id:int>")
def podrobno_film(id):
    film = Film.pridobi_film_z_id(id)
    return bottle.template('podrobno_film.html', film = film)

bottle.run(debug=True, reloader=True)
