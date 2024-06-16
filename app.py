from flask import Flask
from flask_restful import Api
from resources.hotel import Hoteis, Hotel  # Certifique-se de que o nome do recurso está correto

app = Flask(__name__)
api = Api(app)

# Adicionando o recurso à rota /hoteis
api.add_resource(Hoteis, '/hoteis')
api.add_resource(Hotel, '/hoteis/<string:hotel_id>')

if __name__ == '__main__':
    app.run(debug=True)


# http://127.0.0.1:500/hoteis