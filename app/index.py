from flask import Flask 
from flask import render_template 
from flask import g 
from flask import redirect 
from flask import request

app = Flask(__name__, static_url_path="", static_folder="static")

@app.route('/')
def accueil():
    return render_template('accueil.html')
