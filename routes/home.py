from flask import Blueprint, render_template

home_route = Blueprint('home', __name__) # Criação da Blueprint

# Criação da rota
@home_route.route('/') # Rota principal '/'
def home():
    return render_template('index.html')