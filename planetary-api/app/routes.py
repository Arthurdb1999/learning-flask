from flask import Flask, jsonify, request
from app import app, models, db

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