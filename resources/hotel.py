from flask import Flask, request, jsonify
from flask_restful import Api, Resource, reqparse
from models.hotel import HotelModel
from resources.filter import normalize_path_params, consulta_com_cidade, consulta_sem_cidade
from models.site import SiteModel
from flask_jwt_extended import jwt_required
import sqlite3

app = Flask(__name__)
api = Api(app)

# Lista de hotéis
hoteis = [
    {
        'hotel_id': 'alpha',
        'nome': 'Alpha Hotel',
        'estrelas': 4.3,
        'diaria': 420.34,
        'cidade': 'Rio de Janeiro'
    },
    {
        'hotel_id': 'bravo',
        'nome': 'Bravo Hotel',
        'estrelas': 4.4,
        'diaria': 380.90,
        'cidade': 'Santa Catarina'
    },
    {
        'hotel_id': 'charlie',
        'nome': 'Charlie Hotel',
        'estrelas': 3.9,
        'diaria': 320.20,
        'cidade': 'Santa Catarina'
    },
    {
        'hotel_id': 'alvorada',
        'nome': 'Alvorada Hotel',
        'estrelas': 3.5,
        'diaria': 300.20,
        'cidade': 'Santa Catarina'
    }
]


# path /hoteis?cidade= Rio de Janeiro&estrelmas_min=4&diaria_max=400

path_params = reqparse.RequestParser()
path_params.add_argument('cidade', type=str)
path_params.add_argument('estrelas_min', type=float)
path_params.add_argument('estrelas_max', type=float)
path_params.add_argument('diaria_min', type=float)
path_params.add_argument('diaria_max', type=float)
path_params.add_argument('limit', type=float)
path_params.add_argument('offset', type=float)


class Hoteis(Resource):
    def get(self):
        connection = sqlite3.connect('instance/banco.db')
        cursor = connection.cursor()

        dados = path_params.parse_args()
        dados_valid= {chave:dados[chave] for chave in dados if dados [chave] is not None }
        parametrs = normalize_path_params(**dados_valid)

        if not parametrs.get('cidade'):
           # tupla = (
            #    parametrs['estrelas_min'], 
            #    parametrs['estrelas_max'], 
            #    parametrs['diaria_min'], 
            #    parametrs['diaria_max'], 
            #    parametrs['limit'], 
            #    parametrs['offset']
            #)
            tupla = tuple([parametrs [chave] for chave in parametrs])
            resultado = cursor.execute(consulta_sem_cidade, tupla)
        else:
            tupla = tuple([parametrs [chave] for chave in parametrs])
            resultado = cursor.execute(consulta_com_cidade, tupla)

        hoteis = []
        for linha in resultado:
            hoteis.append({
            'hotel_id': linha[0],
            'nome': linha[1],
            'estrelas': linha[2],
            'diaria': linha[3],
            'cidade':linha[4],
            'site_id':linha[5]
            })

        return {'hoteis': hoteis}
       # return {'hoteis': [hotel.json() for hotel in HotelModel.query.all()]} #SELECT * FROM hoteis 

class Hotel(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome', type=str, required=True, help="The filed 'nome' cannot be left blank.")
    argumentos.add_argument('estrelas', type=float, required=True, help="The filed 'estrelas' cannot be left blank.")
    argumentos.add_argument('diaria', type=float)
    argumentos.add_argument('cidade',type=str, required=True, help="The filed 'cidade' cannot be left blank.")
    argumentos.add_argument('site_id', type=int, required=True, help="Every hotel needs to be linked with a site.")

    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json()
        return {'message': 'Hotel not found.'}, 404
    
    @jwt_required()
    def post(self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return {"message":"Hotel id '{}' already exists.".format(hotel_id)},400 #Bad request

        dados = Hotel.argumentos.parse_args()
        hotel = HotelModel(hotel_id, **dados) #objeto #instancia um hotel
        
        if not SiteModel.find_by_id(dados.get('site_id')):
            return{'message': 'The hotel must be associated to a valid site id.'}, 400 #Bad request
        
        try:
            hotel.save_hotel()
        except:
            return {'message': 'An internal error occurred trying to save hotel.'}, 500 #Internal Server Error     
        return hotel.json(), 201

    @jwt_required()
    def put(self, hotel_id):
        dados = Hotel.argumentos.parse_args()
        hotel_encontrado = HotelModel.find_hotel(hotel_id)
        if hotel_encontrado:
            hotel_encontrado.update_hotel(**dados)
            hotel_encontrado.save_hotel()
            return hotel_encontrado.json(), 200
        hotel = HotelModel(hotel_id, **dados) #objeto
        try:
            hotel.save_hotel()
        except:
            return {'message': 'An internal error occurred trying to save hotel.'}, 500 #Internal Server Error
        return hotel.json(), 201

    @jwt_required()
    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel: 
            try:
                hotel.delete_hotel()
            except:
                return {'message': 'An internal error occurred trying to delete hotel'}, 500
            return {'message': 'Hotel deleted.'}
        return {'message': 'Hotel not found.'}, 404

