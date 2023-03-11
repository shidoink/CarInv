from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Car, contact_schema, contacts_schema

api= Blueprint('api',__name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return{'yee':'haw'}

@api.route('/cars',methods = ["POST"])
@token_required
def create_car(current_user_token):
    make= request.json['make']
    model= request.json['model']
    year= request.json['year']
    horse_power= request.json['horse_power']
    value = request.json['value']
    user_token= current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    car = Car(make, model, year, horse_power, value, user_token= user_token)

    db.session.add(car)
    db.session.commit()

    response = contact_schema.dump(car)
    return jsonify(response)

@api.route('/cars',methods = ['GET'])
@token_required
def get_cars(current_user_token):
    a_user = current_user_token.token
    cars = Car.query.filter_by(user_token = a_user).all()
    response = contacts_schema.dump(cars)
    return jsonify(response)

@api.route('/cars/<id>', methods = ['GET'])
@token_required
def get_single_car(current_user_token, id):
    fan = current_user_token.token
    car= Car.query.get(id)
    response = contact_schema.dump(car)
    return jsonify(response)

#Update endpoint
@api.route('/cars/<id>', methods = ['POST','PUT'])
@token_required
def update_car(current_user_token, id):
    car = Car.query.get(id)
    car.make = request.json['make']
    car.model = request.json['model']
    car.year = request.json['year']
    car.horse_power = request.json['horse_power']
    car.value = request.json['value']
    car.user_token = current_user_token.token

    db.session.commit()
    response = contact_schema.dump(car)
    return jsonify(response)

#delete endpoint
@api.route('/cars/<id>', methods = ['DELETE'])
@token_required
def delete_contact(current_user_token, id):
    car = Car.query.get(id)
    db.session.delete(car)
    db.session.commit()
    response = contact_schema.dump(car)
    return jsonify(response)
