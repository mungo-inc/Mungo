from flask import Flask 
from flask import render_template 
from flask import g 
from flask import redirect 
from flask import request

app = Flask(__name__, static_url_path="", static_folder="static")

@app.route('/')
def accueil():
    return render_template('index.html')


@app.route('/recettes')
def recettes():
    return render_template('recettes.html')


@app.route('/search', methods=['GET'])
def search():
    resultats = []
    # requete POST au lieu de GET?
    # aller chercher les valeurs cochées et le budget
    # avec ces valeurs, effectuer une query sql afin d'obtenir des resultats
    epiceries = request.args.getlist('epicerie')
    allergies = request.args.getlist('allergie')
    dietes = request.args.getlist('diete')
    budget = request.args['budget']
    return render_template('resultats.html', resultats=resultats)
