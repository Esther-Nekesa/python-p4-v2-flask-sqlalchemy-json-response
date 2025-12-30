#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate
from models import db, Pet

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# This setting ensures JSON is indented and readable in the browser
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def index():
    # Returns a simple JSON greeting
    body = {'message': 'Welcome to the pet directory!'}
    return make_response(body, 200)

@app.route('/pets/<int:id>')
def pet_by_id(id):
    # Query the database for a specific pet
    pet = Pet.query.filter(Pet.id == id).first()

    if pet:
        # Map model attributes to a dictionary
        body = {
            'id': pet.id,
            'name': pet.name,
            'species': pet.species
        }
        status = 200
    else:
        # Return an error message if the pet doesn't exist
        body = {'message': f'Pet {id} not found.'}
        status = 404

    return make_response(body, status)

@app.route('/species/<string:species>')
def pet_by_species(species):
    pets_list = []
    # Query all pets that match the species string
    for pet in Pet.query.filter_by(species=species).all():
        pet_dict = {
            'id': pet.id,
            'name': pet.name,
            # Note: The lab instructions exclude species here to match the target output
        }
        pets_list.append(pet_dict)
    
    body = {
        'count': len(pets_list),
        'pets': pets_list
    }
    return make_response(body, 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)