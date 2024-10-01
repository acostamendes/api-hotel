from flask import Flask, jsonify
from flask_restful import Api
from sql_alchemy import banco
from resources.hotel import Hoteis, Hotel
from resources.user import User, UserRegister, UserLogin, UserLogout, UserConfirm
from resources.site import Site, Sites
from flask_jwt_extended import JWTManager # type: ignore
from blacklist import BLACKLIST
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.urandom(24).hex()
#app.config['JWT_SECRET_KEY'] = 'DontTellAnyone'
app.config['JWT_BLACKLIST_ENABLED'] = True 

api = Api(app)
jwt = JWTManager(app)

# Solução para criar o banco de dados antes da primeira requisição
@app.before_request
def cria_banco():
    banco.create_all()

@jwt.token_in_blocklist_loader
def verifica_blacklist(jwt_header, jwt_data):
    return jwt_data['jti'] in BLACKLIST

@jwt.revoked_token_loader
def token_de_acesso_invalidado(jwt_header, jwt_data):
    return jsonify({'message':'You have been logged out.'}),401 # unauthorized 

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({'message': 'You have been logged out.', 'error': str(error)}), 401

# Adicionando o recurso à rota
api.add_resource(Hoteis, '/hoteis')
api.add_resource(Hotel, '/hoteis/<string:hotel_id>')
api.add_resource(User, '/usuarios/<int:user_id>')
api.add_resource(UserRegister, '/cadastro')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(Sites,'/sites')
api.add_resource(Site, '/sites/<string:url>')
api.add_resource(UserConfirm, '/confirmacao/<int:user_id>')

if __name__ == '__main__':
    banco.init_app(app)
    app.run(debug=True)




# http://127.0.0.1:500/hoteis

# ativar ambiente virtual windows '.\ambvir\Scripts\Activate'
# subir a aplicação 'python app.py'