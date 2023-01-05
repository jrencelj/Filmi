import bottle
from film import Film

@bottle.route("/")
def glavna_stran():
    return bottle.template('index.html', root = 'Projekt')

@bottle.route("/filmi")
def filmi():
    filmi = Film.pridobi_vse_filme()
    return bottle.template('filmi.html', filmi = filmi)

@bottle.route("/serije")
def serije():
    # TODO
    return FileNotFoundError

@bottle.route("/static/css/<filename>")
def serve_static_file_css(filename):
    return bottle.static_file(
        filename, root = "./static/css"
    )

bottle.run(debug = True, reloader = True)
