from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_mail import Mail, Message
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'planets.db')
app.config['JWT_SECRET_KEY'] = 'super-secret'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_USERNAME'] = os.environ['MAIL_USERNAME']
app.config['MAIL_PASSWORD'] = os.environ['MAIL_PASSWORD']
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True

db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)
mail = Mail(app)


def db_seed():
  mercury = Planet(
    planet_name = 'Mercury',
    planet_type = 'Class D',
    home_star = 'Sol',
    mass = 3.258e23,
    radius = 1516,
    distance = 35.98e6
  )
  venus = Planet(
    planet_name = 'Venus',
    planet_type = 'Class K',
    home_star = 'Sol',
    mass = 4.867e24,
    radius = 3760,
    distance = 67.24e6
  )
  earth = Planet(
    planet_name = 'Earth',
    planet_type = 'Class M',
    home_star = 'Sol',
    mass = 5.972e24,
    radius = 3959,
    distance = 92.96e6
  )

  db.session.add(mercury)
  db.session.add(venus)
  db.session.add(earth)

  test_user = User(
    first_name = 'Roy',
    last_name = 'Cloud',
    email = 'e@ma.il',
    password = '123456'
  )

  db.session.add(test_user)
  db.session.commit()
  return jsonify(message = 'Db seeded')

def validate(_name: str, _age: int):
  if _age < 18:
    return jsonify(message='Sorry ' + _name + ', you are not old enough.'), 401
  else:
    return jsonify(message='Welcome ' + _name + ' to the jungle!', user=_name, age=_age)


# Routes

# GET

@app.route('/')
def index():
  return 'Hello World'

@app.route('/json')
def ret_json():
  return jsonify(message='Hello from JSON')

@app.route('/not-found')
def not_found():
  return jsonify(message='Resource not found'), 404

@app.route('/parameters')
def parameters():
  name = request.args.get('name')
  age = int(request.args.get('age'))
  return validate(name, age)

@app.route('/variables/<string:name>/<int:age>')
def variables(name: str, age: int):
  return validate(name, age)

@app.route('/create-db')
@jwt_required
def db_create():
  db.create_all()
  return jsonify(message = 'Db created')

@app.route('/drop-db')
@jwt_required
def db_drop():
  db.drop_all()
  return jsonify(message = 'Db dropped!')

@app.route('/populate-db')
@jwt_required
def populate_db():
  return db_seed()

@app.route('/planets', methods = ['GET'])
def check_db():
  planets = Planet.query.all()
  res = planets_schema.dump(planets)
  return jsonify(res)


@app.route('/planet/<string:planet_id>', methods = ['GET'])
def planet(planet_id: int):
  planet = Planet.query.filter_by(planet_id = planet_id).first()
  if planet:
    res = planet_schema.dump(planet)
    return jsonify(res)
  else:
    return jsonify(message = 'Planet not found'), 404


@app.route('/users', methods = ['GET'])
def users():
  users = User.query.all()
  res = users_schema.dump(users)
  filtered = list()
  for i, user in enumerate(res):
    filtered.append({
      'first_name': user['first_name'],
      'last_name': user['last_name']
    })
  return jsonify(filtered)

@app.route('/retrieve_password/<string:email>', methods = ['GET'])
def retrieve_password(email: str):
  user = User.query.filter_by(email = email).first()
  if user:
    test_email = 'fuerza14@gmail.com'
    msg = Message('Dear user ' + email + '. Your planetary API password request', 
      sender = 'admin@planetary.com', recipients = [test_email], 
      body = 'Dear ' + email + '. Your password is: ' + user.password)
    mail.send(msg)
    return jsonify(message = 'Password send to: ' + test_email)
  else:
    return jsonify(message = 'Email not found'), 404

# PUT

@app.route('/register', methods=['PUT'])
def register():
  email = request.form['email']
  test = User.query.filter_by(email = email).first()
  if test:
    return jsonify(message = 'Email already registered'), 409
  else:
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    password = request.form['password']
    user = User(first_name = first_name, last_name = last_name, email = email, password = password)
    db.session.add(user)
    db.session.commit()
    return jsonify(message = 'User added'), 201

@app.route('/add_planet', methods = ['PUT'])
@jwt_required
def add_planet():
  planet_name = request.form['planet_name']
  test = Planet.query.filter_by(planet_name = planet_name).first()
  if test:
    return jsonify(message = 'Planet already exists'), 409
  else:
    new_planet = Planet(
      planet_name = planet_name,
      planet_type = request.form['planet_type'],
      home_star = request.form['home_star'],
      mass = float(request.form['mass']),
      radius = float(request.form['radius']),
      distance = float(request.form['distance'])
    )
    db.session.add(new_planet)
    db.session.commit()
    return jsonify(message = 'Planet ' + planet_name + ' added')


# POST

@app.route('/login', methods = ['POST'])
def login():
  if request.is_json:
    email = request.json['email']
    password = request.json['password']
  else:
    email = request.form['email']
    password = request.form['password']
  
  test = User.query.filter_by(email = email, password = password).first()
  if test:
    access_token = create_access_token(identity = email)
    return jsonify(message = 'Login successful', access_token = access_token)
  else:
    return jsonify(message = 'Invalid credentials'), 401

@app.route('/update_planet', methods = ['PATCH'])
@jwt_required
def update_planet():
  planet_id = int(request.form['planet_id'])
  planet = Planet.query.filter_by(planet_id = planet_id).first()
  if planet:
    planet.planet_name = request.form['planet_name']
    planet.planet_type = request.form['planet_type']
    planet.home_star = request.form['home_star']
    planet.mass = request.form['mass']
    planet.radius = request.form['radius']
    planet.distance = request.form['distance']
    db.session.commit()
    return jsonify(message = 'Planet updated'), 202
  else:
    return jsonify(message = 'Planet not found'), 404

# DELETE

@app.route('/delete_planet/<string:planet_id>', methods = ['DELETE'])
@jwt_required
def delete_planet(planet_id: int):
  planet = Planet.query.filter_by(planet_id = planet_id).first()
  if planet:
    planet_name = planet.planet_name
    db.session.delete(planet)
    db.session.commit()
    return jsonify(message = 'Planet ' + planet_name + ' has been deleted')
  else:
    return jsonify(message = 'Planet not found'), 404


# database models

class User(db.Model):
  __tablename__ = 'users'
  user_id = Column(Integer, primary_key = True)
  first_name = Column(String)
  last_name = Column(String)
  email = Column(String, unique = True)
  password = Column(String)

class Planet(db.Model):
  __tablename__ = 'planets'
  planet_id = Column(Integer, primary_key = True)
  planet_name = Column(String)
  planet_type = Column(String)
  home_star = Column(String)
  mass = Column(Float)
  radius = Column(Float)
  distance = Column(Float)

class UserSchema(ma.Schema):
  class Meta:
    fields = ('user_id', 'first_name', 'last_name', 'email', 'password')

class PlanetSchema(ma.Schema):
  class Meta:
    fields = ('planet_id', 'planet_name', 'planet_type', 'home_star', 'mass', 'radius', 'distance')

user_schema = UserSchema()
users_schema = UserSchema(many = True)
planet_schema = PlanetSchema()
planets_schema = PlanetSchema(many = True)



# Entry

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0')