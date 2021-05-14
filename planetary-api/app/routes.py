from flask import Flask, jsonify, request
from app import app, models, db, mail, jwt
from flask_jwt_extended import jwt_required, create_access_token
from flask_mail import Message

@app.route('/')
def hello_world():
    return "Hello World"


@app.route('/super_simple')
def super_simple():
    return jsonify(message='Hello planetary api'), 200


@app.route('/not_found')
def not_found():
    return jsonify(message='That resource was not found'), 404


@app.route('/parameters')
def parameters():
    name = request.args.get('name')
    age = int(request.args.get('age'))
    if age < 18 :
        return jsonify(message='Sorry ' + name + ', you are not old enough!'), 401
    else:
        return jsonify(message='Welcome ' + name + ', you are old enough!')


@app.route('/url_variables/<string:name>/<int:age>')
def url_variables(name: str, age: int):
    if age < 18 :
        return jsonify(message='Sorry ' + name + ', you are not old enough!'), 401
    else:
        return jsonify(message='Welcome ' + name + ', you are old enough!')

@app.route('/planets', methods=["GET"])
def planets():
    planets_list = models.Planet.query.all()
    result = models.planets_schema.dump(planets_list)
    return jsonify(result)

@app.route('/register', methods=["POST"])
def register():
    email = request.form['email']
    test = models.User.query.filter_by(email=email).first()
    
    if test:
        return jsonify(message='That email already exists!'), 409
    else:
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        password = request.form['password']

        user = models.User(first_name=first_name, last_name=last_name, email=email, password=password)
        db.session.add(user)
        db.session.commit()

        return jsonify(message='User created successfully'), 201


@app.route('/login', methods=['POST'])
def login():
    if request.is_json:
        email = request.json['email']
        password = request.json['password']
    else:
        email = request.form['email']
        password = request.form['password']

    test = models.User.query.filter_by(email=email, password=password).first()
    if test:
        access_token = create_access_token(identity=email)
        return jsonify(message="Login succeeded", access_token=access_token)
    else:
        return jsonify(message="Bad email or password"), 401


@app.route('/retrieve_password/<string:email>', methods=["GET"])
def retrieve_password(email: str):
    user = models.User.query.filter_by(email=email).first()
    if user:
        msg = Message("your planetary API password is " + user.password,
                        sender="admin@planetary-api.com",
                        recipients=[email])
        mail.send(msg)
        return jsonify(message="Password sent to " + email)
    else:
        return jsonify(message="That email doesn't exist!"), 401


@app.route('/planet_details/<int:id>', methods=['GET'])
def planet_details(id: int):
    planet = models.Planet.query.filter_by(id=id).first()
    if planet:
        result = models.planet_schema.dump(planet)
        return jsonify(result)
    else:
        return jsonify(message="That planet does not exist"), 404


@app.route('/add_planet', methods=['POST'])
@jwt_required()
def add_planet():
    name = request.form['name']
    test = models.Planet.query.filter_by(name=name).first()
    if test:
        return jsonify(message="There is already a planet by that name"), 409
    else:
        type = request.form['type']
        home_star = request.form['home_star']
        mass = float(request.form['mass'])
        radius = float(request.form['radius'])
        distance = float(request.form['distance'])

        new_planet = models.Planet(name=name, type=type, home_star=home_star, radius=radius, mass=mass, distance=distance)
        db.session.add(new_planet)
        db.session.commit()

        return jsonify(message="You added a planet"), 201


@app.route('/update_planet', methods=["PUT"])
@jwt_required()
def update_planet():
    id = int(request.form['id'])
    planet = models.Planet.query.filter_by(id=id).first()
    if planet:
        planet.name = request.form['name']
        planet.type = request.form['type']
        planet.home_star = request.form['home_star']
        planet.mass = float(request.form['mass'])
        planet.radius = float(request.form['radius'])
        planet.distance = float(request.form['distance'])

        db.session.commit()
        return jsonify(message="You updated a planet"), 202
    else:
        return jsonify(message="That planet doesn't exist!"), 404


@app.route('/remove_planet/<int:id>', methods=["DELETE"])
@jwt_required()
def remove_planet(id: int):
    planet = models.Planet.query.filter_by(id=id).first()
    if planet:
        db.session.delete(planet)
        db.session.commit()
        return jsonify(message="You deleted a planet"), 202
    else:
        return jsonify(message="That planet does not exist"), 404