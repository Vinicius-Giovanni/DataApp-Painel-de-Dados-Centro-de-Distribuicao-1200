from flask import Flask

from routes.home import home_route

# Inicialização do servidor web
app = Flask(__name__)

# Registro de telas blueprint
app.register_blueprint(home_route) # Blueprint da tela principal

# Run do servidor web
app.run(debug=True)
